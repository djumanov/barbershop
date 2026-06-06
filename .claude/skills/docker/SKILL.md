---
name: docker
description: Use for Docker and docker compose work in the barbershop project — building images, bringing the stack up/down, viewing logs, exec-ing into containers, debugging healthchecks. Triggers on "docker compose up", "build the image", "container logs", "rebuild", "the db container", or any container task. Always uses `docker compose` (v2), never `docker-compose`.
---

# docker workflow (barbershop)

This project ships a multi-stage `Dockerfile` (uv-based build, non-root runtime, gunicorn + `uvicorn.workers.UvicornWorker`) and a `docker-compose.yml` with two services: `db` (postgres:16) and `app`. Always use the v2 `docker compose` syntax.

## Everyday commands
- Build images: `docker compose build`
- Start the stack (foreground): `docker compose up`
- Start detached: `docker compose up -d`
- Rebuild + restart after dep/Dockerfile changes: `docker compose up --build`
- Stop and remove containers/network: `docker compose down`
- Stop AND wipe the db volume (destroys data): `docker compose down -v`
- Show service status: `docker compose ps`

## Logs & debugging
- All logs, follow: `docker compose logs -f`
- One service: `docker compose logs -f app` (or `db`)
- Shell into the running app: `docker compose exec app sh`
- One-off command in a fresh app container: `docker compose run --rm app <cmd>`
- psql into the db: `docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"`

## Healthchecks & startup ordering
- `db` has a `pg_isready` healthcheck; `app` `depends_on` it with `condition: service_healthy`.
- If `app` exits immediately, check `docker compose logs app` — usually a bad `DATABASE_URL`,
  a missing env var, or migrations failing.
- In dev, the `app` service runs `alembic upgrade head` before launching uvicorn `--reload`,
  with the source bind-mounted. A failed migration will stop the container — read the log.

## Dockerfile / build notes
- Multi-stage: the build stage copies the `uv` binary from `ghcr.io/astral-sh/uv` and installs
  deps with `uv sync --frozen --no-dev`; the final stage runs as a non-root user.
- `.dockerignore` must exclude `.venv`, `.git`, `__pycache__`, `.env` — never bake secrets into the image.
- Production CMD uses gunicorn with `uvicorn.workers.UvicornWorker`; the dev override in compose swaps
  to `uvicorn --reload`.
- Rebuild after changing `pyproject.toml`/`uv.lock` (deps) or the Dockerfile; a bind-mount covers app
  code in dev so source edits don't need a rebuild.

## Don'ts
- Don't use `docker-compose` (v1) — only `docker compose`.
- Don't commit `.env`; compose reads it but it stays out of git and the image.
- Don't run `down -v` casually — it deletes the Postgres volume and all data.
