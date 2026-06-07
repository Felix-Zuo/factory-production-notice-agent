from __future__ import annotations

from pathlib import Path

from factory_production_notice.agent_contract import build_agent_interface
from factory_production_notice.generator import generate_notice
from factory_production_notice.io_utils import read_json


def test_demo_generation(tmp_path: Path) -> None:
    payload = read_json("sample_data/demo_notice_request.json")
    result = generate_notice(payload, tmp_path)

    assert result.xlsx_path.exists()
    assert result.html_path.exists()
    assert result.manifest_path.exists()
    assert result.agent_context_path.exists()

    context = read_json(result.agent_context_path)
    assert context["notice_id"] == "PN-2026-DEMO-001"
    assert context["required_materials"][0]["required_quantity"] == 1200


def test_agent_interface_shape() -> None:
    spec = build_agent_interface()
    capability_names = {item["name"] for item in spec["capabilities"]}
    assert "generate_notice" in capability_names
    assert spec["input_contract"]["sample_path"].endswith("demo_notice_request.json")
