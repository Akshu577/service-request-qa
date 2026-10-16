"""Public Service Request Portal: a small app I built to practise testing.

Citizens submit a service request and track it with a tracking ID.
Officers move requests through review using an API token.
Data is kept in memory, so it resets when the app restarts.
"""
import os
import re
import threading
from datetime import datetime

from flask import Flask, jsonify, render_template, request

DISTRICTS = [
    "Kathmandu", "Lalitpur", "Bhaktapur", "Morang", "Sunsari", "Jhapa",
    "Kaski", "Chitwan", "Rupandehi", "Banke", "Kailali", "Dhanusha",
]
SERVICES = [
    "Citizenship Copy", "Passport Recommendation", "Birth Registration", "Tax Clearance",
]
OFFICER_TOKEN = os.environ.get("OFFICER_TOKEN", "demo-officer-token")

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z .'-]{2,59}$")
CITIZENSHIP_RE = re.compile(r"^\d{2}-\d{2}-\d{2}-\d{5}$")
PHONE_RE = re.compile(r"^9[78]\d{8}$")

# Which status each status can move to. Approved and Rejected are final.
NEXT_STATUS = {
    "Submitted": {"In Review"},
    "In Review": {"Approved", "Rejected"},
    "Approved": set(),
    "Rejected": set(),
}

app = Flask(__name__)
_lock = threading.Lock()
_requests = {}
_counter = 0


def _now():
    return datetime.now().isoformat(timespec="seconds")


def mask_citizenship(number):
    """Hide everything except the last 4 digits, e.g. XX-XX-XX-X1234."""
    return re.sub(r"\d", "X", number[:-4]) + number[-4:]


def validate(data):
    errors = {}
    name = str(data.get("full_name", "")).strip()
    citizenship = str(data.get("citizenship_no", "")).strip()
    district = data.get("district")
    phone = str(data.get("phone", "")).strip()
    service = data.get("service_type")

    if not name:
        errors["full_name"] = "Full name is required."
    elif not NAME_RE.match(name):
        errors["full_name"] = "Full name must be 3-60 letters."

    if not citizenship:
        errors["citizenship_no"] = "Citizenship number is required."
    elif not CITIZENSHIP_RE.match(citizenship):
        errors["citizenship_no"] = "Citizenship number must look like 12-01-75-01234."

    if not district:
        errors["district"] = "District is required."
    elif district not in DISTRICTS:
        errors["district"] = "Choose a district from the list."

    if not phone:
        errors["phone"] = "Phone number is required."
    elif not PHONE_RE.match(phone):
        errors["phone"] = "Phone must be a 10-digit mobile number starting with 97 or 98."

    if not service:
        errors["service_type"] = "Service type is required."
    elif service not in SERVICES:
        errors["service_type"] = "Choose a service from the list."

    return errors


def public_view(r):
    return {
        "tracking_id": r["tracking_id"],
        "full_name": r["full_name"],
        "citizenship_no": mask_citizenship(r["citizenship_no"]),
        "district": r["district"],
        "service_type": r["service_type"],
        "status": r["status"],
        "rejection_reason": r.get("rejection_reason"),
        "submitted_at": r["submitted_at"],
        "history": r["history"],
    }


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.post("/api/requests")
def create_request():
    global _counter
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Request body must be JSON."), 400

    errors = validate(data)
    if errors:
        return jsonify(errors=errors), 422

    with _lock:
        _counter += 1
        tracking_id = f"SR-{datetime.now().year}-{_counter:05d}"
        r = {
            "tracking_id": tracking_id,
            "full_name": data["full_name"].strip(),
            "citizenship_no": data["citizenship_no"].strip(),
            "district": data["district"],
            "phone": data["phone"].strip(),
            "service_type": data["service_type"],
            "status": "Submitted",
            "submitted_at": _now(),
            "history": [{"status": "Submitted", "at": _now()}],
        }
        _requests[tracking_id] = r

    resp = jsonify(public_view(r))
    resp.headers["Location"] = f"/api/requests/{tracking_id}"
    return resp, 201


@app.get("/api/requests/<tracking_id>")
def get_request(tracking_id):
    r = _requests.get(tracking_id)
    if r is None:
        return jsonify(error="Request not found."), 404
    return jsonify(public_view(r))


@app.patch("/api/requests/<tracking_id>/status")
def update_status(tracking_id):
    if request.headers.get("Authorization") != f"Bearer {OFFICER_TOKEN}":
        return jsonify(error="Officer token missing or invalid."), 401

    r = _requests.get(tracking_id)
    if r is None:
        return jsonify(error="Request not found."), 404

    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    if new_status not in NEXT_STATUS:
        return jsonify(error="Unknown status."), 422

    allowed = NEXT_STATUS[r["status"]]
    if allowed and new_status not in allowed:
        return jsonify(error=f"Cannot move from {r['status']} to {new_status}."), 422

    reason = str(data.get("reason", "")).strip()
    if new_status == "Rejected" and not reason:
        return jsonify(error="A reason is required to reject a request."), 422

    with _lock:
        r["status"] = new_status
        if new_status == "Rejected":
            r["rejection_reason"] = reason
        r["history"].append({"status": new_status, "at": _now()})
    return jsonify(public_view(r))


@app.get("/")
def index():
    return render_template("index.html", districts=DISTRICTS, services=SERVICES)


@app.get("/track")
def track():
    tracking_id = request.args.get("id", "").strip()
    r = _requests.get(tracking_id) if tracking_id else None
    return render_template("track.html", tracking_id=tracking_id, r=r)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5055)))
