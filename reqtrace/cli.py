"""Kommandozeile für ReqTrace.

Beispiele:
    python -m reqtrace list
    python -m reqtrace show REQ-003
    python -m reqtrace testcases
    python -m reqtrace trace
    python -m reqtrace coverage
    python -m reqtrace import-results data/sample_results.csv
    python -m reqtrace serve --port 8000
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from reqtrace import storage
from reqtrace.importer import import_results
from reqtrace.models import ValidationError
from reqtrace.trace import build_trace, coverage_summary

LOG_DIR = storage.PROJECT_ROOT / "logs"


def _setup_logging(verbose: bool) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    handlers = [logging.FileHandler(LOG_DIR / "reqtrace.log", encoding="utf-8")]
    if verbose:
        handlers.append(logging.StreamHandler(sys.stderr))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )


def _print_table(headers: List[str], rows: List[List[str]]) -> None:
    widths = [len(h) for h in headers]
    for row in rows:
        widths = [max(w, len(str(cell))) for w, cell in zip(widths, row)]
    fmt = "  ".join("{:<%d}" % w for w in widths)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * w for w in widths]))
    for row in rows:
        print(fmt.format(*[str(c) for c in row]))


def cmd_list(args: argparse.Namespace) -> int:
    reqs = storage.load_requirements()
    if args.status:
        reqs = [r for r in reqs if r.status == args.status]
    _print_table(
        ["ID", "Priorität", "Status", "Titel"],
        [[r.id, r.priority, r.status, r.title] for r in sorted(reqs, key=lambda r: r.id)],
    )
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    reqs = {r.id: r for r in storage.load_requirements()}
    req = reqs.get(args.id)
    if req is None:
        print(f"Anforderung {args.id} nicht gefunden", file=sys.stderr)
        return 1
    print(f"{req.id} – {req.title}")
    print(f"Priorität: {req.priority} | Status: {req.status}")
    print()
    print(req.text)
    return 0


def cmd_testcases(args: argparse.Namespace) -> int:
    tcs = storage.load_testcases()
    _print_table(
        ["ID", "Ergebnis", "Anforderungen", "Titel"],
        [[t.id, t.last_result, ",".join(t.requirement_ids), t.title] for t in tcs],
    )
    return 0


def cmd_trace(args: argparse.Namespace) -> int:
    rows = build_trace(storage.load_requirements(), storage.load_testcases())
    _print_table(
        ["Anforderung", "Status", "Testfälle"],
        [[r.requirement.id, r.status, ", ".join(t.id for t in r.testcases) or "-"] for r in rows],
    )
    return 0


def cmd_coverage(args: argparse.Namespace) -> int:
    summary = coverage_summary(storage.load_requirements(), storage.load_testcases())
    print(f"Abdeckung: {summary['covered']} von {summary['total']} Anforderungen ({summary['percent']} %)")
    return 0


def cmd_import_results(args: argparse.Namespace) -> int:
    testcases = storage.load_testcases()
    report = import_results(Path(args.csv), testcases)
    storage.save_testcases(testcases)
    print(report.summary())
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    from reqtrace.server import run_server

    run_server(port=args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reqtrace", description="ReqTrace – Workshop-App (synthetische Daten)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Log-Ausgabe zusätzlich auf stderr")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list", help="Anforderungen auflisten (APP-01)")
    p.add_argument("--status", choices=["entwurf", "freigegeben", "verworfen"])
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="Eine Anforderung anzeigen")
    p.add_argument("id")
    p.set_defaults(func=cmd_show)

    sub.add_parser("testcases", help="Testfälle auflisten (APP-03)").set_defaults(func=cmd_testcases)
    sub.add_parser("trace", help="Traceability-Matrix (APP-04)").set_defaults(func=cmd_trace)
    sub.add_parser("coverage", help="Abdeckung berechnen (APP-08)").set_defaults(func=cmd_coverage)

    p = sub.add_parser("import-results", help="Testergebnisse aus CSV importieren (APP-06)")
    p.add_argument("csv")
    p.set_defaults(func=cmd_import_results)

    p = sub.add_parser("serve", help="Lokale Weboberfläche starten (nur 127.0.0.1)")
    p.add_argument("--port", type=int, default=8000)
    p.set_defaults(func=cmd_serve)
    return parser


def _force_utf8_output() -> None:
    """Umlaute auch bei umgeleiteter Ausgabe (z.B. durch Claude Code) korrekt ausgeben."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main(argv: Optional[List[str]] = None) -> int:
    _force_utf8_output()
    args = build_parser().parse_args(argv)
    _setup_logging(args.verbose)
    try:
        return args.func(args)
    except ValidationError as exc:
        print(f"Datenfehler: {exc}", file=sys.stderr)
        return 2
