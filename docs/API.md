# API Plan

All endpoints will be namespaced under `/api/v1/`. This is an implementation plan; endpoints will be documented with request and response examples as they are built.

| Area | Planned endpoints | Purpose |
| --- | --- | --- |
| Authentication | `POST /auth/google/`, `POST /auth/refresh/`, `POST /auth/logout/` | Exchange Google authorization for application JWTs and manage sessions. |
| Integrations | `GET /integrations/`, `POST /integrations/youtube/connect/` | Show connection state and begin/complete YouTube authorization. |
| Imports | `POST /imports/youtube/`, `GET /imports/{id}/` | Start an import and poll job progress. |
| Playlists | `GET /playlists/`, `GET /playlists/{id}/` | Browse imported YouTube playlists. |
| Resources | `GET /resources/`, `GET /resources/{id}/` | List, search, filter, and view imported videos. |

## API conventions

- JSON request and response bodies.
- JWT bearer token required except for authentication callbacks.
- Pagination for collection endpoints.
- Consistent error payloads with a machine-readable `code` and user-safe `detail`.
- Cursor or page-number pagination will be selected with the first list endpoint and applied consistently.
