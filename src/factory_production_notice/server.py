from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .agent_contract import build_agent_interface
from .generator import generate_notice


class NoticeApiHandler(BaseHTTPRequestHandler):
    output_dir = Path("output")

    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_json({"ok": True, "service": "factory-production-notice-agent"})
            return
        if self.path == "/agent-interface":
            self.send_json(build_agent_interface())
            return
        self.send_json({"error": "not_found", "paths": ["/health", "/agent-interface", "/api/generate-notice"]}, status=404)

    def do_POST(self) -> None:
        if self.path != "/api/generate-notice":
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
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


def run_server(host: str, port: int, output_dir: str | Path) -> None:
    NoticeApiHandler.output_dir = Path(output_dir)
    server = ThreadingHTTPServer((host, port), NoticeApiHandler)
    print(f"Serving production notice API at http://{host}:{port}")
    print("POST /api/generate-notice with a ProductionNoticeRequest JSON payload")
    server.serve_forever()
