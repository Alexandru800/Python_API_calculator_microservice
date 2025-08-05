from fastapi import APIRouter, HTTPException, status
from app.schemas.calculation_schema import (FibonacciRequest,
                                            CalculationResponse)
from app.services.math_service import calculate_fibonacci

router = APIRouter()


@router.post(
    "/",
    response_model=CalculationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Compute Fibonacci",
    description="Return the n-th Fibonacci number for a non-negative integer "
                "n (n ≤ 1,476). Returns 400 if n is out of range."
                "Requires an `X-API-Key` header."
)
async def fibonacci_endpoint(req: FibonacciRequest):
    try:
        result = calculate_fibonacci(req.n)
        return CalculationResponse(
            operation="fibonacci",
            input={"n": req.n},
            result=float(result),
            status="success",
            message="Fibonacci number calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "operation": "fibonacci",
                "input": {"n": req.n},
                "result": None,
                "status": "error",
                "message": str(e),
            }
        )
