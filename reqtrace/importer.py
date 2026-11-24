"""Import von Testergebnissen aus CSV-Dateien (APP-06).

Erwartetes Format (Semikolon-getrennt, UTF-8, mit Kopfzeile):

    testcase_id;result;date;tester
    TC-001;passed;2026-11-02;Tester A
"""

from __future__ import annotations

import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from reqtrace.models import RESULTS, TestCaseSpec

log = logging.getLogger("reqtrace.importer")


@dataclass
class ImportReport:
    updated: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)

    def summary(self) -> str:
        return f"{len(self.updated)} Testfälle aktualisiert, {len(self.skipped)} Zeilen übersprungen"


def import_results(csv_path: Path, testcases: List[TestCaseSpec]) -> ImportReport:
    """Überträgt Ergebnisse aus der CSV-Datei auf die übergebenen Testfälle."""
    report = ImportReport()
    by_id = {tc.id: tc for tc in testcases}

    with Path(csv_path).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for line_no, row in enumerate(reader, start=2):
            tc_id = row["testcase_id"]
            result = (row.get("result") or "").strip().lower()
            if result not in RESULTS:
                log.warning("Zeile %d: unbekanntes Ergebnis '%s' – übersprungen", line_no, result)
                report.skipped.append(tc_id)
                continue

            tc = by_id[tc_id]
            tc.last_result = result
            tc.last_run = (row.get("date") or "").strip() or None
            tc.tester = (row.get("tester") or "").strip() or None
            report.updated.append(tc.id)
            log.info("Zeile %d: %s -> %s", line_no, tc.id, result)

    return report
