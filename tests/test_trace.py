import unittest

from reqtrace import storage
from reqtrace.trace import build_trace, coverage_summary
from tests.helpers import IsolatedDataTestCase


class TraceTests(IsolatedDataTestCase):
    def setUp(self):
        super().setUp()
        self.reqs = storage.load_requirements()
        self.tcs = storage.load_testcases()

    def test_trace_contains_every_requirement_sorted(self):
        rows = build_trace(self.reqs, self.tcs)
        self.assertEqual([r.requirement.id for r in rows], sorted(r.id for r in self.reqs))

    def test_failed_testcase_dominates_status(self):
        rows = {r.requirement.id: r for r in build_trace(self.reqs, self.tcs)}
        self.assertEqual(rows["REQ-003"].status, "failed")  # TC-003 failed, TC-009 passed

    def test_requirement_without_testcase(self):
        rows = {r.requirement.id: r for r in build_trace(self.reqs, self.tcs)}
        self.assertEqual(rows["REQ-007"].status, "kein Testfall")

    def test_coverage_summary_seed_data(self):
        summary = coverage_summary(self.reqs, self.tcs)
        self.assertEqual(summary, {"total": 12, "covered": 6, "percent": 50.0})


if __name__ == "__main__":
    unittest.main()
