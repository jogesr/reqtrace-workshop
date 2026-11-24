"""Traceability zwischen Anforderungen und Testfällen (APP-04, APP-08)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from reqtrace.models import Requirement, TestCaseSpec


@dataclass
class TraceRow:
    requirement: Requirement
    testcases: List[TestCaseSpec]

    @property
    def status(self) -> str:
        """Zusammenfassung über alle verknüpften Testfälle."""
        if not self.testcases:
            return "kein Testfall"
        results = {tc.last_result for tc in self.testcases}
        if "failed" in results:
            return "failed"
        if "blocked" in results:
            return "blocked"
        if results == {"passed"}:
            return "passed"
        return "offen"

    def to_dict(self) -> dict:
        return {
            "requirement": self.requirement.to_dict(),
            "testcases": [
                {"id": tc.id, "title": tc.title, "last_result": tc.last_result}
                for tc in self.testcases
            ],
            "status": self.status,
        }


def testcases_by_requirement(testcases: List[TestCaseSpec]) -> Dict[str, List[TestCaseSpec]]:
    mapping: Dict[str, List[TestCaseSpec]] = {}
    for tc in testcases:
        for rid in tc.requirement_ids:
            mapping.setdefault(rid, []).append(tc)
    return mapping


def build_trace(requirements: List[Requirement], testcases: List[TestCaseSpec]) -> List[TraceRow]:
    mapping = testcases_by_requirement(testcases)
    rows = [TraceRow(req, sorted(mapping.get(req.id, []), key=lambda t: t.id)) for req in requirements]
    return sorted(rows, key=lambda row: row.requirement.id)


def coverage_summary(requirements: List[Requirement], testcases: List[TestCaseSpec]) -> dict:
    """Abdeckung gemäss APP-08: Anteil der Anforderungen mit mindestens einem bestandenen Testfall."""
    rows = build_trace(requirements, testcases)
    total = len(rows)
    covered = sum(1 for row in rows if any(tc.last_result == "passed" for tc in row.testcases))
    percent = round(100.0 * covered / total, 1) if total else 0.0
    return {"total": total, "covered": covered, "percent": percent}
