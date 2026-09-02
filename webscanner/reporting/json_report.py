import json
from pathlib import Path

def save(path, target, findings, pages=0):
    data = {
        "tool": "WebSCanner",
        "version": "0.3.0",
        "target": target,
        "pages": pages,
        "finding_count": len(findings),
        "findings": [finding.to_dict() for finding in findings],
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )
    return data