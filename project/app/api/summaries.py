from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import crud
from app.db import get_db_session
from app.models.pydantic import (
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummarySchema,
)

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema, db: AsyncSession = Depends(get_db_session)
) -> SummaryResponseSchema:
    summary_id = await crud.post(payload, db)

    response_object = {"id": summary_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(
    id: int, db: AsyncSession = Depends(get_db_session)
) -> SummarySchema:
    summary = await crud.get(id, db)

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries(db: AsyncSession = Depends(get_db_session)) -> List[SummarySchema]:
    return await crud.get_all(db)
