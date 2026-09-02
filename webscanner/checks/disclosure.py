from ..models.finding import Finding

def check(resp):
    findings = []
    for header in ("Server", "X-Powered-By"):
        value = resp.headers.get(header)
        if value:
            findings.append(Finding(
                header + " disclosure", "low", resp.url,
                "The response exposes the " + header + " header.",
                header + ": " + value,
                "Reduce unnecessary technology and version disclosure.",
                "A05:2021", "disclosure.header", "high"
            ))
    return findings