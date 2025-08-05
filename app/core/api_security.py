from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from app.core.app_config import API_KEY

# Define the header name expected in each request
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> None:
    """
    Dependency that checks if the request includes a valid X-API-Key header.
    - Raises 401 if the header is missing.
    - Raises 403 if the header is present but incorrect.
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
            headers={"WWW-Authenticate": "API Key"},
        )

    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
