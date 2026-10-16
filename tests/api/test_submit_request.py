"""API tests for submitting a request (REQ-01 to REQ-04)."""
import re

import pytest

from tests.conftest import BASE_URL, create_request, valid_payload

URL = f"{BASE_URL}/api/requests"


def test_tc01_valid_request_is_accepted(api):
    res = api.post(URL, json=valid_payload())
    assert res.status_code == 201
    body = res.json()
    assert re.fullmatch(r"SR-\d{4}-\d{5}", body["tracking_id"])
    assert body["status"] == "Submitted"
    assert res.headers["Location"] == f"/api/requests/{body['tracking_id']}"


@pytest.mark.parametrize("field", ["full_name", "citizenship_no", "district", "phone", "service_type"])
def test_tc02_missing_required_field_is_rejected(api, field):
    payload = valid_payload()
    del payload[field]
    res = api.post(URL, json=payload)
    assert res.status_code == 422
    assert field in res.json()["errors"]


@pytest.mark.parametrize("value", ["12-01-75-1234", "1201751234", "AB-01-75-01234", "12/01/75/01234"])
def test_tc03_invalid_citizenship_format_is_rejected(api, value):
    res = api.post(URL, json=valid_payload(citizenship_no=value))
    assert res.status_code == 422
    assert "citizenship_no" in res.json()["errors"]


@pytest.mark.parametrize("phone", ["9841234567", "9801234567", "9761234567"])
def test_tc04a_valid_phone_numbers_are_accepted(api, phone):
    res = api.post(URL, json=valid_payload(phone=phone))
    assert res.status_code == 201


@pytest.mark.parametrize(
    "phone",
    [
        pytest.param(
            "984123456", id="9-digits",
            marks=pytest.mark.xfail(strict=True, reason="BUG-001: 9-digit phone is accepted"),
        ),
        pytest.param("98412345678", id="11-digits"),
        pytest.param("9641234567", id="wrong-prefix-96"),
        pytest.param("01-4412345", id="landline"),
        pytest.param("98412abcde", id="letters"),
    ],
)
def test_tc04b_invalid_phone_numbers_are_rejected(api, phone):
    res = api.post(URL, json=valid_payload(phone=phone))
    assert res.status_code == 422, f"{phone} should be rejected"
    assert "phone" in res.json()["errors"]


@pytest.mark.parametrize(
    "field,value",
    [("district", "Gotham"), ("district", "morang"), ("service_type", "Driving Licence")],
)
def test_tc05_values_outside_the_list_are_rejected(api, field, value):
    res = api.post(URL, json=valid_payload(**{field: value}))
    assert res.status_code == 422
    assert field in res.json()["errors"]


@pytest.mark.parametrize("name", ["Al", "R2D2", "A" * 61])
def test_tc05b_invalid_names_are_rejected(api, name):
    res = api.post(URL, json=valid_payload(full_name=name))
    assert res.status_code == 422


def test_tc06_non_json_body_returns_400(api):
    res = api.post(URL, data="full_name=Sita", headers={"Content-Type": "text/plain"})
    assert res.status_code == 400


def test_tc14_each_request_gets_a_new_tracking_id(api):
    first = create_request(api)["tracking_id"]
    second = create_request(api)["tracking_id"]
    assert first != second
    assert int(second[-5:]) == int(first[-5:]) + 1
