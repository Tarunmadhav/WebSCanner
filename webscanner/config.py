from dataclasses import dataclass


@dataclass
class ScanConfig:
    max_pages: int = 25
    timeout: int = 10
    user_agent: str = "WebSCanner/1.0"
