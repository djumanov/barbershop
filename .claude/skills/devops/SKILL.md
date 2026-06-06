---
name: devops
description: Use for operational/DevOps tasks on the barbershop backend — managing env vars and secrets, running the full stack, smoke-testing the API, health checks, and deployment/CI guidance. Triggers on "deploy", "set up env", "smoke test", "is it healthy", "CI", "production config", or running the app end to end. Broader companion to the focused docker, migrate, and test skills.
---

# devops workflow (barbershop)

Operational guidance for running and shipping this FastAPI + Postgres service. For container mechanics use the `docker` skill, for schema changes the `migrate` skill, for the test suite the `test` skill.

## Environment & secrets
- Config is loaded by pydantic-settings from `.env` (see `app/core/config.py`). `.env.example` lists every variable.
- Copy and fill before first run: `cp .env.example .env`, then set real values.
- Required vars: `POSTGRES_USER/PASSWORD/DB/HOST/PORT`, `SECRET_KEY`, `ALGORITHM`,
  `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, plus `APP_NAME`/`DEBUG`.
- `POSTGRES_HOST` is `db` inside compose, `localhost` when running locally with `uv`.
- NEVER commit `.env`. Generate a strong secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
- In production set `DEBUG=false` and provide secrets via the platform's secret store / env, not a file in the image.

## Running the stack
- Full stack (db + app): `docker compose up --build` → app on `http://localhost:8000`, `/docs` for Swagger.
- Local app against a containerized db: `docker compose up -d db`, then `uv run uvicorn app.main:app --reload`.
- Apply migrations: `uv run alembic upgrade head` (compose dev command does this automatically on startup).

## Health & smoke test
- Liveness: `curl -s http://localhost:8000/health` → `{"status":"ok"}`.
- End-to-end auth smoke (register → login → me):
  ```sh
  BASE=http://localhost:8000/api/v1
  curl -s -X POST $BASE/auth/register -H 'Content-Type: application/json' \
    -d '{"email":"a@b.com","password":"secret123"}'
  TOKEN=$(curl -s -X POST $BASE/auth/login \
    -d 'username=a@b.com&password=secret123' \
    -H 'Content-Type: application/x-www-form-urlencoded' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
  curl -s $BASE/users/me -H "Authorization: Bearer $TOKEN"
  ```
  `/auth/login` uses `OAuth2PasswordRequestForm` → send form-encoded `username`/`password`, not JSON.

## Deploy / CI guidance
- Build a release image from the multi-stage Dockerfile; it installs `--frozen --no-dev` and runs non-root.
- Run migrations as a separate step/job before rolling the new app version: `alembic upgrade head`.
- Serve with gunicorn + `uvicorn.workers.UvicornWorker`; size workers to the host (rule of thumb `2*CPU+1`).
- A minimal CI pipeline: `uv sync` → `uv run ruff check .` → `uv run ruff format . --check` → `uv run pytest`
  → `docker compose build`.
- Keep `uv.lock` committed so CI and prod resolve identical dependency versions.

## Operational don'ts
- Don't autogenerate or run destructive migrations against production from your laptop.
- Don't expose `/docs` publicly in prod unless intended; gate it behind `DEBUG` or auth if needed.
- Don't run the app as root or bake `.env`/secrets into the image.
