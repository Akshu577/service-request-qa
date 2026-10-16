# Test Plan

## What I'm testing
The Public Service Request Portal: the submit form, the tracking page and the REST API behind them (`app/app.py`).

## In scope
- Functional testing of every requirement in [requirements.md](requirements.md)
- API testing (pytest + requests, and a Postman collection run with Newman)
- UI testing in a real browser (Playwright, Chromium)
- Negative and boundary testing: missing fields, wrong formats, 9/10/11-digit phones, invalid status changes
- Access control: officer token checks
- Data privacy: masking of the citizenship number
- A basic response-time check

## Out of scope
- Real load or stress testing (only a 50-request timing check)
- Cross-browser testing beyond Chromium
- Security testing beyond the token check (e.g. no penetration testing)
- Persistence: the app keeps data in memory on purpose

## Approach
1. Write test cases from the requirements before running anything ([test-cases.md](test-cases.md)).
2. Map every requirement to at least one test ([traceability-matrix.md](traceability-matrix.md)).
3. Automate the tests so the whole suite re-runs with one command. This is the regression suite.
4. Log each failure as a bug with steps, expected vs actual result, evidence and severity ([bugs/](bugs/)).
5. Mark known bugs in the code with `xfail(strict=True)` and the bug ID. The run stays green, the bug stays visible, and as soon as a fix lands the test "unexpectedly passes" and tells me to retest and close the bug.
6. Retest fixes and update the bug report and test summary.

## Severity scale
| Severity | Meaning |
|---|---|
| Critical | Data loss, or the main flow is blocked for everyone |
| High | A business rule or privacy rule is broken |
| Medium | Wrong behaviour with a workaround, or bad data gets in |
| Low | Cosmetic or wording |

## Entry and exit criteria
- **Start:** requirements agreed, app runs locally.
- **Finish:** every requirement has a test, all tests have run, every failure is logged as a bug, and High bugs are fixed or explicitly accepted.

## Test data
Made-up names and numbers only. No real citizenship or phone numbers.
