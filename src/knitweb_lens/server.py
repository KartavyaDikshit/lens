"""Tiny stdlib HTTP server exposing POST /interpret."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Iterable

from .adapters import LocalFilesAdapter
from .rlm import RLMHarness


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("content-type", "application/json")
    handler.send_header("content-length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def make_handler(base_paths: Iterable[str | Path]) -> type[BaseHTTPRequestHandler]:
    configured_paths = tuple(str(path) for path in base_paths)

    class InterpretHandler(BaseHTTPRequestHandler):
        server_version = "KnitwebLens/0.1"

        def log_message(self, format: str, *args: object) -> None:
            return

        def do_GET(self) -> None:
            if self.path == "/health":
                _json_response(self, 200, {"ok": True, "route": "/interpret"})
                return
            _json_response(self, 404, {"error": "not found"})

        def do_POST(self) -> None:
            if self.path != "/interpret":
                _json_response(self, 404, {"error": "not found"})
                return
            try:
                length = int(self.headers.get("content-length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
                query = payload["query"]
                paths = tuple(configured_paths) + tuple(payload.get("paths", ()))
                adapters = [LocalFilesAdapter(paths)] if paths else []
                answer = RLMHarness().query(
                    query,
                    adapters=adapters,
                    max_chunks=int(payload.get("max_chunks", 8)),
                    budget_chars=int(payload.get("budget_chars", 4000)),
                )
                _json_response(self, 200, answer.to_dict())
            except Exception as exc:
                _json_response(self, 400, {"error": str(exc)})

    return InterpretHandler


def serve(paths: Iterable[str | Path], *, host: str = "127.0.0.1", port: int = 8765) -> None:
    httpd = HTTPServer((host, port), make_handler(paths))
    print(f"Lens serving /interpret on http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()

