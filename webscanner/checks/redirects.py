from urllib.parse import urlparse
from ..models.finding import Finding

def check(resp):
    location = resp.headers.get("Location")
    if not location:
        return []
    p = urlparse(location)
    current = urlparse(resp.url)
    if p.scheme and p.netloc and p.netloc.lower() != current.netloc.lower():
        return [Finding(
            "External redirect observed", "low", resp.url,
            "The response redirects to a different origin.",
            "Location: " + location,
            "Validate redirect destinations against an allowlist.",
            "A10:2021", "redirect.external", "medium"
        )]
    return []