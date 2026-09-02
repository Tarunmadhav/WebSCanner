import uuid
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from ..models.finding import Finding

def check_reflection(session, url, timeout=8.0):
    parts = urlsplit(url)
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    if not pairs:
        return []
    marker = "WSCANNER_" + uuid.uuid4().hex[:10]
    for index, (key, _) in enumerate(pairs):
        changed = list(pairs)
        changed[index] = (key, marker)
        test_url = urlunsplit((
            parts.scheme, parts.netloc, parts.path,
            urlencode(changed), parts.fragment
        ))
        try:
            response = session.get(test_url, timeout=timeout, allow_redirects=True)
        except Exception:
            continue
        if marker in response.text:
            return [Finding(
                "Potential reflected input", "medium", test_url,
                "A harmless unique marker was reflected in the response.",
                "Reflected marker: " + marker,
                "Contextually encode output and validate input; manually confirm.",
                "A03:2021", "xss.reflection", "medium"
            )]
    return []