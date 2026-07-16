import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from celery import shared_task
from .models import ResourceSummary

SUMMARY_MODEL = "gpt-5.4-nano"


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def generate_resource_summary(self, summary_id):
    """Create a concise learning summary from imported video metadata or a future transcript."""
    summary = ResourceSummary.objects.select_related("resource").get(pk=summary_id)
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        summary.status = ResourceSummary.Status.FAILED
        summary.error_detail = "OPENAI_API_KEY is not configured."
        summary.save(update_fields=["status", "error_detail", "updated_at"])
        return

    resource = summary.resource
    source_text = resource.provider_metadata.get("transcript") or resource.description
    if not source_text:
        summary.status = ResourceSummary.Status.FAILED
        summary.error_detail = "A video description or authorized transcript is required to generate a summary."
        summary.save(update_fields=["status", "error_detail", "updated_at"])
        return

    summary.status = ResourceSummary.Status.PROCESSING
    summary.error_detail = ""
    summary.save(update_fields=["status", "error_detail", "updated_at"])
    payload = json.dumps({
        "model": SUMMARY_MODEL,
        "instructions": "Summarize the supplied learning resource. Be accurate, concise, and do not invent facts. Return a short overview followed by 3-5 key takeaways.",
        "input": f"Title: {resource.title}\n\nSource material:\n{source_text}",
    }).encode()
    request = Request(
        "https://api.openai.com/v1/responses",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode())
    except (HTTPError, URLError, TimeoutError) as error:
        summary.status = ResourceSummary.Status.FAILED
        summary.error_detail = "The summary provider could not be reached."
        summary.save(update_fields=["status", "error_detail", "updated_at"])
        raise self.retry(exc=error)

    summary.status = ResourceSummary.Status.COMPLETED
    summary.content = result.get("output_text", "").strip()
    if not summary.content:
        summary.status = ResourceSummary.Status.FAILED
        summary.error_detail = "The summary provider returned no text."
        summary.save(update_fields=["status", "error_detail", "updated_at"])
        return
    summary.model = SUMMARY_MODEL
    summary.save(update_fields=["status", "content", "model", "updated_at"])
