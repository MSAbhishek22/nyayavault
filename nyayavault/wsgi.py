"""NyayaVault WSGI entrypoint (Vercel / any WSGI host).

Stdlib only. The corpus lives in ``corpus/`` next to this package;
the samples live in ``samples/``. No secrets are read from files —
the BharatCode key comes from the environment only.
"""

from __future__ import annotations

import os

from .config import config_from_env
from .web import make_handler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_ROOT = os.path.join(BASE_DIR, "corpus")
SAMPLES_ROOT = os.path.join(BASE_DIR, "samples")

config = config_from_env(CORPUS_ROOT)

from .agent import LegalAgent  # noqa: E402  (config first, for clarity)

agent = LegalAgent(config)
_handler = make_handler(agent, config, SAMPLES_ROOT)


def application(environ, start_response):
    """WSGI callable: delegates to the bound HTTP handler logic."""
    from wsgiref.util import setup_testing_defaults

    setup_testing_defaults(environ)
    # Adapt the BaseHTTPRequestHandler-based handler to WSGI by
    # reusing its request dispatch through a minimal shim.
    return _wsgi_dispatch(environ, start_response)


def _wsgi_dispatch(environ, start_response):
    """Dispatch one WSGI request through the NyayaVault handler.

    The handler class is written for BaseHTTPRequestHandler; the
    shim below re-implements its routing in WSGI terms so the same
    code serves both ``python3 run.py`` and a WSGI host.
    """
    import io
    import json
    import urllib.parse

    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    query = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw = environ["wsgi.input"].read(length) if length > 0 else b""
    try:
        payload = json.loads(raw.decode("utf-8")) if raw else {}
    except (ValueError, UnicodeDecodeError):
        payload = {}

    status = "200 OK"
    headers = [("Content-Type", "application/json")]
    body: bytes

    def json_body(obj: dict, code: str = "200 OK") -> bytes:
        nonlocal status
        status = code
        return json.dumps(obj).encode("utf-8")

    if method == "GET" and path == "/":
        from .web import _page

        html = _page(agent).encode("utf-8")
        headers = [("Content-Type", "text/html; charset=utf-8")]
        body = html
    elif method == "GET" and path == "/api/status":
        from .web import _status_payload

        body = json_body(_status_payload(agent, config))
    elif method == "GET" and path == "/api/document":
        rel = (query.get("path") or [""])[0]
        provision = next((p for p in agent.provisions if p.rel == rel), None)
        if provision is None:
            body = json_body({"ok": False, "error": "Provision not found."}, "404 Not Found")
        else:
            body = json_body({
                "ok": True,
                "title": provision.title,
                "rel": provision.rel,
                "act": provision.act,
                "section": provision.section,
                "source": provision.source,
                "citation": provision.citation,
                "body": provision.body,
            })
    elif method == "GET" and path == "/api/samples":
        body = json_body({"ok": True, "samples": agent.list_samples(SAMPLES_ROOT)})
    elif method == "GET" and path == "/api/sample":
        name = (query.get("name") or [""])[0]
        text = agent.read_sample(SAMPLES_ROOT, name)
        if text is None:
            body = json_body({"ok": False, "error": "Sample not found."}, "404 Not Found")
        else:
            body = json_body({"ok": True, "name": name, "body": text})
    elif method == "POST" and path == "/api/ask":
        detail = agent.ask_detailed(payload.get("question", ""), payload.get("language", "en"))
        body = json_body({
            "ok": detail.ok,
            "answer": detail.answer,
            "error": detail.error,
            "citations": [
                {
                    "title": p.title,
                    "rel": p.rel,
                    "act": p.act,
                    "section": p.section,
                    "citation": p.citation,
                }
                for p in detail.citations
            ],
            "mode": detail.mode,
            "language": detail.language,
            "model": detail.model,
            "reason": detail.reason,
            "attempted": detail.attempted,
            "fallback_used": detail.fallback_used,
        })
    elif method == "POST" and path == "/api/brief":
        question = payload.get("question", "")
        if not question.strip():
            body = json_body({"ok": False, "error": "Ask a question first."})
        else:
            body = json_body({"ok": True, "brief": agent.research_brief(question, payload.get("language", "en"))})
    elif method == "POST" and path == "/api/reset-budget":
        agent.ledger.calls_used = 0
        agent.ledger.exhausted = False
        body = json_body({"ok": True, "budget": {"used": 0, "limit": agent.ledger.cap}})
    else:
        body = json_body({"ok": False, "error": "Not found."}, "404 Not Found")

    start_response(status, headers)
    return [body]
