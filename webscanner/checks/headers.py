from ..models.finding import Finding


def check_headers(url, response):
    findings = []

    required = {
        "Strict-Transport-Security": (
            "Medium",
            "HSTS was not observed.",
            "Enable Strict-Transport-Security for HTTPS applications."
        ),
        "Content-Security-Policy": (
            "Medium",
            "Content-Security-Policy was not observed.",
            "Define a restrictive Content-Security-Policy."
        ),
        "X-Content-Type-Options": (
            "Low",
            "X-Content-Type-Options was not observed.",
            "Set X-Content-Type-Options to nosniff."
        ),
        "Referrer-Policy": (
            "Low",
            "Referrer-Policy was not observed.",
            "Configure an appropriate Referrer-Policy."
        ),
    }

    for header, values in required.items():
        if not response.headers.get(header):
            severity, description, recommendation = values

            findings.append(
                Finding(
                    title=f"Missing security header: {header}",
                    severity=severity,
                    category="Security Headers",
                    url=url,
                    description=description,
                    recommendation=recommendation,
                    evidence=f"{header} header was not present."
                )
            )

    return findings
