from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class NoticeValidationError(ValueError):
    """Raised when a production notice request is missing required data."""


@dataclass
class Product:
    item_code: str
    name: str
    model: str = ""
    revision: str = ""

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Product":
        return cls(
            item_code=str(payload.get("item_code", "")).strip(),
            name=str(payload.get("name", "")).strip(),
            model=str(payload.get("model", "")).strip(),
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
            item_code=str(payload.get("item_code", "")).strip(),
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
        return cls(
            step=str(payload.get("step", "")).strip(),
            work_center=str(payload.get("work_center", "")).strip(),
            description=str(payload.get("description", "")).strip(),
            cycle_time_sec=float(payload.get("cycle_time_sec") or 0),
        )


@dataclass
class ProductionNotice:
    notice_id: str
    work_order: str
    product: Product
    quantity: float
    due_date: str
    customer: str = ""
    priority: str = "normal"
    issuer: str = "Factory Operations Office"
    materials: list[MaterialLine] = field(default_factory=list)
    routing: list[RoutingStep] = field(default_factory=list)
    packaging: dict[str, Any] = field(default_factory=dict)
    quality: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ProductionNotice":
        required = ["notice_id", "work_order", "product", "quantity", "due_date"]
        missing = [field_name for field_name in required if field_name not in payload]
        if missing:
            raise NoticeValidationError(f"Missing required fields: {', '.join(missing)}")

        product_payload = payload.get("product")
        if not isinstance(product_payload, dict):
            raise NoticeValidationError("Field 'product' must be an object")

        product = Product.from_dict(product_payload)
        if not product.item_code or not product.name:
            raise NoticeValidationError("Product item_code and name are required")

        return cls(
            notice_id=str(payload["notice_id"]).strip(),
            work_order=str(payload["work_order"]).strip(),
            product=product,
            quantity=float(payload["quantity"]),
            due_date=str(payload["due_date"]).strip(),
            customer=str(payload.get("customer", "")).strip(),
            priority=str(payload.get("priority", "normal")).strip() or "normal",
            issuer=str(payload.get("issuer", "Factory Operations Office")).strip(),
            materials=[MaterialLine.from_dict(item) for item in payload.get("materials", [])],
            routing=[RoutingStep.from_dict(item) for item in payload.get("routing", [])],
            packaging=dict(payload.get("packaging", {})),
            quality=dict(payload.get("quality", {})),
            notes=[str(item) for item in payload.get("notes", [])],
        )

    def to_agent_context(self) -> dict[str, Any]:
        total_cycle = sum(step.cycle_time_sec for step in self.routing)
        required_materials = [
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
            "notice_id": self.notice_id,
            "work_order": self.work_order,
            "customer": self.customer,
            "product": {
                "item_code": self.product.item_code,
                "name": self.product.name,
                "model": self.product.model,
                "revision": self.product.revision,
            },
            "quantity": self.quantity,
            "due_date": self.due_date,
            "priority": self.priority,
            "routing_step_count": len(self.routing),
            "estimated_cycle_time_sec_per_unit": total_cycle,
            "required_materials": required_materials,
            "quality": self.quality,
            "packaging": self.packaging,
            "agent_recommended_checks": [
                "Validate required material quantity before releasing notice",
                "Confirm routing capacity against due date",
                "Review packaging and label rule for customer-specific constraints",
                "Escalate if required fields are missing or quantity is unusually high",
            ],
        }
