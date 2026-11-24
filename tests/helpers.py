"""Gemeinsame Hilfsfunktionen für die Tests.

Jeder Test arbeitet auf einer frischen Kopie der Seed-Daten in einem
temporären Verzeichnis, damit data/work/ unverändert bleibt.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from reqtrace import storage


class IsolatedDataTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self._tmp.name)
        for name in (storage.REQUIREMENTS_FILE, storage.TESTCASES_FILE):
            shutil.copyfile(storage.SEED_DIR / name, self.data_dir / name)
        self._old_env = os.environ.get("REQTRACE_DATA_DIR")
        os.environ["REQTRACE_DATA_DIR"] = str(self.data_dir)

    def tearDown(self) -> None:
        if self._old_env is None:
            os.environ.pop("REQTRACE_DATA_DIR", None)
        else:
            os.environ["REQTRACE_DATA_DIR"] = self._old_env
        self._tmp.cleanup()


def make_requirement_dict(**overrides) -> dict:
    data = {
        "id": "REQ-100",
        "title": "Testanforderung",
        "text": "Synthetischer Text.",
        "priority": "mittel",
        "status": "freigegeben",
    }
    data.update(overrides)
    return data


def make_testcase_dict(**overrides) -> dict:
    data = {
        "id": "TC-100",
        "title": "Testfall",
        "steps": ["Schritt 1"],
        "expected": "Erwartetes Ergebnis",
        "requirement_ids": ["REQ-100"],
    }
    data.update(overrides)
    return data
