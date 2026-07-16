# Architecture

## MVP shape

Synapse Keepr is a monorepo with separate frontend and backend applications:

- `frontend`: Next.js, TypeScript, Tailwind CSS, shadcn/ui, and TanStack Query.
- `backend`: Django, Django REST Framework, Celery, Redis, and PostgreSQL.

The frontend talks to the backend only through versioned REST endpoints. Django owns authentication tokens, persisted data, YouTube integration, and background import jobs.

```text
Browser -> Next.js dashboard -> Django REST API -> PostgreSQL
                                  |
                                  +-> Redis -> Celery worker -> YouTube Data API
```

## Modular backend boundaries

The backend will use domain-focused Django apps rather than a single large app:

- `accounts`: authenticated users and Google OAuth identity.
- `integrations`: provider connections, OAuth credentials, and connector contracts.
- `library`: playlists, resources, and search-facing read models.
- `imports`: import job orchestration and Celery tasks.

YouTube will be the first implementation of the integration contract. Future sources can add their own connector while producing the same normalized `Resource` records used by the library and search UI.

## Key decisions

1. **Normalized resources**: playlists remain YouTube-specific metadata, while videos become generic library resources. This keeps future connectors additive.
2. **Asynchronous imports**: playlist/video imports run through Celery so the dashboard stays responsive and import status can be shown clearly.
3. **REST-first API**: a versioned `/api/v1/` surface makes frontend/backend deployment independent and provides a clean base for a mobile client later.
4. **Keyword search first**: PostgreSQL full-text/trigram search is sufficient for the hackathon. Embeddings and `pgvector` are a later enhancement, not an MVP dependency.
5. **Token separation**: Google OAuth tokens are retained server-side for YouTube access; the browser receives our application JWT, never a provider access token.

## Non-goals for this MVP

- Multi-provider import
- Semantic/vector search
- User-created notes and OCR
- Collaboration and sharing
- Production billing, quotas, and analytics
