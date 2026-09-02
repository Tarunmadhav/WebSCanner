from urllib.parse import urlparse, urljoin, urldefrag

def normalize_target(target: str) -> str:
    target = target.strip()
    if not target.startswith(("http://", "https://")):
        target = "https://" + target
    p = urlparse(target)
    if p.scheme not in ("http", "https") or not p.netloc:
        raise ValueError("Target must be a valid HTTP or HTTPS URL")
    return target.rstrip("/")

def same_origin(base: str, candidate: str) -> bool:
    a, b = urlparse(base), urlparse(candidate)
    return (a.scheme, a.netloc.lower()) == (b.scheme, b.netloc.lower())

def absolute(base: str, href: str) -> str:
    return urldefrag(urljoin(base, href))[0]