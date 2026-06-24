from __future__ import annotations

from typing import Any


def build_agent_interface() -> dict[str, Any]:
    return {
        "name": "factory-production-notice-agent",
        "version": "0.4.0",
        "description": "Generate production and operations notice workbooks from JSON, CSV, templates, or schedule plans.",
        "public_positioning": "Local-first notice generator for manufacturing, warehouse, maintenance, service, and other repeatable operations workflows.",
        "input_contract": {
            "format": "json",
            "schema_path": "config/notice_schema.json",
            "sample_path": "sample_data/demo_notice_request.json",
            "production_sample_path": "sample_data/production_notice_request.json",
            "csv_sample_path": "sample_data/csv/work_package_notices.csv",
            "scenario_profile_path": "config/scenario_profiles.json",
            "template_path": "config/notice_templates.json",
            "schedule_sample_path": "sample_data/scheduling_plan.json",
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
                "description": "Create a styled operations notice workbook, HTML preview, manifest, and workflow context.",
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
                "name": "import_csv_work_packages",
                "description": "Convert one or more tabular work-package rows into validated notice request JSON files.",
                "cli": "python -m factory_production_notice.cli import-csv --input sample_data/csv/work_package_notices.csv --output-dir output/imported",
                "outputs": ["notice_request.json"],
            },
            {
                "name": "list_scenario_profiles",
                "description": "List built-in scenario profiles for common operations workflows.",
                "cli": "python -m factory_production_notice.cli profiles",
                "outputs": ["profile_catalog.json"],
            },
            {
                "name": "list_notice_templates",
                "description": "List built-in and optional custom notice templates with field presets.",
                "cli": "python -m factory_production_notice.cli templates",
                "outputs": ["template_catalog.json"],
            },
            {
                "name": "create_notice_from_template",
                "description": "Create an editable notice request from a built-in or user-owned template.",
                "cli": "python -m factory_production_notice.cli new-from-template --template production-release --output output/production_request.json",
                "outputs": ["notice_request.json"],
            },
            {
                "name": "generate_from_schedule",
                "description": "Convert a schedule plan into notice request JSON files and generated notice artifacts.",
                "cli": "python -m factory_production_notice.cli schedule-generate --input sample_data/scheduling_plan.json --output output/scheduled_release",
                "outputs": ["schedule_manifest.json", "notice_request.json", "xlsx", "html", "manifest.json", "agent_context.json"],
            },
            {
                "name": "export_agent_context",
                "description": "Convert a notice request into a structured workflow context payload.",
                "cli": "python -m factory_production_notice.cli analysis-context --input sample_data/demo_notice_request.json --output output/analysis_context.json",
            },
        ],
        "workflow": [
            "Select a scenario profile or import a CSV work package",
            "Apply a built-in or user-owned template when a preset is needed",
            "Optionally generate notice requests and artifacts from a schedule plan",
            "Convert the input into the standard operations notice request",
            "Validate required subject, quantity, due date, resource, step, fulfillment, and control fields",
            "Generate workbook and preview artifacts",
            "Return manifest and structured workflow context",
            "Let a human reviewer approve release before sending the notice into the live workflow",
        ],
        "safety_notes": [
            "Do not commit private BOM files, customer records, supplier lists, or generated notice history",
            "Use masked or synthetic examples in public repositories",
            "Keep final operational release approval as a human decision",
        ],
    }
