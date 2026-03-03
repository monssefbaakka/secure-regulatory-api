from fastapi import FastAPI
from app.api.routes import router
from app.core.middleware import CorrelationIdMiddleware
from app.core.exceptions import register_exception_handlers
from app.config import settings
import logging

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = FastAPI(title="Validation API", version="1.0.0")
app.add_middleware(CorrelationIdMiddleware)
app.include_router(router)
register_exception_handlers(app)
