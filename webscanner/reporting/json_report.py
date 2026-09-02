import json


def write_json(findings, path):
    data = [
        finding.to_dict()
        for finding in findings
    ]

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
