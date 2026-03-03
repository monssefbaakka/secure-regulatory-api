from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


def problem_response(
    *,
    status: int,
    title: str,
    detail: str,
    instance: str,
    correlation_id: str | None = None,
    type_: str | None = None,
):
    return JSONResponse(
        status_code=status,
        content={
            "type": type_ or "about:blank",
            "title": title,
            "status": status,
            "detail": detail,
            "instance": instance,
            "correlation_id": correlation_id,
        },
    )


def register_exception_handlers(app):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        correlation_id = getattr(request.state, "correlation_id", None)

        logger.warning(
            "request_validation_failed",
            extra={
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method,
                "errors": exc.errors(),
            },
        )

        return problem_response(
            status=400,
            title="Invalid request payload",
            detail="Request body is malformed or does not match schema.",
            instance=str(request.url.path),
            correlation_id=correlation_id,
            type_="https://httpstatuses.com/400",
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
                "detail": exc.detail,
            },
        )

        return problem_response(
            status=exc.status_code,
            title="HTTP error",
            detail=str(exc.detail),
            instance=str(request.url.path),
            correlation_id=correlation_id,
            type_=f"https://httpstatuses.com/{exc.status_code}",
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
                "exception_type": exc.__class__.__name__,
            },
        )

        return problem_response(
            status=500,
            title="Internal server error",
            detail="An unexpected error occurred.",
            instance=str(request.url.path),
            correlation_id=correlation_id,
            type_="https://httpstatuses.com/500",
        )
