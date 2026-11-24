"""Laden und Speichern der JSON-Daten.

Arbeitsdaten liegen in data/work/ und werden beim ersten Zugriff aus data/seed/
erzeugt. Mit `python tools/reset_workshop.py` lässt sich der Ausgangszustand
wiederherstellen. Über die Umgebungsvariable REQTRACE_DATA_DIR kann (z.B. in
Tests) ein anderes Verzeichnis verwendet werden.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import List

from reqtrace.models import Requirement, TestCaseSpec, ValidationError

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEED_DIR = PROJECT_ROOT / "data" / "seed"
DEFAULT_WORK_DIR = PROJECT_ROOT / "data" / "work"

REQUIREMENTS_FILE = "requirements.json"
TESTCASES_FILE = "testcases.json"


def data_dir() -> Path:
    """Liefert das Arbeitsverzeichnis und legt es bei Bedarf aus den Seed-Daten an."""
    override = os.environ.get("REQTRACE_DATA_DIR")
    target = Path(override) if override else DEFAULT_WORK_DIR
    if not (target / REQUIREMENTS_FILE).exists():
        target.mkdir(parents=True, exist_ok=True)
        for name in (REQUIREMENTS_FILE, TESTCASES_FILE):
            shutil.copyfile(SEED_DIR / name, target / name)
    return target


def _read_json(path: Path) -> list:
    with path.open(encoding="utf-8") as fh:
        content = json.load(fh)
    if not isinstance(content, list):
        raise ValidationError(f"{path.name}: erwartet wird eine JSON-Liste")
    return content


def load_requirements(directory: Path = None) -> List[Requirement]:
    directory = directory or data_dir()
    items = [Requirement.from_dict(d) for d in _read_json(directory / REQUIREMENTS_FILE)]
    ids = [r.id for r in items]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        raise ValidationError(f"Doppelte Anforderungs-IDs: {', '.join(duplicates)}")
    return items


def load_testcases(directory: Path = None) -> List[TestCaseSpec]:
    directory = directory or data_dir()
    return [TestCaseSpec.from_dict(d) for d in _read_json(directory / TESTCASES_FILE)]


def save_testcases(testcases: List[TestCaseSpec], directory: Path = None) -> None:
    directory = directory or data_dir()
    path = directory / TESTCASES_FILE
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump([tc.to_dict() for tc in testcases], fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    tmp.replace(path)
