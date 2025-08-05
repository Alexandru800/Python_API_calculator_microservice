from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.openapi.models import SecuritySchemeType, APIKeyIn
from fastapi.openapi.utils import get_openapi
from fastapi.responses import PlainTextResponse

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator

from app.controllers import (
    factorial_controller,
    fibonacci_controller,
    power_controller,
    log_controller,
)
from app.database.db_connection import init_db
from app.core.app_config import DEBUG
from app.core.api_security import verify_api_key


# Lifespan handler
@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()  # Run DB setup at startup
    yield      # Control returns to FastAPI while app is running


# FastAPI app instance with custom metadata and lifespan
app = FastAPI(
    title="Math Operations Microservice",
    description="A minimal FastAPI-based microservice exposing factorial, "
                "Fibonacci, and power operations via API. "
                "Requests are logged with SQLite.",
    version="1.0.0",
    debug=DEBUG,
    lifespan=lifespan,
)


# Instrumentation for Prometheus metrics
instrum_prom = Instrumentator().instrument(app)


# Register Prometheus metrics endpoint
@app.get("/metrics",
         tags=["Metrics"],
         response_class=PlainTextResponse,
         include_in_schema=True,
         dependencies=[Depends(verify_api_key)])
# Endpoint to expose Prometheus metrics
def metrics():
    # This endpoint returns the latest metrics in Prometheus format.
    # It is protected by the API key dependency.
    return PlainTextResponse(
        generate_latest(instrum_prom.registry),
        media_type=CONTENT_TYPE_LATEST
    )


def custom_openapi():
    """
    Override FastAPI's default OpenAPI generator to add a global
    API‑Key header security scheme called 'APIKeyHeader'.
    """
    if app.openapi_schema:
        return app.openapi_schema

    # Generate the base schema first
    openapi_schema = get_openapi(
        title=app.title,                # type: ignore[attr-defined]
        version=app.version,            # type: ignore[attr-defined]
        description=app.description,    # type: ignore[attr-defined]
        routes=app.routes,
    )

    # 1. Define the security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "MathAPIKey": {
            "type": SecuritySchemeType.apiKey.value,
            "in": APIKeyIn.header.value,
            "name": "X-API-Key",
            "description": "All requests (Except the "
                           "health check) must include "
                           "an **X‑API‑Key** header "
                           "with your API key. ",
        }
    }

    # 2. Apply it globally so every route shows the lock icon
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if "security" in operation:
                operation["security"] = [{"MathAPIKey": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Health check endpoint
@app.get("/", tags=["Health"], summary="Health check")
def root():
    return {"status": "ok"}


# Route registrations with API key dependency
app.include_router(log_controller.router,
                   prefix="/logs",
                   dependencies=[Depends(verify_api_key)])
app.include_router(factorial_controller.router,
                   prefix="/factorial",
                   tags=["Math"],
                   dependencies=[Depends(verify_api_key)])
app.include_router(fibonacci_controller.router,
                   prefix="/fibonacci",
                   tags=["Math"],
                   dependencies=[Depends(verify_api_key)])
app.include_router(power_controller.router,
                   prefix="/power",
                   tags=["Math"],
                   dependencies=[Depends(verify_api_key)])

# Tell FastAPI to use this custom generator
app.openapi = custom_openapi
