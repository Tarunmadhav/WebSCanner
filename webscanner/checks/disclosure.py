from ..models.finding import Finding


def check_disclosure(url, response):
    findings = []

    server = response.headers.get("Server")
    powered = response.headers.get("X-Powered-By")

    if server:
        findings.append(
            Finding(
                title="Server information disclosure",
                severity="Low",
                category="Information Disclosure",
                url=url,
                description="The Server header exposes server information.",
                recommendation="Minimize unnecessary server technology disclosure.",
                evidence=f"Server: {server}"
            )
        )

    if powered:
        findings.append(
            Finding(
                title="Technology information disclosure",
                severity="Low",
                category="Information Disclosure",
                url=url,
                description="X-Powered-By exposes technology information.",
                recommendation="Remove unnecessary technology disclosure headers.",
                evidence=f"X-Powered-By: {powered}"
            )
        )

    return findings
