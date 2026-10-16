"""A basic response-time check (REQ-09). Not a load test: 50 requests one after another."""
import statistics
import time

from tests.conftest import BASE_URL, create_request


def test_tc22_tracking_api_responds_quickly(api):
    tid = create_request(api)["tracking_id"]
    timings = []
    for _ in range(50):
        start = time.perf_counter()
        res = api.get(f"{BASE_URL}/api/requests/{tid}")
        timings.append((time.perf_counter() - start) * 1000)
        assert res.status_code == 200

    p95 = statistics.quantiles(timings, n=20)[18]
    print(f"\nmedian {statistics.median(timings):.1f} ms, p95 {p95:.1f} ms")
    assert p95 < 500
