# Full-Stack DevOps Project

> **Stack:** HTML/JS Frontend · FastAPI Backend · PostgreSQL · Docker · GitHub Actions

---

## Folder Structure

```
devops-project/
├── frontend/
│   ├── index.html          # Single-page dashboard (HTML + CSS + JS)
│   ├── Dockerfile          # nginx:alpine image
│   └── nginx.conf          # Reverse-proxy config
│
├── backend/
│   ├── main.py             # FastAPI app (routes + DB models)
│   ├── requirements.txt
│   ├── Dockerfile          # python:3.11-slim multi-stage build
│   └── tests/
│       └── test_main.py    # Unit tests (pytest)
│
├── db/
│   └── init.sql            # Seed data (runs once on first PG start)
│
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
│
├── docker-compose.yml      # Orchestrates all 3 services
├── .env.example            # Template — copy to .env
├── .gitignore
└── README.md
```

---

## Quick Start (Local)

### Prerequisites
- Docker Desktop ≥ 24 (includes Compose v2)
- Git

### 1 — Clone & configure

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd devops-project

cp .env.example .env          # uses default dev credentials
```

### 2 — Build & start everything

```bash
docker compose up --build
```

This starts three containers:

| Service    | URL                        |
|------------|----------------------------|
| Frontend   | http://localhost:3000      |
| Backend    | http://localhost:8000      |
| PostgreSQL | localhost:5432             |

### 3 — Open the app

Visit **http://localhost:3000** — the dashboard auto-polls the API.

### 4 — Try the API directly

```bash
# Root
curl http://localhost:8000/

# Health check (shows DB status)
curl http://localhost:8000/health

# Submit a record
curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "message": "Hello from curl!"}'

# List all records
curl http://localhost:8000/data

# Interactive API docs
open http://localhost:8000/docs
```

### 5 — Stop everything

```bash
docker compose down          # keep DB volume
docker compose down -v       # also delete DB data
```

---

## Run Backend Locally (without Docker)

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Point at your local Postgres (or Docker Postgres on 5432)
export DATABASE_URL=postgresql://devuser:devpass@localhost:5432/devdb

uvicorn main:app --reload --port 8000
```

---

## Run Tests

```bash
cd backend
pip install pytest httpx
pytest tests/ -v
```

---

## GitHub Setup

```bash
# 1. Create a new repo on github.com (no README, no .gitignore)

# 2. Inside the project folder:
git init
git add .
git commit -m "feat: initial full-stack devops project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

GitHub Actions will automatically trigger on push to `main`.

---

## CI/CD Pipeline (GitHub Actions)

`.github/workflows/ci.yml` runs four jobs in sequence:

```
push to main
  └─► 1. Lint          — flake8 + py_compile
  └─► 2. Unit Tests    — pytest (mocked DB)
  └─► 3. Docker Build  — validates both Dockerfiles + compose config
  └─► 4. Integration   — spins up the full stack, hits all endpoints
```

---

## API Reference

| Method | Path      | Description                      |
|--------|-----------|----------------------------------|
| GET    | `/`       | Returns API name & version       |
| GET    | `/health` | DB connectivity + timestamp      |
| POST   | `/data`   | Save `{name, message}` to DB     |
| GET    | `/data`   | List all entries (newest first)  |
| GET    | `/docs`   | Auto-generated Swagger UI        |

---

## Environment Variables

| Variable          | Default    | Description              |
|-------------------|------------|--------------------------|
| `POSTGRES_DB`     | `devdb`    | Database name            |
| `POSTGRES_USER`   | `devuser`  | DB user                  |
| `POSTGRES_PASSWORD` | `devpass` | DB password             |
| `DATABASE_URL`    | _(built from above)_ | Full connection string |
