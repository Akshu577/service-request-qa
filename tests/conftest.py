import threading

import pytest
import requests
from werkzeug.serving import make_server

from app.app import app

HOST, PORT = "127.0.0.1", 5055
BASE_URL = f"http://{HOST}:{PORT}"
OFFICER_HEADERS = {"Authorization": "Bearer demo-officer-token"}


@pytest.fixture(scope="session", autouse=True)
def live_server():
    """Start the app once for the whole test run."""
    server = make_server(HOST, PORT, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield BASE_URL
    server.shutdown()


@pytest.fixture(scope="session")
def base_url():
    # Also used by pytest-playwright, so page.goto("/") works.
    return BASE_URL


@pytest.fixture
def api():
    with requests.Session() as s:
        yield s


def valid_payload(**overrides):
    payload = {
        "full_name": "Sita Sharma",
        "citizenship_no": "12-01-75-01234",
        "district": "Morang",
        "phone": "9841234567",
        "service_type": "Citizenship Copy",
    }
    payload.update(overrides)
    return payload


def create_request(api, **overrides):
    res = api.post(f"{BASE_URL}/api/requests", json=valid_payload(**overrides))
    assert res.status_code == 201, res.text
    return res.json()


def set_status(api, tracking_id, status, reason=None, headers=OFFICER_HEADERS):
    body = {"status": status}
    if reason is not None:
        body["reason"] = reason
    return api.patch(f"{BASE_URL}/api/requests/{tracking_id}/status", json=body, headers=headers)
