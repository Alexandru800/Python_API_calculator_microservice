from app.core.app_config import API_KEY

headers = {"X-API-Key": API_KEY}


def test_factorial_valid(client):
    response = client.post("/factorial/", json={"n": 5}, headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 120


def test_factorial_zero(client):
    response = client.post("/factorial/", json={"n": 0}, headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 1


def test_factorial_too_large(client):
    response = client.post("/factorial/", json={"n": 171}, headers=headers)
    assert response.status_code == 400


def test_factorial_negative(client):
    response = client.post("/factorial/", json={"n": -1}, headers=headers)
    assert response.status_code == 400


def test_factorial_invalid_type(client):
    response = client.post("/factorial/", json={"n": "abc"}, headers=headers)
    assert response.status_code == 422


def test_factorial_missing_api_key(client):
    response = client.post("/factorial/", json={"n": 5})  # No headers
    assert response.status_code == 401
    assert "Missing" in response.json()["detail"]


def test_factorial_wrong_api_key(client):
    bad_headers = {"X-API-Key": "wrong_key"}
    response = client.post("/factorial/", json={"n": 5}, headers=bad_headers)
    assert response.status_code == 403
    assert "Invalid" in response.json()["detail"]


# This will run last if kept at the bottom and named accordingly
def test_z_logs_include_factorial_success_and_error(client):
    response = client.get("/logs/", headers=headers)
    assert response.status_code == 200
    logs = response.json()

    # Check that at least one successful factorial log exists
    success_found = any(
        log["operation"] == "factorial" and
        log["input"] == {"n": 5} and
        log["result"] == 120 and
        log["status"] == "success"
        for log in logs
    )
    assert success_found, "Expected factorial(n=5) success log not found"

    # Check that a failed factorial request was logged (n too large)
    error_found = any(
        log["operation"] == "factorial" and
        log["input"] == {"n": 171} and
        log["status"] == "error"
        for log in logs
    )
    assert error_found, "Expected factorial(n=171) error log not found"
