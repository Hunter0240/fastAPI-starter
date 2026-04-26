# FastAPI Starter

A batteries-included FastAPI project template with authentication, database migrations, rate limiting, and Docker deployment. Clone it, define your models, and start building endpoints.

## Features

- Modular router structure (one file per resource)
- SQLAlchemy 2.0 async with Alembic migrations
- JWT auth with access/refresh tokens, password hashing
- Role-based access control (admin, user)
- Rate limiting middleware (per-IP, configurable)
- Request ID middleware for tracing
- Structured JSON logging
- Auto-generated OpenAPI docs at /docs
- Health check endpoint
- CORS configuration
- Pagination helper for list endpoints
- Docker Compose with PostgreSQL, API, and Caddy

## Tech Stack

- Python 3.12
- FastAPI + Uvicorn
- SQLAlchemy 2.0 (async) + Alembic
- PostgreSQL (prod) / SQLite (dev)
- Pydantic v2
- JWT (python-jose + passlib)
- Docker + Docker Compose
- pytest + httpx

## Quick Start

```bash
cp .env.example .env
docker compose up --build
# API docs at http://localhost:8000/docs
```

## API Endpoints

```
POST   /auth/register      -- create account
POST   /auth/login          -- get tokens
POST   /auth/refresh        -- refresh access token
GET    /auth/me             -- current user profile

GET    /items               -- list items (paginated)
POST   /items               -- create item
GET    /items/{id}          -- get item
PUT    /items/{id}          -- update item
DELETE /items/{id}          -- delete item

GET    /health              -- service health
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | required |
| SECRET_KEY | JWT signing key | required |
| ACCESS_TOKEN_EXPIRE | Minutes | 30 |
| REFRESH_TOKEN_EXPIRE | Days | 7 |
| CORS_ORIGINS | Comma-separated origins | * |
| RATE_LIMIT_MAX | Requests per window | 100 |
| RATE_LIMIT_WINDOW | Window in seconds | 60 |
| LOG_LEVEL | Logging level | INFO |

## Project Structure

```
app/
  main.py              -- app factory, middleware, lifespan
  config.py            -- pydantic-settings
  database.py          -- async engine, session factory
  auth/
    router.py          -- login, register, refresh, me
    service.py         -- JWT creation/validation
    dependencies.py    -- get_current_user, require_role
  models/
    user.py
    item.py
  schemas/
    user.py
    item.py
  routers/
    users.py
    items.py
  middleware/
    rate_limit.py
    request_id.py
    logging.py
migrations/
tests/
```
