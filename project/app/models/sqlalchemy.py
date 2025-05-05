# project/app/models/sqlalchemy.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for declarative class definitions
Base = declarative_base()

class TextSummary(Base):
    __tablename__ = 'text_summary'  # Define the table name

    id = Column(Integer, primary_key=True, autoincrement=True)  # Add a primary key
    url = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return self.url