# Loyihani ishga tushirish (Development & Production)

Bu hujjat `barbershop` FastAPI backendini **development** va **production**
rejimlarida qanday ishga tushirishni tushuntiradi.

> Holat: hozircha app `/health` endpoint bilan ishlaydi. Auth/DB endpointlari,
> migratsiyalar (Alembic) va `docker compose` keyingi fazalarda qo'shiladi —
> quyida ular "(keyinroq)" deb belgilangan.

---

## 1. Talablar

- **Python 3.11+**
- **uv** — paket va virtual muhit menejeri ([o'rnatish](https://docs.astral.sh/uv/))
- **PostgreSQL 16** (lokalda 14 ham ishlaydi) — DB ishlatadigan fazalardan kerak
- **Redis** — cache va Celery result backend uchun
- **RabbitMQ** — Celery broker (message queue) uchun

Lokalda (macOS, Homebrew) servislar:

```bash
brew services start postgresql@16   # yoki @14
brew services start redis
brew services start rabbitmq
```

> Muqobil: hammasini `docker compose` orqali ko'tarish — Phase 13 (keyinroq).

---

## 2. Bir martalik tayyorgarlik

```bash
# 1) .env faylini namunadan yaratish
cp .env.example .env

# 2) bog'liqliklarni o'rnatish (.venv avtomatik yaratiladi)
uv sync
```

### `.env` dagi muhim o'zgaruvchilar

| O'zgaruvchi | Dev | Prod | Izoh |
|-------------|-----|------|------|
| `ENVIRONMENT` | `development` | `production` | `/docs` ko'rinishini boshqaradi |
| `DEBUG` | `true` | `false` | SQL echo + xato izlari |
| `SECRET_KEY` | ixtiyoriy | **kuchli, maxfiy** | JWT imzolash kaliti |
| `POSTGRES_HOST` | `localhost` | `db` (compose) | lokal vs konteyner |
| `REDIS_URL` | `redis://localhost:6379/0` | `redis://redis:6379/0` | cache |
| `RABBITMQ_URL` / `CELERY_BROKER_URL` | `amqp://guest:guest@localhost:5672//` | `...@rabbitmq:5672//` | broker |

Kuchli `SECRET_KEY` yaratish:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

> `.env` **hech qachon** git'ga commit qilinmaydi (`.gitignore`da). Faqat
> `.env.example` versiyalanadi.

---

## 3. Development rejimi

```bash
uv run uvicorn app.main:app --reload
```

- 🔁 `--reload` — kod o'zgarsa server avtomatik qayta yuklanadi
- 🌐 App: <http://localhost:8000>
- ❤️ Health: <http://localhost:8000/health> → `{"status":"ok","environment":"development"}`
- 📚 Swagger UI: <http://localhost:8000/docs> (dev'da **ochiq**)
- 📕 ReDoc: <http://localhost:8000/redoc>

Bitta worker, debug yoqilgan, hot-reload — kundalik ishlab chiqish uchun.

---

## 4. Production rejimi

`.env` da `ENVIRONMENT=production` va `DEBUG=false` bo'lsin, keyin **gunicorn**:

```bash
ENVIRONMENT=production uv run gunicorn app.main:app -c gunicorn.conf.py
```

- ⚙️ gunicorn + `UvicornWorker`, worker soni `CPU*2+1` (`gunicorn.conf.py`)
- 🌐 App: <http://localhost:8000> (`bind = 0.0.0.0:8000`)
- ❤️ `/health` → `{"status":"ok","environment":"production"}`
- 🚫 `/docs`, `/redoc`, `/openapi.json` → **404** (prod'da xavfsizlik uchun o'chiq)
- Reload yo'q, ko'p worker, debug o'chiq, loglar stdout/stderr ga

---

## 5. Dev vs Prod — qisqacha

| | Development | Production |
|--|-------------|------------|
| Server | uvicorn | gunicorn + UvicornWorker |
| Worker soni | 1 | `CPU*2+1` |
| Auto-reload | ✅ | ❌ |
| `/docs` (Swagger) | ✅ ochiq | ❌ 404 |
| `DEBUG` | `true` | `false` |
| Buyruq | `uv run uvicorn app.main:app --reload` | `uv run gunicorn app.main:app -c gunicorn.conf.py` |

---

## 6. Ma'lumotlar bazasi migratsiyalari (keyinroq — Phase 12)

Alembic sozlangach:

```bash
uv run alembic upgrade head        # barcha migratsiyalarni qo'llash
uv run alembic revision --autogenerate -m "xabar"   # yangi migratsiya
```

---

## 7. Celery worker (keyinroq)

Celery app moduli yozilgach, background worker:

```bash
uv run celery -A app.core.celery_app worker --loglevel=info
```

> Hozir broker (RabbitMQ) va backend (Redis) sozlangan va ulanish sinovdan
> o'tgan, lekin worker moduli hali yozilmagan.

---

## 8. Docker bilan (keyinroq — Phase 13)

```bash
docker compose up --build
```

Postgres + Redis + RabbitMQ + app (+ worker) ni birga ko'taradi, migratsiyalarni
qo'llaydi va gunicorn bilan xizmat qiladi. **Hozir `docker-compose.yml` yo'q.**

---

## 9. Tez yordam (troubleshooting)

- **Port 8000 band** — boshqa portda: `uv run uvicorn app.main:app --reload --port 8001`.
- **DB ulanmayapti** — `pg_isready -h localhost -p 5432`; `.env` dagi
  `POSTGRES_*` lokal Postgres rol/baza bilan mosligini tekshiring (Homebrew
  odatda rolni OS foydalanuvchisi nomi bilan yaratadi, `barbershop` bazasi
  bo'lmasligi mumkin).
- **Redis/RabbitMQ** — `redis-cli ping` (→ `PONG`), `nc -z localhost 5672`.
- **prod'da `/docs` 404** — bu normal; faqat development'da ochiladi.
