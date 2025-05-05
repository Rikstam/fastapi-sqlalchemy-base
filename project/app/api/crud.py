from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pydantic import SummaryPayloadSchema
from app.models.sqlalchemy import TextSummary


async def post(payload: SummaryPayloadSchema, db: AsyncSession) -> int:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    db.add(summary)
    await db.commit()
    await db.refresh(summary)  # To get the generated ID and other defaults
    return summary.id
