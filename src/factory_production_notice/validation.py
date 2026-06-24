from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .models import NoticeValidationError, ProductionNotice


@dataclass
class NoticeValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": self.summary,
        }


def validate_notice_payload(payload: dict[str, Any]) -> NoticeValidationResult:
    try:
        notice = ProductionNotice.from_dict(payload)
    except NoticeValidationError as exc:
        return NoticeValidationResult(ok=False, errors=[str(exc)])

    warnings = review_warnings(notice)
    return NoticeValidationResult(
        ok=True,
        warnings=warnings,
        summary={
            "notice_id": notice.notice_id,
            "notice_type": notice.notice_type,
            "domain": notice.domain,
            "subject_id": notice.product.item_code,
            "subject": notice.product.name,
            "quantity": notice.quantity,
            "quantity_unit": notice.quantity_unit,
            "resource_count": len(notice.materials),
            "step_count": len(notice.routing),
            "custom_field_count": len(notice.custom_fields),
        },
    )


def review_warnings(notice: ProductionNotice) -> list[str]:
    warnings: list[str] = []
    if not notice.materials:
        warnings.append("No resources/materials are listed.")
    if not notice.routing:
        warnings.append("No execution steps/routing entries are listed.")
    if not notice.packaging:
        warnings.append("No fulfillment/packaging rule is listed.")
    if not notice.quality:
        warnings.append("No controls/quality rule is listed.")
    if notice.quantity >= 10000:
        warnings.append("Quantity is unusually high for a public demo payload.")
    if not notice.customer:
        warnings.append("Requester/customer is blank.")
    return warnings
