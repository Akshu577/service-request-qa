# Requirements Traceability Matrix

Every requirement is covered by at least one test, and every failing test is linked to a bug.

| Requirement | Test cases | Result | Bug |
|---|---|---|---|
| REQ-01 Submit a request | TC-01, TC-02, TC-06, TC-16, TC-17, PM | ✅ Pass | |
| REQ-02 Input formats | TC-03, TC-05, TC-05b | ✅ Pass | |
| REQ-03 Valid mobile number | TC-04a, TC-04b, TC-18, PM | ✅ Pass after fix | [BUG-001](bugs/BUG-001.md) (closed) |
| REQ-04 Unique tracking ID | TC-01, TC-14, TC-16 | ✅ Pass | |
| REQ-05 Track a request | TC-07, TC-08, TC-19, TC-21, PM | ✅ Pass | |
| REQ-06 Status rules | TC-10, TC-11, TC-12, TC-13, TC-15, PM | ❌ Fail (final status can change) | [BUG-002](bugs/BUG-002.md) |
| REQ-07 Officer-only changes | TC-09, PM | ✅ Pass | |
| REQ-08 Protect personal data | TC-07, TC-20 | ❌ Fail (web page) | [BUG-003](bugs/BUG-003.md) |
| REQ-09 Response time | TC-22, PM | ✅ Pass | |
