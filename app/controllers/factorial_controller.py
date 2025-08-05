from fastapi import APIRouter, HTTPException, status

from app.schemas.calculation_schema import (FactorialRequest,
                                            CalculationResponse)
from app.services.math_service import calculate_factorial

router = APIRouter()


@router.post(
    "/",
    response_model=CalculationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Compute factorial",
    description="Calculate n! for a non-negative integer n (n ≤ 170). "
                "Returns 400 if n is out of range."
                "Requires an `X-API-Key` header."
)
async def factorial_endpoint(req: FactorialRequest):
    try:
        result = calculate_factorial(req.n)
        return CalculationResponse(
            operation="factorial",
            input={"n": req.n},
            result=float(result),
            status="success",
            message="Factorial calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "operation": "factorial",
                "input": {"n": req.n},
                "result": None,
                "status": "error",
                "message": str(e),
            }
        )
