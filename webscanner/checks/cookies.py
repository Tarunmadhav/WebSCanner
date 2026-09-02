from ..models.finding import Finding

def check(resp):
    findings = []
    values = resp.headers.get("Set-Cookie", "")
    for raw in values.splitlines():
        if not raw.strip():
            continue
        name = raw.split("=", 1)[0].strip()
        low = raw.lower()
        if "secure" not in low:
            findings.append(Finding(
                "Cookie missing Secure attribute", "medium", resp.url,
                "A cookie was observed without Secure.",
                "Cookie: " + name,
                "Set Secure on sensitive cookies.",
                "A05:2021", "cookies.secure", "high"
            ))
        if "httponly" not in low:
            findings.append(Finding(
                "Cookie missing HttpOnly attribute", "medium", resp.url,
                "A cookie was observed without HttpOnly.",
                "Cookie: " + name,
                "Set HttpOnly on session cookies where client-side access is unnecessary.",
                "A05:2021", "cookies.httponly", "high"
            ))
        if "samesite" not in low:
            findings.append(Finding(
                "Cookie missing SameSite attribute", "low", resp.url,
                "A cookie was observed without SameSite.",
                "Cookie: " + name,
                "Set an appropriate SameSite value.",
                "A05:2021", "cookies.samesite", "medium"
            ))
    return findings