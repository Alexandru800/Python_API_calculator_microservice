from fastapi import APIRouter, Depends, Query
from typing import List, Optional, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from app.database.db_connection import get_db
from app.models.calculation_model import Request
from app.schemas.calculation_schema import CalculationResponse

router = APIRouter()


@router.get(
    "/",
    response_model=List[CalculationResponse],
    tags=["Logs"],
    summary="Retrieve up to 300 logged API calls.")
def get_logs(
    db: Session = Depends(get_db),
    operation: Optional[str] = Query(
        None,
        description="Filter by operation (e.g. 'factorial', "
                    "'fibonacci' or 'power')"
    ),
    status: Optional[str] = Query(
        None,
        description="Filter by status (e.g. 'success' or 'error')"
    ),
    limit: int = Query(
        300,
        le=300,
        description="Maximum number of rows to return (max 300)"
    ),
):
    """
    Returns the most recent logged API calls,
    optionally filtered by operation and status.
    Requires an `X-API-Key` header.
    """
    query = db.query(Request).order_by(
        desc(cast(ColumnElement, Request.timestamp))
    )

    if operation:
        query = query.filter_by(operation=operation)
    if status:
        query = query.filter_by(status=status)

    results = query.limit(limit).all()
    return results
