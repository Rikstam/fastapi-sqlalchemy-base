from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime


class SummaryPayloadSchema(BaseModel):
    url: AnyHttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummarySchema(BaseModel):
    id: int
    url: str
    summary: str
    created_at: datetime

    class Config:
        orm_mode = True  # This allows Pydantic to work with SQLAlchemy models


class SummaryUpdatePayloadSchema(BaseModel):
    url: AnyHttpUrl
    summary: str
