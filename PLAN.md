# Build Plan

## Phase 1 -- Foundation (day 1-2)

- Project structure, Dockerfile, docker-compose with PostgreSQL
- FastAPI app factory with lifespan (startup/shutdown hooks)
- Config via pydantic-settings, reading from .env
- Async SQLAlchemy engine and session factory
- Alembic setup with async migration support
- User model and initial migration
- Health check endpoint

## Phase 2 -- Auth (day 2-3)

- Password hashing with bcrypt via passlib
- JWT access/refresh token generation and validation
- Register endpoint: create user, hash password, return tokens
- Login endpoint: verify credentials, return tokens
- Refresh endpoint: validate refresh token, issue new access token
- get_current_user dependency that extracts user from Authorization header
- require_role dependency for admin-only routes
- /auth/me endpoint returning current user profile

## Phase 3 -- CRUD and middleware (day 3-5)

- Item model as example resource (belongs to user)
- Item CRUD router: create, list (paginated), get, update, delete
- Pagination helper: offset/limit with total count in response
- Rate limiting middleware: in-memory counter per IP, configurable window/max
- Request ID middleware: generate UUID, attach to response headers and log context
- Structured JSON logging with request method, path, status, duration
- CORS middleware configuration

## Phase 4 -- Testing and CI (day 5-7)

- conftest.py: async test client, SQLite test database, fixture for authenticated user
- Auth tests: register, login, refresh, access protected route, role enforcement
- Item tests: full CRUD cycle, ownership enforcement, pagination
- GitHub Actions: lint (ruff), test (pytest), Docker build
- README: setup, API reference, authentication guide, deployment
