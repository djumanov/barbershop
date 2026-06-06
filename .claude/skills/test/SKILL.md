---
name: test
description: Use to run or write tests for the barbershop backend. Triggers on "run the tests", "run pytest", "add a test", "check coverage", or verifying a change works. Uses uv + pytest + pytest-asyncio + httpx as configured in this project.
---

# test workflow (barbershop)

This project tests with `pytest`, `pytest-asyncio`, and `httpx` (async test client), all run through `uv`.

## Running tests
- Whole suite: `uv run pytest`
- Verbose: `uv run pytest -v`
- A single file: `uv run pytest tests/test_auth.py`
- A single test: `uv run pytest tests/test_auth.py::test_register -v`
- Stop on first failure: `uv run pytest -x`
- Show print/log output: `uv run pytest -s`

## Writing async tests
- Mark async tests with `@pytest.mark.asyncio` (or configure `asyncio_mode = "auto"` in `[tool.pytest.ini_options]`).
- Use `httpx.AsyncClient` with `ASGITransport` to call the app without a live server:
  ```python
  from httpx import AsyncClient, ASGITransport
  from app.main import app

  transport = ASGITransport(app=app)
  async with AsyncClient(transport=transport, base_url="http://test") as client:
      resp = await client.post("/api/v1/auth/register", json={...})
  ```
- For DB-touching tests, prefer a transactional fixture that rolls back, or a disposable test database — don't hit the dev Postgres.

## Conventions
- Test files live in `tests/`, named `test_*.py`.
- Cover the auth flow end to end: register → login → `/users/me`, plus failure cases
  (duplicate email, bad password, missing/expired token).
- Keep tests independent of execution order.

## After changing code
Run `uv run pytest` and report the real result. If tests fail, show the failing output — do not claim success.
