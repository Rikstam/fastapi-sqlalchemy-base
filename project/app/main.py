import logging
import sys
from fastapi import FastAPI
from app.db import sessionmanager
from contextlib import asynccontextmanager
from app.api import ping
from app.config import get_settings

settings = get_settings()
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG if settings.log_level == "DEBUG" else logging.INFO,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


def create_application() -> FastAPI:
    application = FastAPI(
        lifespan=lifespan,
        title=settings.project_name,
    )

    application.include_router(ping.router)

    return application


app = create_application()
