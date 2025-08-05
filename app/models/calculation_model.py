"""
SQLAlchemy ORM model for persisting every API request.

Table name: requests
Columns:
    id          – Primary key, auto-increment
    operation   – Name of the math operation (factorial, fibonacci, power)
    input       – JSON payload received from the client
    result      – Numeric result of the operation (stored as FLOAT)
    timestamp   – UTC datetime when the request was processed
"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.types import JSON

from app.database.db_connection import Base


class Request(Base):
    """ORM model representing a single logged API request."""
    __tablename__ = "requests"

    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    operation: str = Column(String, nullable=False, index=True)
    # Uses SQLite JSON extension
    input: dict = Column(JSON, nullable=False)
    result: float = Column(Float, nullable=True)
    # Stores factorial/Fibonacci/power result
    timestamp: datetime = Column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    # Stores the status of the request (e.g., 'success', 'error')
    status: str = Column(String, nullable=False)
    # Optional message for errors or additional info
    message: str = Column(String, nullable=True)

    # Optional, but useful when inspecting objects in logs / debugger
    def __repr__(self) -> str:  # pragma: no cover
        # Shorten message for failed calls to keep repr manageable
        msg = (self.message[:40] + "…") \
            if self.message and len(self.message) > 43 \
            else self.message
        return (
            f"<Request(id={self.id}, op={self.operation}, "
            f"input={self.input}, result={self.result}, ts={self.timestamp}, "
            f"status={self.status}, message={msg})>"
        )
