# Test Summary Report

**System under test:** Public Service Request Portal (`app/`)
**Environment:** local, Python 3.9 / 3.12 (CI), Chromium via Playwright, Newman 6

## Results

| Suite | Tool | Run | Passed | Known failures (xfail) | Failed |
|---|---|---|---|---|---|
| API | pytest + requests | 43 | 35 | 8 (BUG-002) | 0 |
| UI | Playwright | 6 | 5 | 1 (BUG-003) | 0 |
| Performance | pytest | 1 | 1 | 0 | 0 |
| API (Postman) | Newman | 11 requests, 23 assertions | 23 | 0 | 0 |

The tracking API answered in a median of **0.7 ms** (95th percentile **1.0 ms**) over 50 requests, well under the 500 ms target. That's on my laptop with no load, so it says nothing about behaviour under many users.

## Defects

| ID | Title | Severity | Status |
|---|---|---|---|
| [BUG-001](bugs/BUG-001.md) | 9-digit mobile number is accepted | Medium | ✅ Closed: fixed and retested |
| [BUG-002](bugs/BUG-002.md) | Approved or Rejected request can still be changed | High | ❌ Open |
| [BUG-003](bugs/BUG-003.md) | Tracking page shows the full citizenship number | High | ❌ Open |

## Requirements coverage
9 of 9 requirements have tests ([traceability matrix](traceability-matrix.md)). 7 pass, and 2 (REQ-06 and REQ-08) fail because of open High bugs.

## Recommendation
**Not ready for release.** Both open bugs are High: one lets a final decision be reversed, the other exposes citizens' citizenship numbers. Both should be fixed and retested before release. The rest of the system behaved as specified.
