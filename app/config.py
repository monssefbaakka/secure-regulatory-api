from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    ALLOWED_API_KEYS: List[str]

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
