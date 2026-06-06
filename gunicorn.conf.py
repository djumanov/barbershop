"""Gunicorn configuration for production.

Run with: gunicorn app.main:app -c gunicorn.conf.py
Uses Uvicorn workers so the ASGI app runs under gunicorn's process manager.
"""

import multiprocessing

from app.core.config import settings

bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1

# Log to stdout/stderr (container-friendly).
accesslog = "-"
errorlog = "-"
loglevel = "debug" if settings.debug else "info"
