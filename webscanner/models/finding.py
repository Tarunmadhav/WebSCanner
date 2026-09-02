from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Finding:
    title: str
    severity: str
    url: str
    description: str
    evidence: str = ""
    remediation: str = ""
    owasp: str = ""
    check_id: str = ""
    confidence: str = "medium"
    risk_score: float = 0.0
    extra: dict[str, Any] | None = None

    def to_dict(self):
        data = asdict(self)
        data["extra"] = data["extra"] or {}
        return data