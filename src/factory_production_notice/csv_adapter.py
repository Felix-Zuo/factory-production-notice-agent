from __future__ import annotations

import csv
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterable

from .models import ProductionNotice

MAX_ROWS = 2000
MAX_CELL_LENGTH = 2000
LIST_SEPARATOR = "|"


class CsvImportError(ValueError):
    """Raised when a work-package CSV cannot be converted safely."""


def import_csv_notices(path: str | Path) -> list[dict[str, Any]]:
    rows = _read_rows(Path(path))
    grouped: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    for row in rows:
        notice_id = row.get("notice_id", "").strip()
        if not notice_id:
            raise CsvImportError("CSV column notice_id is required on every row")
        grouped.setdefault(notice_id, []).append(row)

    notices = [_build_notice_payload(notice_rows) for notice_rows in grouped.values()]
    for payload in notices:
        ProductionNotice.from_dict(payload)
    return notices


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise CsvImportError("CSV file must include a header row")
        rows: list[dict[str, str]] = []
        for index, row in enumerate(reader, start=1):
            if index > MAX_ROWS:
                raise CsvImportError(f"CSV import is limited to {MAX_ROWS} rows")
            cleaned = {_clean_key(key): _clean_cell(value) for key, value in row.items() if key is not None}
            if any(cleaned.values()):
                rows.append(cleaned)
    if not rows:
        raise CsvImportError("CSV file does not contain any data rows")
    return rows


def _build_notice_payload(rows: list[dict[str, str]]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "notice_id": _required_from_rows(rows, "notice_id"),
        "notice_type": _first_value(rows, "notice_type", "Operations Notice"),
        "domain": _first_value(rows, "domain", "general-operations"),
        "work_order": _required_from_rows(rows, "work_order"),
        "requester": _first_value(rows, "requester"),
        "priority": _first_value(rows, "priority", "normal"),
        "quantity": _required_number_from_rows(rows, "quantity"),
        "quantity_unit": _first_value(rows, "quantity_unit", "units"),
        "due_date": _required_from_rows(rows, "due_date"),
        "issuer": _first_value(rows, "issuer", "Operations Office"),
        "subject": {
            "subject_id": _required_from_rows(rows, "subject_id"),
            "name": _required_from_rows(rows, "subject_name"),
            "category": _first_value(rows, "subject_category"),
            "revision": _first_value(rows, "subject_revision"),
        },
        "resources": _resource_rows(rows),
        "steps": _step_rows(rows),
        "fulfillment": {
            "method": _first_value(rows, "fulfillment_method"),
            "units_per_container": _optional_number(_first_value(rows, "units_per_container"), key="units_per_container"),
            "containers_per_batch": _optional_number(_first_value(rows, "containers_per_batch"), key="containers_per_batch"),
            "label_rule": _first_value(rows, "label_rule"),
        },
        "controls": {
            "approval_required": _bool_cell(_first_value(rows, "approval_required")),
            "review_rule": _first_value(rows, "review_rule"),
            "critical_controls": _split_controls(rows),
        },
        "notes": _unique_values(row.get("note", "") for row in rows),
    }
    return payload


def _resource_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    resources: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for row in rows:
        resource_id = row.get("resource_id", "").strip()
        if not resource_id:
            continue
        resources[resource_id] = {
            "resource_id": resource_id,
            "name": row.get("resource_name", ""),
            "quantity_per": _optional_number(row.get("quantity_per"), key="quantity_per", default=0),
            "unit": row.get("resource_unit") or "pcs",
            "source": row.get("resource_source", ""),
        }
    return list(resources.values())


def _step_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    steps: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for row in rows:
        step = row.get("step", "").strip()
        if not step:
            continue
        steps[step] = {
            "step": step,
            "owner": row.get("owner", ""),
            "instruction": row.get("instruction", ""),
            "target_time_min": _optional_number(row.get("target_time_min"), key="target_time_min", default=0),
        }
    return list(steps.values())


def _clean_key(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _clean_cell(value: str | None) -> str:
    if value is None:
        return ""
    cleaned = value.strip()
    if len(cleaned) > MAX_CELL_LENGTH:
        raise CsvImportError(f"CSV cell exceeds {MAX_CELL_LENGTH} characters")
    return cleaned


def _required_from_rows(rows: list[dict[str, str]], key: str) -> str:
    value = _first_value(rows, key)
    if not value:
        raise CsvImportError(f"CSV column {key} is required")
    return value


def _required_number_from_rows(rows: list[dict[str, str]], key: str) -> float:
    value = _required_from_rows(rows, key)
    return _number_cell(value, key)


def _first_value(rows: list[dict[str, str]], key: str, default: str = "") -> str:
    for row in rows:
        value = row.get(key, "").strip()
        if value:
            return value
    return default


def _optional_number(value: str | None, *, key: str, default: float | int | str = "") -> float | int | str:
    if value is None or value == "":
        return default
    return _number_cell(value, key)


def _number_cell(value: str, key: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise CsvImportError(f"CSV column {key} must be a number") from exc
    if parsed < 0:
        raise CsvImportError(f"CSV column {key} must not be negative")
    return parsed


def _bool_cell(value: str | None) -> bool:
    if value is None or value == "":
        return False
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise CsvImportError("CSV column approval_required must be true or false")


def _split_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(LIST_SEPARATOR) if item.strip()]


def _split_controls(rows: list[dict[str, str]]) -> list[str]:
    return _unique_values(item for row in rows for item in _split_list(row.get("critical_controls", "")))


def _unique_values(values: Iterable[str]) -> list[str]:
    seen: OrderedDict[str, None] = OrderedDict()
    for value in values:
        cleaned = str(value).strip()
        if cleaned:
            seen[cleaned] = None
    return list(seen.keys())
