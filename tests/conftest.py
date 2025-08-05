import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    """
    Create a TestClient for the FastAPI app.
    This client can be used to make requests to the app in tests.
    """
    with TestClient(app) as c:
        yield c
