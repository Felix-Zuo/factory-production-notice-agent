from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class NoticeValidationError(ValueError):
    """Raised when an operations notice request is missing required data."""


@dataclass
class Product:
    item_code: str
    name: str
    model: str = ""
    revision: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Product":
        return cls(
            item_code=str(payload.get("item_code") or payload.get("subject_id") or payload.get("id") or "").strip(),
            name=str(payload.get("name", "")).strip(),
            model=str(payload.get("model") or payload.get("category") or payload.get("type") or "").strip(),
            revision=str(payload.get("revision", "")).strip(),
        )


@dataclass
class MaterialLine:
    item_code: str
    name: str
    quantity_per: float = 0
    unit: str = "pcs"
    source: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MaterialLine":
        return cls(
            item_code=str(payload.get("item_code") or payload.get("resource_id") or payload.get("id") or "").strip(),
            name=str(payload.get("name", "")).strip(),
            quantity_per=float(payload.get("quantity_per") or 0),
            unit=str(payload.get("unit", "pcs")).strip() or "pcs",
            source=str(payload.get("source", "")).strip(),
        )


@dataclass
class RoutingStep:
    step: str
    work_center: str
    description: str = ""
    cycle_time_sec: float = 0

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RoutingStep":
        cycle_time = payload.get("cycle_time_sec")
        if cycle_time is None:
            cycle_time = payload.get("target_time_sec")
        if cycle_time is None and payload.get("target_time_min") is not None:
            cycle_time = float(payload.get("target_time_min") or 0) * 60
        return cls(
            step=str(payload.get("step") or payload.get("id") or "").strip(),
            work_center=str(payload.get("work_center") or payload.get("owner") or payload.get("station") or "").strip(),
            description=str(payload.get("description") or payload.get("instruction") or "").strip(),
            cycle_time_sec=float(cycle_time or 0),
        )


@dataclass
class ProductionNotice:
    notice_id: str
    work_order: str
    product: Product
    quantity: float
    due_date: str
    notice_type: str = "Operations Notice"
    domain: str = "general-operations"
    quantity_unit: str = "units"
    customer: str = ""
    priority: str = "normal"
    issuer: str = "Operations Office"
    materials: list[MaterialLine] = field(default_factory=list)
    routing: list[RoutingStep] = field(default_factory=list)
    packaging: dict[str, Any] = field(default_factory=dict)
    quality: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProductionNotice":
        required = ["notice_id", "work_order", "quantity", "due_date"]
        missing = [field_name for field_name in required if field_name not in payload]
        if missing:
            raise NoticeValidationError(f"Missing required fields: {', '.join(missing)}")

        product_payload = payload.get("subject") or payload.get("product")
        if not isinstance(product_payload, dict):
            raise NoticeValidationError("Field 'subject' or legacy field 'product' must be an object")

        product = Product.from_dict(product_payload)
        if not product.item_code or not product.name:
            raise NoticeValidationError("Subject item_code/subject_id and name are required")

        notice_id = str(payload["notice_id"]).strip()
        work_order = str(payload["work_order"]).strip()
        due_date = str(payload["due_date"]).strip()
        if not notice_id or not work_order or not due_date:
            raise NoticeValidationError("notice_id, work_order, and due_date must not be blank")

        try:
            quantity = float(payload["quantity"])
        except (TypeError, ValueError) as exc:
            raise NoticeValidationError("quantity must be a number") from exc
        if quantity <= 0:
            raise NoticeValidationError("quantity must be greater than zero")

        materials_payload = payload.get("resources", payload.get("materials", []))
        routing_payload = payload.get("steps", payload.get("routing", []))
        if not isinstance(materials_payload, list):
            raise NoticeValidationError("resources/materials must be an array")
        if not isinstance(routing_payload, list):
            raise NoticeValidationError("steps/routing must be an array")
        if any(not isinstance(item, dict) for item in materials_payload):
            raise NoticeValidationError("resources/materials entries must be objects")
        if any(not isinstance(item, dict) for item in routing_payload):
            raise NoticeValidationError("steps/routing entries must be objects")

        packaging_payload = payload.get("fulfillment", payload.get("packaging", {}))
        quality_payload = payload.get("controls", payload.get("quality", {}))
        if not isinstance(packaging_payload, dict):
            raise NoticeValidationError("fulfillment/packaging must be an object")
        if not isinstance(quality_payload, dict):
            raise NoticeValidationError("controls/quality must be an object")

        return cls(
            notice_id=notice_id,
            work_order=work_order,
            product=product,
            quantity=quantity,
            due_date=due_date,
            notice_type=str(payload.get("notice_type", "Operations Notice")).strip() or "Operations Notice",
            domain=str(payload.get("domain", "general-operations")).strip() or "general-operations",
            quantity_unit=str(payload.get("quantity_unit", "units")).strip() or "units",
            customer=str(payload.get("requester") or payload.get("customer") or "").strip(),
            priority=str(payload.get("priority", "normal")).strip() or "normal",
            issuer=str(payload.get("issuer", "Operations Office")).strip(),
            materials=[MaterialLine.from_dict(item) for item in materials_payload],
            routing=[RoutingStep.from_dict(item) for item in routing_payload],
            packaging=dict(packaging_payload),
            quality=dict(quality_payload),
            notes=[str(item) for item in payload.get("notes", [])],
        )

    def to_agent_context(self) -> dict[str, Any]:
        total_cycle = sum(step.cycle_time_sec for step in self.routing)
        required_resources = [
            {
                "item_code": line.item_code,
                "name": line.name,
                "required_quantity": round(line.quantity_per * self.quantity, 4),
                "unit": line.unit,
                "source": line.source,
            }
            for line in self.materials
        ]
        return {
            "notice_type": self.notice_type,
            "domain": self.domain,
            "notice_id": self.notice_id,
            "work_order": self.work_order,
            "requester": self.customer,
            "customer": self.customer,
            "subject": {
                "item_code": self.product.item_code,
                "name": self.product.name,
                "category": self.product.model,
                "revision": self.product.revision,
            },
            "product": {
                "item_code": self.product.item_code,
                "name": self.product.name,
                "model": self.product.model,
                "revision": self.product.revision,
            },
            "quantity": self.quantity,
            "quantity_unit": self.quantity_unit,
            "due_date": self.due_date,
            "priority": self.priority,
            "execution_step_count": len(self.routing),
            "routing_step_count": len(self.routing),
            "estimated_cycle_time_sec_per_unit": total_cycle,
            "required_resources": required_resources,
            "required_materials": required_resources,
            "controls": self.quality,
            "quality": self.quality,
            "fulfillment": self.packaging,
            "packaging": self.packaging,
            "agent_recommended_checks": [
                "Validate required resources before releasing the notice",
                "Confirm step ownership and capacity against the due date",
                "Review fulfillment and label rules for requester-specific constraints",
                "Escalate if required fields are missing or quantity is unusually high",
            ],
        }
