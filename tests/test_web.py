"""Tests: web app + WSGI — live server smoke tests (stdlib only)."""

import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nyayavault.agent import LegalAgent
from nyayavault.config import NyayaVaultConfig
from nyayavault.web import make_handler
from nyayavault.wsgi import application

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE, "corpus")
SAMPLES = os.path.join(BASE, "samples")


def _agent() -> LegalAgent:
    return LegalAgent(NyayaVaultConfig(corpus_root=CORPUS, mock_mode=True, daily_call_cap=10))


class TestWebServer(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = _agent()
        config = NyayaVaultConfig(corpus_root=CORPUS, mock_mode=True)
        handler = make_handler(self.agent, config, SAMPLES)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def _url(self, path: str) -> str:
        return f"http://127.0.0.1:{self.port}{path}"

    def _get(self, path: str):
        with urllib.request.urlopen(self._url(path), timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8")

    def _post(self, path: str, payload: dict):
        req = urllib.request.Request(
            self._url(path),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))

    def test_home_page_renders(self) -> None:
        status, body = self._get("/")
        self.assertEqual(status, 200)
        self.assertIn("NyayaVault", body)
        self.assertIn("Authority constellation", body)
        self.assertIn("not legal advice", body)
        self.assertIn("it-act-s66c.md", body)  # provisions embedded

    def test_status_reports_mock_and_seventeen(self) -> None:
        status, body = self._get("/api/status")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["mode"], "mock")
        self.assertEqual(data["notes_count"], 17)
        self.assertEqual(data["budget"]["limit"], 10)

    def test_ask_identity_theft(self) -> None:
        status, data = self._post("/api/ask", {"question": "Someone stole my password and used my account.", "language": "en"})
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertTrue(data["answer"].startswith("[mock]"))
        self.assertEqual(data["mode"], "mock")
        self.assertTrue(any(c["rel"] == "it-act-s66c.md" for c in data["citations"]))

    def test_ask_dpdp_refuses(self) -> None:
        status, data = self._post("/api/ask", {"question": "What does the DPDP Act 2023 say about a data breach?", "language": "en"})
        self.assertEqual(status, 200)
        self.assertFalse(data["ok"])
        self.assertIn("not in the NyayaVault corpus", data["error"])

    def test_document_endpoint(self) -> None:
        status, body = self._get("/api/document?path=it-act-s66c.md")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertIn("66C", data["title"])
        self.assertIn("password", data["body"])

    def test_document_missing_404(self) -> None:
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self._get("/api/document?path=nope.md")
        self.assertEqual(ctx.exception.code, 404)

    def test_brief_endpoint(self) -> None:
        status, data = self._post("/api/brief", {"question": "Someone stole my password and used my account.", "language": "en"})
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertIn("## What the law says", data["brief"])

    def test_samples_endpoint_lists_samples(self) -> None:
        status, body = self._get("/api/samples")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertTrue(len(data["samples"]) >= 3)

    def test_sample_endpoint_serves_markdown(self) -> None:
        status, body = self._get("/api/samples")
        name = json.loads(body)["samples"][0]
        status, body = self._get(f"/api/sample?name={name}")
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertIn("not legal advice", data["body"])

    def test_reset_budget(self) -> None:
        self._post("/api/ask", {"question": "Someone stole my password.", "language": "en"})
        status, data = self._post("/api/reset-budget", {})
        self.assertEqual(status, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["budget"]["used"], 0)


class TestWsgi(unittest.TestCase):
    def _call(self, method: str, path: str, body: bytes = b""):
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": "",
            "CONTENT_LENGTH": str(len(body)),
            "wsgi.input": __import__("io").BytesIO(body),
            "wsgi.errors": __import__("io").StringIO(),
            "wsgi.version": (1, 0),
            "wsgi.run_once": False,
            "wsgi.url_scheme": "http",
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "SERVER_NAME": "test",
            "SERVER_PORT": "80",
        }
        captured: dict = {}

        def start_response(status, headers):
            captured["status"] = status
            captured["headers"] = headers

        chunks = application(environ, start_response)
        return captured["status"], b"".join(chunks).decode("utf-8")

    def test_wsgi_home(self) -> None:
        status, body = self._call("GET", "/")
        self.assertTrue(status.startswith("200"))
        self.assertIn("NyayaVault", body)

    def test_wsgi_status(self) -> None:
        status, body = self._call("GET", "/api/status")
        data = json.loads(body)
        self.assertTrue(status.startswith("200"))
        self.assertTrue(data["ok"])
        self.assertEqual(data["notes_count"], 17)

    def test_wsgi_unknown_404(self) -> None:
        status, _ = self._call("GET", "/nope")
        self.assertTrue(status.startswith("404"))


if __name__ == "__main__":
    unittest.main()
