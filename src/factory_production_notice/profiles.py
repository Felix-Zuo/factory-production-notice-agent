from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .io_utils import project_root, read_json


@dataclass(frozen=True)
class ScenarioProfile:
    id: str
    label: str
    notice_type: str
    domain: str
    artifact_focus: tuple[str, ...]
    review_gates: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ScenarioProfile":
        return cls(
            id=str(payload["id"]),
            label=str(payload["label"]),
            notice_type=str(payload["notice_type"]),
            domain=str(payload["domain"]),
            artifact_focus=tuple(str(item) for item in payload.get("artifact_focus", [])),
            review_gates=tuple(str(item) for item in payload.get("review_gates", [])),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "notice_type": self.notice_type,
            "domain": self.domain,
            "artifact_focus": list(self.artifact_focus),
            "review_gates": list(self.review_gates),
        }


def load_profiles() -> list[ScenarioProfile]:
    payload = read_json(project_root() / "config" / "scenario_profiles.json")
    profiles = payload.get("profiles", [])
    if not isinstance(profiles, list):
        raise ValueError("config/scenario_profiles.json must contain a profiles array")
    return [ScenarioProfile.from_dict(item) for item in profiles]


def profile_catalog() -> dict[str, Any]:
    profiles = [profile.as_dict() for profile in load_profiles()]
    return {"profiles": profiles, "count": len(profiles)}
