"""API tests for tracking (REQ-05, REQ-08) and status changes (REQ-06, REQ-07)."""
import pytest

from tests.conftest import BASE_URL, create_request, set_status


def test_tc07_track_existing_request_masks_citizenship(api):
    created = create_request(api, citizenship_no="27-02-70-05678")
    res = api.get(f"{BASE_URL}/api/requests/{created['tracking_id']}")
    assert res.status_code == 200
    body = res.json()
    assert body["citizenship_no"] == "XX-XX-XX-X5678"
    assert "phone" not in body


def test_tc08_unknown_tracking_id_returns_404(api):
    res = api.get(f"{BASE_URL}/api/requests/SR-1999-99999")
    assert res.status_code == 404


@pytest.mark.parametrize(
    "headers",
    [{}, {"Authorization": "Bearer wrong-token"}, {"Authorization": "demo-officer-token"}],
    ids=["no-token", "wrong-token", "missing-bearer"],
)
def test_tc09_status_change_needs_valid_officer_token(api, headers):
    created = create_request(api)
    res = set_status(api, created["tracking_id"], "In Review", headers=headers)
    assert res.status_code == 401
    # and nothing changed
    assert api.get(f"{BASE_URL}/api/requests/{created['tracking_id']}").json()["status"] == "Submitted"


def test_tc10_full_approval_flow(api):
    tid = create_request(api)["tracking_id"]
    assert set_status(api, tid, "In Review").status_code == 200
    res = set_status(api, tid, "Approved")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "Approved"
    assert [h["status"] for h in body["history"]] == ["Submitted", "In Review", "Approved"]


def test_tc11_cannot_skip_review(api):
    tid = create_request(api)["tracking_id"]
    res = set_status(api, tid, "Approved")
    assert res.status_code == 422


def test_tc12_rejection_needs_a_reason(api):
    tid = create_request(api)["tracking_id"]
    set_status(api, tid, "In Review")
    assert set_status(api, tid, "Rejected").status_code == 422
    assert set_status(api, tid, "Rejected", reason="   ").status_code == 422

    res = set_status(api, tid, "Rejected", reason="Document is unclear")
    assert res.status_code == 200
    assert res.json()["rejection_reason"] == "Document is unclear"


@pytest.mark.xfail(strict=True, reason="BUG-002: final status can still be changed")
@pytest.mark.parametrize("final_status", ["Approved", "Rejected"])
@pytest.mark.parametrize("new_status", ["Submitted", "In Review", "Approved", "Rejected"])
def test_tc13_final_status_cannot_change(api, final_status, new_status):
    tid = create_request(api)["tracking_id"]
    set_status(api, tid, "In Review")
    set_status(api, tid, final_status, reason="Not eligible")

    res = set_status(api, tid, new_status, reason="trying again")
    assert res.status_code == 422, f"{final_status} -> {new_status} should be blocked"
    assert api.get(f"{BASE_URL}/api/requests/{tid}").json()["status"] == final_status


def test_tc15_unknown_status_value_is_rejected(api):
    tid = create_request(api)["tracking_id"]
    assert set_status(api, tid, "Done").status_code == 422
