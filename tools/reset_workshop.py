"""Setzt die Arbeitsdaten auf den Ausgangszustand zurück.

    python tools/reset_workshop.py

- kopiert data/seed/*.json nach data/work/
- löscht logs/reqtrace.log
Code-Änderungen werden NICHT zurückgesetzt – dafür Git verwenden (siehe README).
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "data" / "seed"
WORK = ROOT / "data" / "work"
LOG = ROOT / "logs" / "reqtrace.log"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    WORK.mkdir(parents=True, exist_ok=True)
    for src in SEED.glob("*.json"):
        shutil.copyfile(src, WORK / src.name)
        print(f"zurückgesetzt: data/work/{src.name}")
    if LOG.exists():
        LOG.unlink()
        print("gelöscht: logs/reqtrace.log")
    print("Fertig. Code-Änderungen ggf. mit 'git restore .' bzw. 'git stash' zurücksetzen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
