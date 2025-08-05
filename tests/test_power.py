from app.core.app_config import API_KEY

headers = {"X-API-Key": API_KEY}


def test_power_valid_int(client):
    response = client.post("/power/",
                           json={"base": 2, "exponent": 3},
                           headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 8


def test_power_valid_float(client):
    response = client.post("/power/",
                           json={"base": 2.5, "exponent": 2},
                           headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 6.25


def test_power_zero_exponent(client):
    response = client.post("/power/",
                           json={"base": 5, "exponent": 0},
                           headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 1


def test_power_zero_base(client):
    response = client.post("/power/",
                           json={"base": 0, "exponent": 5},
                           headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 0


def test_power_negative_exponent(client):
    response = client.post("/power/",
                           json={"base": 2, "exponent": -2},
                           headers=headers)
    assert response.status_code == 201
    assert response.json()["result"] == 0.25


def test_power_invalid_type(client):
    response = client.post("/power/",
                           json={"base": "a", "exponent": 2},
                           headers=headers)
    assert response.status_code == 422
    response = client.post("/power/",
                           json={"base": 2, "exponent": "b"},
                           headers=headers)
    assert response.status_code == 422


def test_power_overflow(client):
    response = client.post("/power/",
                           json={"base": 1e+308, "exponent": 2},
                           headers=headers)
    assert response.status_code == 400
    assert "overflows" in response.json()["detail"]["message"]


def test_power_missing_api_key(client):
    response = client.post("/power/",
                           json={"base": 2, "exponent": 3})
    assert response.status_code == 401
    assert "Missing" in response.json()["detail"]


def test_power_wrong_api_key(client):
    bad_headers = {"X-API-Key": "wrong_key"}
    response = client.post("/power/",
                           json={"base": 2, "exponent": 3},
                           headers=bad_headers)
    assert response.status_code == 403
    assert "Invalid" in response.json()["detail"]


def test_z_logs_include_power_success_and_error(client):
    response = client.get("/logs/", headers=headers)
    assert response.status_code == 200
    logs = response.json()

    # Check that at least one successful power log exists
    success_found = any(
        log["operation"] == "power" and
        log["input"] == {"base": 2, "exponent": 3} and
        log["result"] == 8 and
        log["status"] == "success"
        for log in logs
    )
    assert success_found, ("Expected power(base=2, exponent=3)"
                           " success log not found")

    # Check that a failed power request was logged (overflow)
    error_found = any(
        log["operation"] == "power" and
        log["input"] == {"base": 1e308, "exponent": 2} and
        log["status"] == "error"
        for log in logs
    )
    assert error_found, ("Expected power overflow "
                         "error log not found")
