import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.config import settings
from app.database import Base, engine
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.models.item import Item  # noqa: F401
from app.models.user import User  # noqa: F401
from app.routers.items import router as items_router

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


API_DESCRIPTION = """
Production-ready REST API template with JWT authentication, role-based access
control, rate limiting, and async SQLAlchemy. Built as a starting point for
new projects -- clone it, define your models, and start building endpoints.

## Authentication

All protected endpoints require a Bearer token in the Authorization header.
Get tokens via `/auth/login` or `/auth/register`, then pass the access token:

```
Authorization: Bearer <access_token>
```

Access tokens expire after 30 minutes. Use `/auth/refresh` with your refresh
token to get a new access token without re-authenticating.

## Demo credentials

```
Email:    demo@example.com
Password: demo1234
```
"""

app = FastAPI(
    title="FastAPI Starter",
    description=API_DESCRIPTION,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(items_router)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
