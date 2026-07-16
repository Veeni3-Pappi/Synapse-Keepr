# Database Plan

PostgreSQL is the system of record. Django migrations are the source of truth once the backend is bootstrapped.

## Core entities

| Entity | Responsibility |
| --- | --- |
| `User` | Application user, initially backed by Google identity. |
| `IntegrationConnection` | One user's authorized provider connection and encrypted provider credentials. |
| `Playlist` | A provider playlist imported through a connection. |
| `Resource` | A normalized library item; in this MVP, a YouTube video. |
| `PlaylistResource` | Membership and ordering of resources inside playlists. |
| `ImportJob` | Import lifecycle, progress, errors, and timestamps. |

## Resource normalization

`Resource` will hold fields common to future sources: owner, provider, external ID, title, description, URL, thumbnail URL, published timestamp, duration, and raw provider metadata. Provider-specific fields remain in structured metadata until a genuine cross-provider need warrants a first-class column.

Uniqueness will prevent duplicates using the owner, provider, and provider external ID. A playlist-resource relationship supports the same video appearing in multiple playlists without duplicating the resource.

## Security

- Provider refresh tokens are encrypted at rest and never exposed by the API.
- Application JWTs are short-lived and refreshable.
- Every library query is scoped to the authenticated owner.
