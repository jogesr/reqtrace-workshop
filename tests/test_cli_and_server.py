"""Integrationstests: CLI-Aufrufe und HTTP-API über einen echten lokalen Server."""

import contextlib
import io
import json
import threading
import unittest
import urllib.error
import urllib.request

from reqtrace import cli
from reqtrace.server import make_server
from tests.helpers import IsolatedDataTestCase


def run_cli(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = cli.main(list(args))
    return code, out.getvalue()


class CliTests(IsolatedDataTestCase):
    def test_list_shows_all_requirements(self):
        code, output = run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("REQ-001", output)
        self.assertIn("REQ-012", output)

    def test_list_filter_by_status(self):
        code, output = run_cli("list", "--status", "verworfen")
        self.assertEqual(code, 0)
        self.assertIn("REQ-011", output)
        self.assertNotIn("REQ-001", output)

    def test_show_unknown_requirement_returns_error(self):
        code, _ = run_cli("show", "REQ-999")
        self.assertEqual(code, 1)

    def test_coverage_output(self):
        code, output = run_cli("coverage")
        self.assertEqual(code, 0)
        self.assertIn("6 von 12", output)


class ServerTests(IsolatedDataTestCase):
    def setUp(self):
        super().setUp()
        self.httpd = make_server(port=0)  # freier Port
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as resp:
            return resp.status, resp.read().decode("utf-8")

    def test_requirements_endpoint(self):
        status, body = self.get("/api/requirements")
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)), 12)

    def test_trace_endpoint(self):
        status, body = self.get("/api/trace")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)[0]["requirement"]["id"], "REQ-001")

    def test_index_page(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("ReqTrace", body)

    def test_unknown_path_returns_404(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.get("/api/gibt-es-nicht")
        self.assertEqual(ctx.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
