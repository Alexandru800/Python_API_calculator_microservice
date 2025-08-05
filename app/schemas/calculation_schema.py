"""
Pydantic models (schemas) used for request validation and response formatting.
Each request type has its own schema, and we return a common response schema
(without the auto-incremented database ID).
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


# 1. Request schemas
class FactorialRequest(BaseModel):
    """Payload for /factorial – non-negative integer n."""
    n: int = Field(..., description="Non-negative integer")


class FibonacciRequest(BaseModel):
    """Payload for /fibonacci – non-negative integer n."""
    n: int = Field(..., description="Non-negative integer")


class PowerRequest(BaseModel):
    """Payload for /power – float/int base and float/int exponent."""
    base: float = Field(..., description="Base number (float or int)")
    exponent: float = Field(..., description="Exponent (float or int)")


# 2. Response schema
class CalculationResponse(BaseModel):
    """
    Standard API response:
      • operation  – 'factorial', 'fibonacci', or 'power'
      • input      – original request payload as a dict
      • result     – numeric result (stored as FLOAT in DB)
      • timestamp  – UTC time when the calculation was processed
      • status     – "success" or "error"
      • message    – error explanation if status = "error"
    """
    operation: str
    input: Dict[str, Any]
    result: Optional[float] = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    status: str = "success"
    message: Optional[str] = None

    # Enables conversion from SQLAlchemy model instances
    # to Pydantic models when returning from endpoints
    model_config = ConfigDict(from_attributes=True)
