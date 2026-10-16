# QA Testing: Public Service Request Portal

![Tests](https://github.com/Akshu577/service-request-qa/actions/workflows/tests.yml/badge.svg)

A complete QA project on a small government-style web app: citizens submit a service request (citizenship copy, passport recommendation and so on) and track it with a tracking ID, and officers move requests through review.

I wanted to practise the whole testing process, not just write a few automated tests. So I started from written requirements, designed test cases from them, automated the tests (API, browser and a basic performance check), logged the bugs I found with evidence, and fixed and retested one of them.

**Tools:** Python, pytest, Playwright, Postman / Newman, GitHub Actions, Flask (the app under test)

## What I found

The first full run had 10 failing checks out of 50, which came down to 3 bugs:

| Bug | Severity | Status |
|---|---|---|
| [BUG-001](docs/bugs/BUG-001.md): a 9-digit mobile number is accepted | Medium | ✅ Fixed and retested |
| [BUG-002](docs/bugs/BUG-002.md): an Approved or Rejected request can still be changed | High | ❌ Open |
| [BUG-003](docs/bugs/BUG-003.md): the tracking page shows the full citizenship number | High | ❌ Open |

The two I find most interesting:

- **BUG-002** came from one line: `if allowed and new_status not in allowed`. For a final status, `allowed` is an empty set, which Python treats as false, so the check is skipped completely. The happy-path tests all passed. Only testing *every* final status against *every* target status (8 cases) caught it.
- **BUG-003** is a privacy bug that only shows up in the browser. The API masks the citizenship number correctly (`XX-XX-XX-X5678`), but the web page reads the raw record. If I had only tested the API, I'd have missed it. Because tracking IDs are sequential, someone could walk through them and collect citizenship numbers.

Full results: [test summary report](docs/test-summary.md).

## How the project is organised

| Document | What it is |
|---|---|
| [Requirements](docs/requirements.md) | 9 requirements with acceptance criteria. I wrote these first. |
| [Test plan](docs/test-plan.md) | Scope, approach, severity scale, entry/exit criteria |
| [Test cases](docs/test-cases.md) | 22 test cases plus 11 Postman requests, each linked to a requirement |
| [Traceability matrix](docs/traceability-matrix.md) | Requirement → test cases → result → bug |
| [Bug reports](docs/bugs/) | Steps to reproduce, expected vs actual, evidence, likely cause, impact |
| [Test summary](docs/test-summary.md) | Results and a release recommendation |

```
app/                  the app under test (Flask)
tests/api/            API tests (pytest + requests)
tests/ui/             browser tests (Playwright)
tests/perf/           response-time check
postman/              Postman collection + environment
.github/workflows/    runs everything on every push
```

## How known bugs are handled

Tests for open bugs are marked `@pytest.mark.xfail(strict=True, reason="BUG-002: ...")`. That way:

- the run stays green, so a *new* failure stands out straight away,
- the bug is still visible in every test report, with its ID,
- when someone fixes the bug, `strict=True` turns the "expected failure" into an error (`XPASS`), which tells me to retest and close it. That's exactly what happened with BUG-001.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

pytest                      # API, UI and performance tests
pytest --headed tests/ui    # watch the browser tests run
```

Postman collection:

```bash
python -m app.app &         # start the app on http://127.0.0.1:5055
npm install -g newman
newman run postman/service-request-api.postman_collection.json -e postman/local.postman_environment.json
```

You can also import both files from `postman/` into the Postman app. The officer token for the demo is `demo-officer-token`.

## What I'd add next

- Fix and retest BUG-002 and BUG-003
- Non-sequential tracking IDs (see the note in BUG-003)
- A real load test with k6 or JMeter
- Firefox and WebKit runs, and an accessibility check with axe

All names and numbers in the tests are made up.
