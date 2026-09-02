from dataclasses import dataclass

@dataclass
class ScanConfig:
    target: str
    max_pages: int = 25
    timeout: float = 8.0
    delay: float = 0.15
    active: bool = True
    zap: bool = False