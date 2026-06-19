from __future__ import annotations

from pathlib import Path

from factory_production_notice.agent_contract import build_agent_interface
from factory_production_notice.generator import generate_notice
from factory_production_notice.io_utils import read_json
from factory_production_notice.models import NoticeValidationError, ProductionNotice
from scripts.package_project import should_skip


def test_demo_generation(tmp_path: Path) -> None:
    payload = read_json("sample_data/demo_notice_request.json")
    result = generate_notice(payload, tmp_path)

    assert result.xlsx_path.exists()
    assert result.html_path.exists()
    assert result.manifest_path.exists()
    assert result.agent_context_path.exists()

    context = read_json(result.agent_context_path)
    assert context["notice_id"] == "ON-2026-DEMO-001"
    assert context["domain"] == "warehouse-fulfillment"
    assert context["required_resources"][0]["required_quantity"] == 240
    assert context["required_materials"][0]["required_quantity"] == 240


def test_agent_interface_shape() -> None:
    spec = build_agent_interface()
    capability_names = {item["name"] for item in spec["capabilities"]}
    assert "generate_operations_notice" in capability_names
    assert "generate_notice" in capability_names
    assert spec["input_contract"]["sample_path"].endswith("demo_notice_request.json")


def test_legacy_manufacturing_payload_still_works(tmp_path: Path) -> None:
    payload = {
        "notice_id": "PN-LEGACY-001",
        "work_order": "WO-LEGACY-001",
        "quantity": 12,
        "due_date": "2026-06-30",
        "product": {"item_code": "FG-001", "name": "Legacy Assembly"},
        "materials": [{"item_code": "RM-001", "name": "Legacy Part", "quantity_per": 2}],
        "routing": [{"step": "OP10", "work_center": "Cell A", "description": "Build"}],
    }

    result = generate_notice(payload, tmp_path)
    context = read_json(result.agent_context_path)

    assert context["product"]["item_code"] == "FG-001"
    assert context["required_materials"][0]["required_quantity"] == 24


def test_rejects_invalid_quantity() -> None:
    payload = {
        "notice_id": "ON-BAD-001",
        "work_order": "OPS-BAD-001",
        "quantity": 0,
        "due_date": "2026-06-30",
        "subject": {"subject_id": "BAD", "name": "Invalid Quantity"},
    }

    try:
        ProductionNotice.from_dict(payload)
    except NoticeValidationError as exc:
        assert "quantity must be greater than zero" in str(exc)
    else:
        raise AssertionError("Expected NoticeValidationError")


def test_rejects_non_object_resource_entries() -> None:
    payload = {
        "notice_id": "ON-BAD-002",
        "work_order": "OPS-BAD-002",
        "quantity": 1,
        "due_date": "2026-06-30",
        "subject": {"subject_id": "BAD", "name": "Invalid Resource"},
        "resources": ["not an object"],
    }

    try:
        ProductionNotice.from_dict(payload)
    except NoticeValidationError as exc:
        assert "resources/materials entries must be objects" in str(exc)
    else:
        raise AssertionError("Expected NoticeValidationError")


def test_package_excludes_generated_probe_outputs() -> None:
    assert should_skip(Path("output") / "demo.html")
    assert should_skip(Path("output_http_probe") / "demo.html")
    assert should_skip(Path("output_alias_probe") / "demo.html")
