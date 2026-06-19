from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .agent_contract import build_agent_interface
from .generator import generate_notice


class NoticeApiHandler(BaseHTTPRequestHandler):
    output_dir = Path("output")
    max_body_bytes = 1_000_000

    def do_GET(self) -> None:
        path = urlsplit(self.path).path.rstrip("/") or "/"
        if path == "/health":
            self.send_json({"ok": True, "service": "structured-operations-notice-agent"})
            return
        if path == "/agent-interface":
            self.send_json(build_agent_interface())
            return
        self.send_json(
            {"error": "not_found", "paths": ["/health", "/agent-interface", "/api/generate-notice", "/api/generate-operations-notice"]},
            status=404,
        )

    def do_POST(self) -> None:
        path = urlsplit(self.path).path.rstrip("/") or "/"
        if path not in {"/api/generate-notice", "/api/generate-operations-notice"}:
            self.send_json({"error": "not_found"}, status=404)
            return
        try:
            payload = self.read_body_json()
            result = generate_notice(payload, self.output_dir)
            self.send_json({"ok": True, "artifacts": result.as_manifest()})
        except Exception as exc:  # API boundary returns structured errors.
            self.send_json({"ok": False, "error": str(exc)}, status=400)

    def read_body_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            raise ValueError("Request body must not be empty")
        if length > self.max_body_bytes:
            raise ValueError(f"Request body exceeds {self.max_body_bytes} bytes")
        raw = self.rfile.read(length)
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Request body must be a JSON object")
        return data

    def send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def run_server(host: str, port: int, output_dir: str | Path) -> None:
    NoticeApiHandler.output_dir = Path(output_dir)
    server = ThreadingHTTPServer((host, port), NoticeApiHandler)
    print(f"Serving operations notice API at http://{host}:{port}")
    print("POST /api/generate-notice with an OperationsNoticeRequest JSON payload")
    server.serve_forever()
