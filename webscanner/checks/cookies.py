from ..models.finding import Finding


def check_cookies(url, response):
    findings = []

    cookies = response.headers.get("Set-Cookie")

    if not cookies:
        return findings

    lower = cookies.lower()

    if "secure" not in lower:
        findings.append(
            Finding(
                title="Cookie without Secure attribute",
                severity="Medium",
                category="Cookies",
                url=url,
                description="A Set-Cookie response was observed without Secure.",
                recommendation="Use the Secure attribute for cookies sent over HTTPS.",
                evidence=cookies[:500]
            )
        )

    if "httponly" not in lower:
        findings.append(
            Finding(
                title="Cookie without HttpOnly attribute",
                severity="Medium",
                category="Cookies",
                url=url,
                description="A Set-Cookie response was observed without HttpOnly.",
                recommendation="Use HttpOnly when client-side JavaScript does not need the cookie.",
                evidence=cookies[:500]
            )
        )

    if "samesite" not in lower:
        findings.append(
            Finding(
                title="Cookie without SameSite attribute",
                severity="Low",
                category="Cookies",
                url=url,
                description="A Set-Cookie response was observed without SameSite.",
                recommendation="Configure an appropriate SameSite policy.",
                evidence=cookies[:500]
            )
        )

    return findings
