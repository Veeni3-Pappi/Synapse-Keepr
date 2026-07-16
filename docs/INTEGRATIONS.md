# YouTube and AI integrations

## YouTube import

Synapse Keepr imports a user's saved videos through the YouTube Data API, not by scraping YouTube.

1. In Google Cloud Console, create a project and enable **YouTube Data API v3**.
2. Configure the OAuth consent screen, then create a **Web application** OAuth client.
3. Add `http://localhost:8000/api/v1/integrations/youtube/callback/` as an authorized redirect URI for local development.
4. Set `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, and `GOOGLE_OAUTH_REDIRECT_URI` in `.env`; never commit them.
5. The backend will redirect the signed-in user to Google with the minimal `https://www.googleapis.com/auth/youtube.readonly` scope. The callback exchanges the authorization code for tokens, stores the refresh token encrypted at rest, and queues an import job.
6. The worker calls `playlists.list`, `playlistItems.list`, and `videos.list`, then upserts the normalized `Playlist` and `Resource` records.

An API key alone cannot read a person's private playlists or saved videos; the user must complete OAuth consent. The redirect URI must exactly match the Google Cloud configuration.

You may still create a restricted YouTube API key for public-data requests and quota monitoring, but it is not used to import a signed-in user's private library.

## AI summaries

The summary endpoint runs in Celery so a dashboard request never waits on an AI response. It sends the imported description or a future authorized transcript to the OpenAI Responses API and saves the result on `ResourceSummary`.

Set `OPENAI_API_KEY` only in the runtime environment. The server is the only component that sees this key; the Next.js frontend must never receive it. Metadata-only summaries should be labelled accordingly. To summarize what a video actually teaches, import a transcript where permitted, store it in provider metadata, then submit it to the summary task.

Use a lower-cost model for asynchronous summaries and keep the prompt constrained to the source text so the output does not invent lessons. Add rate limits, retries, and a per-user queue before enabling the feature broadly.
