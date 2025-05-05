import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends

from app.config import get_settings, Settings
from app.models.sqlalchemy import Base  # Import the model

# SQLAlchemy setup
DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

app = FastAPI()

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

# Create tables after all models are imported
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#@app.on_event("startup")
#async def startup_event():
#    await init_db()

@app.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
