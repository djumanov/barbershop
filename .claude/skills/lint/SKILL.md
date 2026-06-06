---
name: lint
description: Use to lint or format the barbershop codebase with ruff. Triggers on "run ruff", "lint the code", "format the code", "fix lint errors", or before committing. Uses the ruff config in pyproject.toml (line-length 100).
---

# lint workflow (barbershop)

Linting and formatting use **ruff**, run through `uv`. Config lives in `[tool.ruff]` in `pyproject.toml` (line-length 100).

## Commands
- Check for issues: `uv run ruff check .`
- Auto-fix safe issues: `uv run ruff check . --fix`
- Format code: `uv run ruff format .`
- Check formatting without writing: `uv run ruff format . --check`

## Recommended order before a commit
1. `uv run ruff check . --fix`
2. `uv run ruff format .`
3. `uv run ruff check .` (confirm clean)

## Conventions
- Keep code lint-clean; don't suppress with blanket `# noqa` — fix the cause or use a targeted `# noqa: <code>` with a reason.
- Imports: let ruff's isort rules (`I`) order them; don't hand-sort.
- Match line-length 100 from the project config; don't reformat to a different width.
- Run this on the files you actually changed before reporting a task done.
