SEVERITY_ORDER = {
    "Informational": 0,
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}


def severity_score(severity):
    return SEVERITY_ORDER.get(severity, 0)
