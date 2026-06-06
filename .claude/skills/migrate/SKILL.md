---
name: migrate
description: Use for database migrations in the barbershop project with Alembic (async). Triggers on "create a migration", "run migrations", "alembic upgrade/downgrade", "the schema changed", or after editing a SQLAlchemy model. Uses the async Alembic env wired to app.core.config settings.
---

# migrate workflow (barbershop)

Schema changes are managed with **Alembic** (async template), run through `uv`. The Alembic env imports `Base` and the models and pulls the URL from `app.core.config.settings.database_url`.

## Typical flow after changing a model
1. Edit/add the SQLAlchemy model under `app/models/` and make sure it's imported in `alembic/env.py` (so autogenerate sees it).
2. Generate a migration:
   `uv run alembic revision --autogenerate -m "<short description>"`
3. **Review the generated file** in `alembic/versions/` before applying — autogenerate can miss server defaults, enum changes, and index/constraint renames. Edit by hand if needed.
4. Apply it: `uv run alembic upgrade head`

## Common commands
- Apply all pending: `uv run alembic upgrade head`
- Roll back one: `uv run alembic downgrade -1`
- Show current revision: `uv run alembic current`
- History: `uv run alembic history --verbose`
- New empty (hand-written) migration: `uv run alembic revision -m "<description>"`

## Notes
- Postgres must be reachable (`docker compose up db`) for autogenerate and upgrade — both connect to the database.
- In docker compose, the app's dev command runs `alembic upgrade head` on startup before launching uvicorn.
- One logical change per migration; use a clear `-m` message. Don't edit a migration that's already been applied/shared — add a new one.
- Never autogenerate against the production database; generate against a dev/throwaway DB and apply the reviewed file in prod.
