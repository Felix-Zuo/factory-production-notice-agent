from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from .io_utils import project_root, read_json
from .models import ProductionNotice, labelize


class NoticeTemplateError(ValueError):
    """Raised when a notice template cannot be resolved or applied."""


def load_templates(template_file: str | Path | None = None) -> list[dict[str, Any]]:
    payload = read_json(project_root() / "config" / "notice_templates.json")
    templates = _template_list(payload, "config/notice_templates.json")
    if template_file:
        custom_payload = read_json(template_file)
        templates.extend(_template_list(custom_payload, str(template_file)))
    return templates


def template_catalog(template_file: str | Path | None = None) -> dict[str, Any]:
    templates = [
        {
            "id": item["id"],
            "label": item.get("label", item["id"]),
            "profile_id": item.get("profile_id", ""),
            "description": item.get("description", ""),
        }
        for item in load_templates(template_file)
    ]
    return {"templates": templates, "count": len(templates)}


def build_notice_from_template(
    template_id: str,
    *,
    template_file: str | Path | None = None,
    overrides: list[str] | None = None,
    custom_fields: list[str] | None = None,
) -> dict[str, Any]:
    template = resolve_template(template_id, template_file)
    payload = deepcopy(template.get("payload", {}))
    if not isinstance(payload, dict):
        raise NoticeTemplateError(f"Template {template_id} payload must be an object")

    for assignment in overrides or []:
        key, value = parse_assignment(assignment)
        set_path(payload, key, parse_value(value))

    for assignment in custom_fields or []:
        key, value = parse_assignment(assignment)
        append_custom_field(payload, key, value)

    ProductionNotice.from_dict(payload)
    return payload


def resolve_template(template_id: str, template_file: str | Path | None = None) -> dict[str, Any]:
    for template in load_templates(template_file):
        if template.get("id") == template_id:
            return template
    raise NoticeTemplateError(f"Template not found: {template_id}")


def deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def append_custom_field(payload: dict[str, Any], key: str, value: Any, *, group: str = "Custom") -> None:
    fields = payload.setdefault("custom_fields", [])
    if isinstance(fields, dict):
        fields[key] = value
        return
    if not isinstance(fields, list):
        raise NoticeTemplateError("custom_fields must be an object or an array")
    fields.append({"key": key, "label": labelize(key), "value": value, "group": group})


def set_path(payload: dict[str, Any], dotted_path: str, value: Any) -> None:
    parts = [part for part in dotted_path.split(".") if part]
    if not parts:
        raise NoticeTemplateError("Override path must not be blank")
    target = payload
    for part in parts[:-1]:
        child = target.setdefault(part, {})
        if not isinstance(child, dict):
            raise NoticeTemplateError(f"Cannot set nested value under non-object path: {part}")
        target = child
    target[parts[-1]] = value


def parse_assignment(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise NoticeTemplateError("Expected KEY=VALUE assignment")
    key, raw_value = value.split("=", 1)
    key = key.strip()
    if not key:
        raise NoticeTemplateError("Assignment key must not be blank")
    return key, raw_value.strip()


def parse_value(value: str) -> Any:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _template_list(payload: dict[str, Any], source: str) -> list[dict[str, Any]]:
    templates = payload.get("templates", [])
    if not isinstance(templates, list) or any(not isinstance(item, dict) for item in templates):
        raise NoticeTemplateError(f"{source} must contain a templates array of objects")
    return templates
