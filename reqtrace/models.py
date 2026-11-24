"""Datenmodelle und Validierung (siehe REQUIREMENTS.md, APP-02 und APP-03)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

REQ_ID_PATTERN = re.compile(r"^REQ-\d{3}$")
TC_ID_PATTERN = re.compile(r"^TC-\d{3}$")

REQ_STATUSES = ("entwurf", "freigegeben", "verworfen")
PRIORITIES = ("hoch", "mittel", "niedrig")
RESULTS = ("passed", "failed", "blocked", "not_run")


class ValidationError(ValueError):
    """Wird geworfen, wenn ein Datensatz nicht dem erwarteten Format entspricht."""


def _require(data: dict, key: str, context: str) -> str:
    value = data.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValidationError(f"{context}: Pflichtfeld '{key}' fehlt oder ist leer")
    return value


@dataclass(frozen=True)
class Requirement:
    id: str
    title: str
    text: str
    priority: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "Requirement":
        req_id = _require(data, "id", "Anforderung")
        if not REQ_ID_PATTERN.match(req_id):
            raise ValidationError(
                f"Ungültige Anforderungs-ID '{req_id}' (erwartet: REQ- gefolgt von 3 Ziffern)"
            )
        priority = _require(data, "priority", req_id)
        if priority not in PRIORITIES:
            raise ValidationError(f"{req_id}: unbekannte Priorität '{priority}'")
        status = _require(data, "status", req_id)
        if status not in REQ_STATUSES:
            raise ValidationError(f"{req_id}: unbekannter Status '{status}'")
        return cls(
            id=req_id,
            title=_require(data, "title", req_id),
            text=_require(data, "text", req_id),
            priority=priority,
            status=status,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "priority": self.priority,
            "status": self.status,
        }


@dataclass
class TestCaseSpec:
    """Ein Testfall. Heisst bewusst nicht 'TestCase', um Verwechslungen mit unittest zu vermeiden."""

    __test__ = False  # verhindert, dass pytest diese Klasse als Testklasse einsammelt

    id: str
    title: str
    steps: List[str]
    expected: str
    requirement_ids: List[str]
    last_result: str = "not_run"
    last_run: Optional[str] = None
    tester: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "TestCaseSpec":
        tc_id = _require(data, "id", "Testfall")
        if not TC_ID_PATTERN.match(tc_id):
            raise ValidationError(
                f"Ungültige Testfall-ID '{tc_id}' (erwartet: TC- gefolgt von 3 Ziffern)"
            )
        req_ids = data.get("requirement_ids") or []
        for rid in req_ids:
            if not REQ_ID_PATTERN.match(rid):
                raise ValidationError(f"{tc_id}: ungültige Anforderungs-Referenz '{rid}'")
        last_result = data.get("last_result", "not_run")
        if last_result not in RESULTS:
            raise ValidationError(f"{tc_id}: unbekanntes Ergebnis '{last_result}'")
        return cls(
            id=tc_id,
            title=_require(data, "title", tc_id),
            steps=list(data.get("steps") or []),
            expected=_require(data, "expected", tc_id),
            requirement_ids=list(req_ids),
            last_result=last_result,
            last_run=data.get("last_run"),
            tester=data.get("tester"),
            notes=list(data.get("notes") or []),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "steps": list(self.steps),
            "expected": self.expected,
            "requirement_ids": list(self.requirement_ids),
            "last_result": self.last_result,
            "last_run": self.last_run,
            "tester": self.tester,
            "notes": list(self.notes),
        }
