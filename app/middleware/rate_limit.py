import time
from collections import deque

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import settings

_MAX_BUCKETS = 10_000
_EVICT_INTERVAL = 60.0


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._buckets: dict[str, deque[float]] = {}
        self._last_evict: float = 0.0

    def _evict_stale(self, now: float) -> None:
        if now - self._last_evict < _EVICT_INTERVAL:
            return
        self._last_evict = now
        cutoff = now - settings.rate_limit_window
        stale = [ip for ip, hits in self._buckets.items() if not hits or hits[-1] < cutoff]
        for ip in stale:
            del self._buckets[ip]

    async def dispatch(self, request: Request, call_next) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - settings.rate_limit_window

        if len(self._buckets) > _MAX_BUCKETS:
            self._evict_stale(now)

        hits = self._buckets.get(client_ip)
        if hits is None:
            hits = deque()
            self._buckets[client_ip] = hits

        while hits and hits[0] <= window_start:
            hits.popleft()

        if len(hits) >= settings.rate_limit_max:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
            )

        hits.append(now)
        self._evict_stale(now)
        return await call_next(request)
