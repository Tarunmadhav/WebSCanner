from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Finding:
    title: str
    severity: str
    category: str
    url: str
    description: str
    recommendation: str
    evidence: Optional[str] = None

    def to_dict(self):
        return asdict(self)
