WEIGHTS = {
    "critical": 10.0,
    "high": 8.0,
    "medium": 5.0,
    "low": 2.0,
    "info": 0.5,
}

def risk_score(severity, confidence="medium"):
    factor = {"high": 1.0, "medium": 0.8, "low": 0.6}.get(confidence, 0.8)
    return round(WEIGHTS.get(severity.lower(), 0.5) * factor, 2)