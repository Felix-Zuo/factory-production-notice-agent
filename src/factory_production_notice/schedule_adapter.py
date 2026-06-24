from __future__ import annotations

from pathlib import Path
from typing import Any

from .generator import generate_notice, slug
from .io_utils import read_json, write_json
from .models import ProductionNotice
from .templates import NoticeTemplateError, append_custom_field, deep_merge, resolve_template


class SchedulePlanError(ValueError):
    """Raised when a schedule plan cannot be converted into notices."""


def generate_from_schedule(
    schedule_path: str | Path,
    output_dir: str | Path,
    *,
    template_file: str | Path | None = None,
) -> dict[str, Any]:
    plan = read_json(schedule_path)
    items = plan.get("items", [])
    if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
        raise SchedulePlanError("Schedule plan must contain an items array of objects")
    if not items:
        raise SchedulePlanError("Schedule plan items must not be empty")

    template_id = str(plan.get("template_id") or "production-release").strip()
    template = resolve_template(template_id, template_file)
    base_payload = template.get("payload", {})
    if not isinstance(base_payload, dict):
        raise SchedulePlanError(f"Template {template_id} payload must be an object")

    out = Path(output_dir)
    requests_dir = out / "requests"
    artifacts_dir = out / "artifacts"
    entries = []
    for item in items:
        payload = build_scheduled_notice_payload(base_payload, plan, item)
        ProductionNotice.from_dict(payload)
        request_name = f"{slug(str(payload['notice_id']))}.json"
        write_json(requests_dir / request_name, payload)
        result = generate_notice(payload, artifacts_dir)
        entries.append(
            {
                "notice_id": payload["notice_id"],
                "work_order": payload["work_order"],
                "line": item.get("line", ""),
                "slot_start": item.get("slot_start", ""),
                "slot_end": item.get("slot_end", ""),
                "request": f"requests/{request_name}",
                "artifacts": {
                    "xlsx": f"artifacts/{result.xlsx_path.name}",
                    "html": f"artifacts/{result.html_path.name}",
                    "manifest": f"artifacts/{result.manifest_path.name}",
                    "agent_context": f"artifacts/{result.agent_context_path.name}",
                },
            }
        )

    manifest = {
        "schedule_id": plan.get("schedule_id", ""),
        "template_id": template_id,
        "planner": plan.get("planner", ""),
        "release_date": plan.get("release_date", ""),
        "notice_count": len(entries),
        "notices": entries,
    }
    write_json(out / "schedule_manifest.json", manifest)
    return manifest


def build_scheduled_notice_payload(base_payload: dict[str, Any], plan: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    reserved = {"line", "shift", "slot_start", "slot_end", "capacity_status", "sequence", "custom_fields"}
    overlay = {key: value for key, value in item.items() if key not in reserved}
    payload = deep_merge(base_payload, overlay)

    schedule_fields = {
        "schedule_id": plan.get("schedule_id", ""),
        "planner": plan.get("planner", ""),
        "release_date": plan.get("release_date", ""),
        "line": item.get("line", ""),
        "shift": item.get("shift", ""),
        "slot_start": item.get("slot_start", ""),
        "slot_end": item.get("slot_end", ""),
        "capacity_status": item.get("capacity_status", ""),
        "sequence": item.get("sequence", ""),
    }
    schedule_keys = set(schedule_fields)
    existing_fields = payload.get("custom_fields", [])
    if isinstance(existing_fields, list):
        payload["custom_fields"] = [
            field
            for field in existing_fields
            if not (isinstance(field, dict) and str(field.get("key", "")).strip() in schedule_keys)
        ]
    elif isinstance(existing_fields, dict):
        for key in schedule_keys:
            existing_fields.pop(key, None)
    elif existing_fields not in (None, ""):
        raise NoticeTemplateError("custom_fields must be an object or an array")

    for key, value in schedule_fields.items():
        if value not in ("", None):
            append_custom_field(payload, key, value, group="Schedule")

    custom_fields = item.get("custom_fields", {})
    if isinstance(custom_fields, dict):
        for key, value in custom_fields.items():
            append_custom_field(payload, str(key), value, group="Scheduled Custom")
    elif isinstance(custom_fields, list):
        fields = payload.setdefault("custom_fields", [])
        if not isinstance(fields, list):
            raise NoticeTemplateError("custom_fields must be an object or an array")
        fields.extend(custom_fields)
    elif custom_fields not in ({}, [], None):
        raise SchedulePlanError("Schedule item custom_fields must be an object or an array")

    return payload
