---
name: git
description: Use for git work in the barbershop repo — staging, committing, branching, and opening PRs. Triggers on "commit", "create a branch", "open a PR", "git status", or any version-control request. Enforces this repo's conventions (never commit .env or .venv, branch off master, Conventional Commits).
---

# git workflow (barbershop)

Helper conventions for version control in this FastAPI/uv project. Follow these unless the user overrides them.

## Before committing
- Run `git status` and `git diff --staged` and show the user what will be committed.
- NEVER stage or commit: `.env`, `.venv/`, `__pycache__/`, `*.db`, `.ruff_cache/`, `.pytest_cache/`. These are gitignored — if one shows up staged, stop and warn.
- DO commit `uv.lock` (the lockfile is intentionally tracked).
- Prefer staging explicit paths (`git add app/ tests/ pyproject.toml`) over `git add -A`.
- Only commit when the user asks. If on `master`, create a feature branch first (see below).

## Branching
- Branch off the default branch `master`.
- Name branches `feat/<slug>`, `fix/<slug>`, `chore/<slug>`, or `docs/<slug>`.
- `git switch -c feat/<slug>` to create and switch.

## Commit messages — Conventional Commits
Format: `<type>(<scope>): <subject>`
- Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `build`, `ci`.
- Scope is optional but encouraged (e.g. `auth`, `db`, `users`, `alembic`, `docker`).
- Subject: imperative mood, lowercase, no trailing period, ≤ 72 chars.
- Examples:
  - `feat(auth): add refresh-token endpoint`
  - `fix(db): use async_sessionmaker with expire_on_commit=False`
  - `chore(deps): add pwdlib[bcrypt]`

End every commit message body with:
```
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
```

## Pull requests
- Use the `gh` CLI: `gh pr create`.
- Push the branch first (`git push -u origin <branch>`).
- PR title follows the same Conventional Commits format.
- PR body: short summary, a "What changed" bullet list, and a "How to test" section
  (e.g. `docker compose up`, then register → login → `/users/me`).
- End the PR body with:
```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Don'ts
- Don't force-push to `master`.
- Don't `git rebase -i` / `git add -i` (interactive flags aren't supported in this environment).
- Don't amend or rewrite commits the user has already pushed unless they ask.
