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

## Status

Project structure is in place. Framework setup and the first vertical slice will be added incrementally.
