from fastapi import APIRouter, HTTPException, status
from app.schemas.calculation_schema import (PowerRequest,
                                            CalculationResponse)
from app.services.math_service import calculate_power

router = APIRouter()


@router.post(
    "/",
    response_model=CalculationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Compute power",
    description="Calculate baseⁿ where base is a float (or int) "
                "and exponent is an integer (or float, and can be negative)."
                "Requires an `X-API-Key` header."
)
async def power_endpoint(req: PowerRequest):
    try:
        result = calculate_power(req.base, req.exponent)
        return CalculationResponse(
            operation="power",
            input={"base": req.base, "exponent": req.exponent},
            result=result,
            status="success",
            message="Power calculated successfully"
        )
    except ValueError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "operation": "power",
                "input": {"base": req.base, "exponent": req.exponent},
                "result": None,
                "status": "error",
                "message": str(e),
            }
        )
