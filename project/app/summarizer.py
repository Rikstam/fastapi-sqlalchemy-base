import asyncio
import logging

import nltk
from newspaper import Article
from sqlalchemy import select

from app.db import sessionmanager  # Import your session manager
from app.models.sqlalchemy import TextSummary


async def generate_summary(summary_id: int, url: str) -> None:
    article = Article(url)
    article.download()
    article.parse()

    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab")
    finally:
        article.nlp()

    summary_text = article.summary

    async with sessionmanager.session() as db:
        result = await db.execute(
            select(TextSummary).where(TextSummary.id == summary_id)
        )
        summary = result.scalars().first()
        if summary:
            summary.summary = summary_text
            await db.commit()
            await db.refresh(summary)
