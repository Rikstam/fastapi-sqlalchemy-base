import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import ping, summaries
from app.config import get_settings
from app.db import sessionmanager

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
    application.include_router(
        summaries.router, prefix="/summaries", tags=["summaries"]
    )

    return application


app = create_application()
