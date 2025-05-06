from typing import List, Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pydantic import SummaryPayloadSchema, SummaryUpdatePayloadSchema
from app.models.sqlalchemy import TextSummary


async def post(payload: SummaryPayloadSchema, db: AsyncSession) -> int:
    summary = TextSummary(
        url=str(payload.url),
        summary="",
    )
    db.add(summary)
    await db.commit()
    await db.refresh(summary)  # To get the generated ID and other defaults
    return summary.id


async def get(id: int, db: AsyncSession) -> Union[TextSummary, None]:
    result = await db.execute(select(TextSummary).where(TextSummary.id == id))
    summary = result.scalars().first()
    return summary


async def get_all(db: AsyncSession) -> List[TextSummary]:
    result = await db.execute(select(TextSummary))
    return result.scalars().all()


async def delete(id: int, db: AsyncSession) -> Optional[TextSummary]:
    summary = await get(id, db)
    if summary:
        await db.delete(summary)
        await db.commit()
    return summary


async def put(
    id: int, payload: SummaryUpdatePayloadSchema, db: AsyncSession
) -> Union[TextSummary, None]:
    # Fetch the existing summary
    result = await db.execute(select(TextSummary).where(TextSummary.id == id))
    summary = result.scalars().first()
    if not summary:
        return None

    # Update fields
    summary.url = str(payload.url)
    summary.summary = payload.summary

    await db.commit()
    await db.refresh(summary)
    return summary
