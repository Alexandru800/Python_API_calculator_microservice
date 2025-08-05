from app.core.app_config import API_KEY

headers = {"X-API-Key": API_KEY}


def test_fibonacci_valid(client):
    response = client.post("/fibonacci/", json={"n": 7}, headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 13


def test_fibonacci_zero(client):
    response = client.post("/fibonacci/", json={"n": 0}, headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 0


def test_fibonacci_too_large(client):
    response = client.post("/fibonacci/", json={"n": 1477}, headers=headers)
    assert response.status_code == 400


def test_fibonacci_negative(client):
    response = client.post("/fibonacci/", json={"n": -1}, headers=headers)
    assert response.status_code == 400


def test_fibonacci_invalid_type(client):
    response = client.post("/fibonacci/", json={"n": "abc"}, headers=headers)
    assert response.status_code == 422


def test_fibonacci_missing_api_key(client):
    response = client.post("/fibonacci/", json={"n": 5})  # No headers
    assert response.status_code == 401
    assert "Missing" in response.json()["detail"]


def test_fibonacci_wrong_api_key(client):
    bad_headers = {"X-API-Key": "wrong_key"}
    response = client.post("/fibonacci/", json={"n": 5}, headers=bad_headers)
    assert response.status_code == 403
    assert "Invalid" in response.json()["detail"]


def test_z_logs_include_fibonacci_success_and_error(client):
    response = client.get("/logs/", headers=headers)
    assert response.status_code == 200
    logs = response.json()

    # Check that at least one successful fibonacci log exists
    success_found = any(
        log["operation"] == "fibonacci" and
        log["input"] == {"n": 7} and
        log["result"] == 13 and
        log["status"] == "success"
        for log in logs
    )
    assert success_found, "Expected fibonacci(n=7) success log not found"

    # Check that a failed fibonacci request was logged (n negative)
    error_found = any(
        log["operation"] == "fibonacci" and
        log["input"] == {"n": -1} and
        log["status"] == "error"
        for log in logs
    )
    assert error_found, "Expected fibonacci(n=-1) error log not found"
