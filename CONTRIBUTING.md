# Contributing to Synapse Keepr

Thanks for improving Synapse Keepr. Keep pull requests focused: one feature or fix per pull request whenever possible.

## Local setup

1. Copy `.env.example` to `.env` and replace development secrets as needed.
2. Run `docker compose up --build`.
3. Open `http://localhost:3000`; API health is available at `http://localhost:8000/api/v1/health/`.

For non-Docker development, install `backend/requirements.txt`, then run Django from `backend/`; install frontend dependencies with `npm install` from `frontend/`.

## Contribution expectations

- Keep TypeScript strict and add tests for backend behavior.
- Do not commit `.env`, OAuth credentials, refresh tokens, or generated build directories.
- Update the relevant file under `docs/` whenever an endpoint, schema, architecture decision, or roadmap item changes.
- Run the checks listed in the README before opening a pull request.

## Pull request checklist

- [ ] Scope is clear and linked to an MVP roadmap item.
- [ ] Documentation matches the implementation.
- [ ] Tests and lint/type checks pass locally.
- [ ] UI changes include loading, empty, and error states where applicable.
