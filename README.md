# Synapse Keepr

> Remember Everything. Find Anything.

Synapse Keepr is an AI-ready personal knowledge vault. This hackathon MVP helps learners reconnect with the YouTube tutorials and resources they saved by importing playlists and making videos easy to browse and search.

## MVP

- Sign in with Google
- Connect a YouTube account
- Import playlists and their videos
- Browse and search imported videos
- Open a video detail view

The current implementation supports YouTube only. PDFs, GitHub, articles, notes, and semantic AI search are intentionally deferred.

## Repository layout

```text
frontend/  Next.js dashboard
backend/   Django REST API and background jobs
docs/      Product and technical documentation
docker/    Local-development container assets
.github/   CI workflows
scripts/   Project automation
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API plan](docs/API.md)
- [Database plan](docs/DATABASE.md)
- [Roadmap](docs/ROADMAP.md)

## Local development

The project uses Docker Compose so every contributor runs compatible PostgreSQL, Redis, backend, Celery worker, and frontend services.

1. Copy `.env.example` to `.env`.
2. Run `docker compose up --build`.
3. Visit `http://localhost:3000`. Verify the API at `http://localhost:8000/api/v1/health/`.

To stop services, run `docker compose down`. Add `--volumes` only when you deliberately want to discard local database data.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before making changes. Every implemented decision must update the appropriate document in `docs/`.

## Status

The contributor-ready foundation is in place: local services, a Django API health check, Celery configuration, and a Next.js application shell. The next slice is the polished dashboard design system.
