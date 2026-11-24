"""Minimale lokale Weboberfläche und JSON-API (nur Python-Standardbibliothek).

Bindet ausschliesslich an 127.0.0.1 (APP-11). Nicht für den Produktivbetrieb gedacht.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from reqtrace import storage
from reqtrace.trace import build_trace, coverage_summary

STATIC_DIR = Path(__file__).resolve().parent / "static"


def _api_requirements() -> list:
    return [r.to_dict() for r in storage.load_requirements()]


def _api_testcases() -> list:
    return [t.to_dict() for t in storage.load_testcases()]


def _api_trace() -> list:
    return [row.to_dict() for row in build_trace(storage.load_requirements(), storage.load_testcases())]


def _api_coverage() -> dict:
    return coverage_summary(storage.load_requirements(), storage.load_testcases())


API_ROUTES = {
    "/api/requirements": _api_requirements,
    "/api/testcases": _api_testcases,
    "/api/trace": _api_trace,
    "/api/coverage": _api_coverage,
}


class Handler(BaseHTTPRequestHandler):
    server_version = "ReqTrace/0.1"

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802 (Name von BaseHTTPRequestHandler vorgegeben)
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            body = (STATIC_DIR / "index.html").read_bytes()
            self._send(200, body, "text/html; charset=utf-8")
            return
        route = API_ROUTES.get(path)
        if route is None:
            self._send_json(404, {"error": f"Unbekannter Pfad: {path}"})
            return
        try:
            self._send_json(200, route())
        except Exception as exc:  # bewusst einfach gehalten für den Workshop
            self._send_json(500, {"error": str(exc)})

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        pass  # Konsole ruhig halten


def make_server(port: int = 8000) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def run_server(port: int = 8000) -> None:
    httpd = make_server(port)
    print(f"ReqTrace läuft auf http://127.0.0.1:{httpd.server_address[1]}/ (Abbrechen mit Ctrl+C)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
