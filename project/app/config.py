import logging
from functools import lru_cache
from pydantic import AnyUrl
from pydantic_settings import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: AnyUrl = None
    project_name: str = "My FastAPI project"
    log_level: str = "DEBUG"
    echo_sql: bool = bool(0)

@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
