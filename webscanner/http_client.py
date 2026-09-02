from dataclasses import dataclass

@dataclass
class HttpResponse:
    url: str
    status: int
    headers: dict
    text: str
    elapsed_ms: float