# Test Cases

Each test case is automated. The function name in the code starts with the test case ID (e.g. `test_tc04b_...`), so it's easy to find.

| ID | Requirement | Type | Test case | Expected result | Where |
|---|---|---|---|---|---|
| TC-01 | REQ-01, REQ-04 | API | Submit a valid request | 201, tracking ID `SR-YYYY-NNNNN`, status `Submitted`, `Location` header | `tests/api/test_submit_request.py` |
| TC-02 | REQ-01 | API, negative | Leave out each required field (5 cases) | 422 with an error for that field | same |
| TC-03 | REQ-02 | API, negative | Wrong citizenship formats: short, no dashes, letters, slashes | 422 | same |
| TC-04a | REQ-03 | API, boundary | Valid phones starting 984, 980, 976 | 201 | same |
| TC-04b | REQ-03 | API, boundary | 9 digits, 11 digits, prefix 96, landline, letters | 422 for each | same |
| TC-05 | REQ-02 | API, negative | District/service not in the list, wrong case ("morang") | 422 | same |
| TC-05b | REQ-02 | API, boundary | Name of 2 letters, with digits, 61 letters | 422 | same |
| TC-06 | REQ-01 | API, negative | Send a non-JSON body | 400 | same |
| TC-07 | REQ-05, REQ-08 | API | Track an existing request | 200, citizenship masked, no phone in the response | `tests/api/test_track_and_status.py` |
| TC-08 | REQ-05 | API, negative | Track an unknown ID | 404 | same |
| TC-09 | REQ-07 | API, security | Change status with no token, a wrong token, or a token without `Bearer` | 401, status unchanged | same |
| TC-10 | REQ-06 | API | Submitted → In Review → Approved | 200 each time, history has 3 steps | same |
| TC-11 | REQ-06 | API, negative | Submitted → Approved (skipping review) | 422 | same |
| TC-12 | REQ-06 | API, negative | Reject with no reason or a blank reason, then with a reason | 422, 422, then 200 with the reason saved | same |
| TC-13 | REQ-06 | API, negative | Try to change an Approved or Rejected request to any status (8 cases) | 422, status unchanged | same |
| TC-14 | REQ-04 | API | Submit two requests | Different IDs, second = first + 1 | `tests/api/test_submit_request.py` |
| TC-15 | REQ-06 | API, negative | Set an unknown status ("Done") | 422 | `tests/api/test_track_and_status.py` |
| TC-16 | REQ-01, REQ-04 | UI | Fill in and submit the form | Tracking ID shown | `tests/ui/test_portal_ui.py` |
| TC-17 | REQ-01 | UI, negative | Submit an empty form | An error under every field, no tracking ID | same |
| TC-18 | REQ-03 | UI, negative | Submit with phone "12345" | Phone error shown, no error on other fields | same |
| TC-19 | REQ-05 | UI | Submit, then click "Track your request" | Status shows `Submitted` | same |
| TC-20 | REQ-08 | UI, privacy | Open the tracking page for a request | Citizenship number masked | same |
| TC-21 | REQ-05 | UI, negative | Open the tracking page with an unknown ID | "No request found" message | same |
| TC-22 | REQ-09 | Performance | 50 tracking requests in a row | 95th percentile under 500 ms | `tests/perf/test_response_time.py` |
| PM-01 to PM-11 | REQ-01 to REQ-07 | API (Postman) | Smoke + end-to-end flow: submit, track, token check, review, reject-without-reason, approve | See the tests in each request | `postman/` |
