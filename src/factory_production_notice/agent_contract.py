from __future__ import annotations

from typing import Any


def build_agent_interface() -> dict[str, Any]:
    return {
        "name": "factory-production-notice-agent",
        "version": "0.2.1",
        "description": "Generate operations notice workbooks from structured work-package requests.",
        "public_positioning": "Local-first notice generator for manufacturing, warehouse, maintenance, service, and other repeatable operations workflows.",
        "input_contract": {
            "format": "json",
            "schema_path": "config/notice_schema.json",
            "sample_path": "sample_data/demo_notice_request.json",
        },
        "supported_domains": [
            "manufacturing release",
            "warehouse fulfillment",
            "maintenance work package",
            "field service dispatch",
            "quality or compliance review",
        ],
        "capabilities": [
            {
                "name": "generate_operations_notice",
                "description": "Create a styled operations notice workbook, HTML preview, manifest, and agent context.",
                "cli": "python -m factory_production_notice.cli generate --input sample_data/demo_notice_request.json --output output",
                "http": {
                    "method": "POST",
                    "path": "/api/generate-operations-notice",
                    "body": "OperationsNoticeRequest JSON",
                },
                "outputs": ["xlsx", "html", "manifest.json", "agent_context.json"],
            },
            {
                "name": "generate_notice",
                "description": "Backward-compatible alias for existing production-notice integrations.",
                "cli": "python -m factory_production_notice.cli generate --input sample_data/demo_notice_request.json --output output",
                "http": {
                    "method": "POST",
                    "path": "/api/generate-notice",
                    "body": "OperationsNoticeRequest JSON",
                },
                "outputs": ["xlsx", "html", "manifest.json", "agent_context.json"],
            },
            {
                "name": "run_demo",
                "description": "Generate the public demo artifacts from synthetic sample data.",
                "cli": "python -m factory_production_notice.cli run-demo --output output",
            },
            {
                "name": "validate_notice",
                "description": "Validate a notice request and return preflight warnings without writing artifacts.",
                "cli": "python -m factory_production_notice.cli validate --input sample_data/demo_notice_request.json",
            },
            {
                "name": "export_agent_context",
                "description": "Convert a notice request into a structured context payload for downstream analysis agents.",
                "cli": "python -m factory_production_notice.cli analysis-context --input sample_data/demo_notice_request.json --output output/analysis_context.json",
            },
        ],
        "workflow": [
            "Receive a standard operations notice request",
            "Validate required subject, quantity, due date, resource, step, fulfillment, and control fields",
            "Generate workbook and preview artifacts",
            "Return manifest and structured agent context",
            "Let a human reviewer approve release before sending the notice into the live workflow",
        ],
        "safety_notes": [
            "Do not commit private BOM files, customer records, supplier lists, or generated notice history",
            "Use masked or synthetic examples in public repositories",
            "Keep final operational release approval as a human decision",
        ],
    }
