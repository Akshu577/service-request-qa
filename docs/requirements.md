# Requirements

These are the requirements I tested against. I wrote them first, the way a system analyst would hand them to a QA team, and then designed the tests from them.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| REQ-01 | A citizen can submit a service request. | Full name, citizenship number, district, mobile number and service type are all required. A missing field returns 422 with an error for that field. |
| REQ-02 | Input must be in the right format. | Name: 3–60 letters (spaces, `.`, `'` and `-` allowed). Citizenship number: `NN-NN-NN-NNNNN`. District and service: must be one from the list. |
| REQ-03 | Mobile number must be a valid Nepali mobile number. | Exactly 10 digits, starting with 97 or 98. Anything else returns 422. |
| REQ-04 | Each request gets a unique tracking ID. | Format `SR-YYYY-NNNNN`, increasing by one. New requests start as `Submitted`. |
| REQ-05 | A citizen can track a request by tracking ID. | Known ID: 200 with status. Unknown ID: 404 (API) or a "not found" message (web page). |
| REQ-06 | Officers move requests through review. | `Submitted → In Review → Approved` or `Rejected`. Skipping a step returns 422. **Approved and Rejected are final** and can't be changed. Rejecting needs a reason. Every change is recorded in the history. |
| REQ-07 | Only officers can change status. | Missing or wrong officer token returns 401, and the status doesn't change. |
| REQ-08 | Personal data is protected. | The citizenship number is masked everywhere it's shown (`XX-XX-XX-X1234`), on the API **and** the web page. The phone number is never shown. |
| REQ-09 | Tracking is fast. | `GET /api/requests/{id}` responds in under 500 ms (95th percentile) over 50 requests. |
