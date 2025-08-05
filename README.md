# Math Operations Microservice

A FastAPI based microservice that exposes three arithmetic operations—factorial, Fibonacci, power—over HTTP.  
Each request is logged to a local SQLite database, responses are cached in‑process, protected by an API‑Key header, and instrumented with Prometheus metrics.

---

## Quick start

```bash
# 1. Create a virtual‑env & install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Run the service (hot‑reload)
setx API_KEY=secret_math2000
uvicorn app.main:app --reload

# 3. Visit the interactive docs
open http://localhost:8000/docs
```

---

## Configuration (.env variables)

| Variable       | Default                   | Description                                   |
| -------------- | ------------------------- | --------------------------------------------- |
| `API_KEY`      | **none required**         | Shared secret sent as `X-API-Key` header.     |
| `DATABASE_URL` | `sqlite:///./app/database.db` | Any SQLAlchemy URL; defaults to local SQLite. |
| `DEBUG`        | `False`                   | Enables verbose logging & auto‑reload.        |

Put them in a .env file or export from shell.

---

## REST API overview

| Method & path     | Purpose                                    | Auth? |
|-------------------|--------------------------------------------|-------|
| `GET /health`     | Liveness probe. Returns `{"status":"ok"}`. | No    |
| `POST /factorial` | Compute *n!* (`n ≤ 170`).                  | Yes   |
| `POST /fibonacci` | Compute F(*n*) (up to *n = 1476*).         | Yes   |
| `POST /power`     | Compute `base ** exponent` (float safe).   | Yes   |
| `GET /logs`       | Return last ≤ 300 logged calls.            | Yes   |
| `GET /metrics`    | Prometheus scrape endpoint.                | Yes   |

Schema example:

```json
# POST /factorial  (request)
{ "n": 5 }

# 201 Created (success)
{
  "operation": "factorial",
  "input":   { "n": 5 },
  "result":  120,
  "timestamp": "2025‑07‑29T13:00:00Z",
  "status": "success"
}

# 400 Bad Request (error)
{
  "status": "error",
  "message": "n must be non‑negative (n ≥ 0)"
}
```

---

## Development/Testing

```bash
# run style checks & unit tests
flake8 app tests
python -m pytest -q      # uses in‑memory SQLite via override
```

Caching is provided by **functools.lru_cache**.  
Metrics via **prometheus-fastapi-instrumentator** (see **/metrics**).  
Logs are inspectable with python **tools/debug_db.py**.

---

## Roadmap / Nice-to-haves

- Dockerfile & Containerization.  
- Automatic key rotation endpoint (/auth/token).   
- Grafana dashboard for Prometheus metrics

---

Built using **FastAPI**, **SQLAlchemy**, **SQLite**, **Prometheus**, and **Uvicorn**.