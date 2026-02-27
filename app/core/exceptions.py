from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)

def register_exception_handlers(app):
    """Register all API exception handlers."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        correlation_id = getattr(request.state, "correlation_id", None)

        logger.warning(
            "request_validation_failed",
            extra={
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method,
                "errors": exc.errors()
            }
        )

        return JSONResponse(
            status_code=400,
            content={
                "correlation_id": correlation_id,
                "error": "Invalid request payload",
                "details": exc.errors()
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        correlation_id = getattr(request.state, "correlation_id", None)

        logger.info(
            "http_exception",
            extra={
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method,
                "status_code": exc.status_code,
                "detail": exc.detail
            }
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "correlation_id": correlation_id,
                "error": exc.detail
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        correlation_id = getattr(request.state, "correlation_id", None)

        logger.exception(
            "unhandled_exception",
            extra={
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method,
                "exception_type": exc.__class__.__name__
            }
        )

        return JSONResponse(
            status_code=500,
            content={
                "correlation_id": correlation_id,
                "error": "Internal server error"
            },
        )