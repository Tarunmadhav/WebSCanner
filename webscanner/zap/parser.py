from ..models.finding import Finding

def parse_alerts(alerts):
    findings = []
    for alert in alerts:
        severity = {
            "3": "high",
            "2": "medium",
            "1": "low",
            "0": "info",
        }.get(str(alert.get("riskcode", "")), "info")
        findings.append(Finding(
            alert.get("alert", "ZAP alert"),
            severity,
            alert.get("url", ""),
            alert.get("description", ""),
            alert.get("evidence", "") or alert.get("otherinfo", ""),
            alert.get("solution", ""),
            "",
            "zap",
            "medium",
            0.0,
            {
                "pluginId": alert.get("pluginId", ""),
                "cweid": alert.get("cweid", ""),
            }
        ))
    return findings