import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._buckets: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - settings.rate_limit_window

        hits = self._buckets.get(client_ip, [])
        hits = [t for t in hits if t > window_start]

        if len(hits) >= settings.rate_limit_max:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
            )

        hits.append(now)
        self._buckets[client_ip] = hits
        return await call_next(request)
