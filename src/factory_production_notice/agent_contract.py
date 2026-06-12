from __future__ import annotations

from typing import Any


def build_agent_interface() -> dict[str, Any]:
    return {
        "name": "factory-production-notice-agent",
        "version": "0.1.1",
        "description": "Generate production notice workbooks from structured manufacturing requests.",
        "input_contract": {
            "format": "json",
            "schema_path": "config/notice_schema.json",
            "sample_path": "sample_data/demo_notice_request.json",
        },
        "capabilities": [
            {
                "name": "generate_notice",
                "description": "Create a styled production notice workbook, HTML preview, manifest, and agent context.",
                "cli": "python -m factory_production_notice.cli generate --input sample_data/demo_notice_request.json --output output",
                "http": {
                    "method": "POST",
                    "path": "/api/generate-notice",
                    "body": "ProductionNoticeRequest JSON",
                },
                "outputs": ["xlsx", "html", "manifest.json", "agent_context.json"],
            },
            {
                "name": "run_demo",
                "description": "Generate the public demo artifacts from synthetic sample data.",
                "cli": "python -m factory_production_notice.cli run-demo --output output",
            },
            {
                "name": "export_agent_context",
                "description": "Convert a notice request into a structured context payload for downstream analysis agents.",
                "cli": "python -m factory_production_notice.cli analysis-context --input sample_data/demo_notice_request.json --output output/analysis_context.json",
            },
        ],
        "workflow": [
            "Receive standard production notice request",
            "Validate required product, quantity, due date, material, routing, packaging, and quality fields",
            "Generate workbook and preview artifacts",
            "Return manifest and structured agent context",
            "Let a human reviewer approve release before sending to production",
        ],
        "safety_notes": [
            "Do not commit production BOM files or generated notice history",
            "Use masked or synthetic examples in public repositories",
            "Keep final release approval as a human decision",
        ],
    }
