from ..models.finding import Finding

RULES = [
    ("Strict-Transport-Security", "Missing Strict-Transport-Security", "medium",
     "HSTS was not observed.", "Add an appropriate HSTS policy after HTTPS is correctly deployed.", "A05:2021"),
    ("Content-Security-Policy", "Missing Content-Security-Policy", "medium",
     "CSP was not observed.", "Deploy and test a restrictive Content-Security-Policy.", "A05:2021"),
    ("X-Content-Type-Options", "Missing X-Content-Type-Options", "low",
     "X-Content-Type-Options was not observed.", "Set X-Content-Type-Options: nosniff.", "A05:2021"),
    ("Referrer-Policy", "Missing Referrer-Policy", "low",
     "Referrer-Policy was not observed.", "Set an explicit Referrer-Policy.", "A05:2021"),
]

def check(resp):
    existing = {k.lower() for k in resp.headers}
    findings = []
    for header, title, severity, desc, remediation, owasp in RULES:
        if header.lower() not in existing:
            findings.append(Finding(
                title, severity, resp.url, desc,
                "Header absent: " + header, remediation, owasp,
                "headers.missing", "high"
            ))
    return findings