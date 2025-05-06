from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import crud
from app.db import get_db_session
from app.models.pydantic import (
    SummaryPayloadSchema,
    SummaryResponseSchema,
    SummarySchema,
    SummaryUpdatePayloadSchema,
)
from app.summarizer import generate_summary

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
) -> SummaryResponseSchema:
    summary_id = await crud.post(payload, db)

    background_tasks.add_task(generate_summary, summary_id, str(payload.url))

    response_object = {"id": summary_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(
    id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db_session)
) -> SummarySchema:
    summary = await crud.get(id, db)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_all_summaries(
    db: AsyncSession = Depends(get_db_session),
) -> List[SummarySchema]:
    return await crud.get_all(db)


@router.delete("/{id}/", response_model=SummaryResponseSchema)
async def delete_summary(
    id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db_session)
) -> SummaryResponseSchema:
    summary = await crud.get(id, db)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    await crud.delete(id, db)

    return summary


@router.put("/{id}/", response_model=SummarySchema)
async def update_summary(
    payload: SummaryUpdatePayloadSchema,
    id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db_session),
) -> SummarySchema:
    summary = await crud.put(id, payload, db)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary
