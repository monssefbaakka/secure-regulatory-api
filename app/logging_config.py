import logging
from pythonjsonlogger import jsonlogger
from app.config import settings


def setup_logging(level=settings.LOG_LEVEL):
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    log_handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[log_handler])
