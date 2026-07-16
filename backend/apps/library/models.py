from django.conf import settings
from django.db import models


class Provider(models.TextChoices):
    YOUTUBE = "youtube", "YouTube"


class IntegrationConnection(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="integration_connections")
    provider = models.CharField(max_length=32, choices=Provider.choices)
    provider_account_id = models.CharField(max_length=255)
    encrypted_refresh_token = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["owner", "provider", "provider_account_id"], name="unique_provider_connection")]


class Playlist(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="playlists")
    connection = models.ForeignKey(IntegrationConnection, on_delete=models.CASCADE, related_name="playlists")
    external_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    imported_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["connection", "external_id"], name="unique_connection_playlist")]
        ordering = ["name"]


class Resource(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources")
    provider = models.CharField(max_length=32, choices=Provider.choices)
    external_id = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    url = models.URLField()
    thumbnail_url = models.URLField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)
    provider_metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["owner", "provider", "external_id"], name="unique_owner_provider_resource")]
        ordering = ["-published_at", "-created_at"]


class PlaylistResource(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name="playlist_resources")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="playlist_memberships")
    position = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["playlist", "resource"], name="unique_playlist_resource")]
        ordering = ["position"]


class ImportJob(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="import_jobs")
    connection = models.ForeignKey(IntegrationConnection, on_delete=models.CASCADE, related_name="import_jobs")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED)
    playlists_discovered = models.PositiveIntegerField(default=0)
    resources_imported = models.PositiveIntegerField(default=0)
    error_detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]


class ResourceSummary(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, related_name="summary")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED)
    content = models.TextField(blank=True)
    model = models.CharField(max_length=100, blank=True)
    error_detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
