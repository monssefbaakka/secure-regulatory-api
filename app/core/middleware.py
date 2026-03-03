from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import Response
import uuid
import logging


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Generates a correlation ID for each request, logs safely, and adds security headers.
    """

    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id

        logging.info(
            f"[{correlation_id}] Incoming request: {request.method} {request.url}"
        )

        response: Response = await call_next(request)

        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response
