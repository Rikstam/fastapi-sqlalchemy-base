from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import crud
from app.db import get_db_session
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema

router = APIRouter()


@router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: SummaryPayloadSchema, db: AsyncSession = Depends(get_db_session)
) -> SummaryResponseSchema:
    summary_id = await crud.post(payload, db)

    response_object = {"id": summary_id, "url": payload.url}
    return response_object
