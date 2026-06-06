# syntax=docker/dockerfile:1

# ---- Builder: install dependencies into a venv with uv ----
FROM python:3.11-slim AS builder

# Bring in the uv binary.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install dependencies first (cached layer), without the project code.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the source.
COPY . .
RUN uv sync --frozen --no-dev

# ---- Runtime: minimal image, non-root ----
FROM python:3.11-slim AS runtime

# Create an unprivileged user.
RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app

# Copy the populated venv and source from the builder.
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

# Production default: gunicorn with Uvicorn workers.
# (docker compose overrides this to uvicorn --reload for development.)
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
