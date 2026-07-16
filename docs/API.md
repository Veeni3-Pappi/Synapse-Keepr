# API Plan

All endpoints will be namespaced under `/api/v1/`. This is an implementation plan; endpoints will be documented with request and response examples as they are built.

## Implemented

### `GET /health/`

Public liveness endpoint. It returns `200 OK` with:

```json
{ "status": "ok", "service": "synapse-keepr-api" }
```

### `GET /playlists/` and `GET /playlists/{id}/`

Authenticated endpoints for an owner's imported YouTube playlists. List items include their imported-resource count.

### `GET /resources/` and `GET /resources/{id}/`

Authenticated endpoints for an owner's imported videos. The list accepts optional `q` (keyword search over title and description) and `playlist` (playlist ID) query parameters.

### `GET /imports/` and `GET /imports/{id}/`

Authenticated endpoints that expose an owner's import-job status and progress counters. Creating an import job will be added alongside the YouTube connection flow.

### `POST /resources/{id}/summary/`

Queues an AI summary for an owned resource and returns `202 Accepted`. Poll `GET /resources/{id}/` for the summary status and content. Summaries require `OPENAI_API_KEY` and either an imported description or an authorized transcript.

| Area | Planned endpoints | Purpose |
| --- | --- | --- |
| Authentication | `POST /auth/google/`, `POST /auth/refresh/`, `POST /auth/logout/` | Exchange Google authorization for application JWTs and manage sessions. |
| Integrations | `GET /integrations/`, `POST /integrations/youtube/connect/` | Show connection state and begin/complete YouTube authorization. |
| Imports | `POST /imports/youtube/` | Start an import after YouTube authorization. |

## API conventions

- JSON request and response bodies.
- JWT bearer token required except for authentication callbacks.
- Pagination for collection endpoints.
- Consistent error payloads with a machine-readable `code` and user-safe `detail`.
- Cursor or page-number pagination will be selected with the first list endpoint and applied consistently.
