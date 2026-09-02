from urllib.parse import urlsplit, urlunsplit
from ..models.finding import Finding

RESOURCE_KEYS = {"id", "user", "userid", "account", "item", "file"}

def check(session, url, timeout=8.0):
    parsed = urlsplit(url)
    if not parsed.query:
        return []
    pieces = parsed.query.split("&")
    candidate = None
    for piece in pieces:
        key, sep, value = piece.partition("=")
        if sep and key.lower() in RESOURCE_KEYS and value:
            candidate = (key, value)
            break
    if not candidate:
        return []
    key, value = candidate
    alternate = "0" if value != "0" else "1"
    rebuilt = []
    for piece in pieces:
        k, sep, v = piece.partition("=")
        rebuilt.append(k + "=" + (alternate if k == key else v))
    test_url = urlunsplit((
        parsed.scheme, parsed.netloc, parsed.path,
        "&".join(rebuilt), parsed.fragment
    ))
    try:
        original = session.get(url, timeout=timeout, allow_redirects=True)
        alternate_response = session.get(test_url, timeout=timeout, allow_redirects=True)
    except Exception:
        return []
    if (
        original.status_code == 200 and
        alternate_response.status_code == 200 and
        abs(len(original.text) - len(alternate_response.text)) > 500
    ):
        return [Finding(
            "Heuristic access-control difference", "medium", test_url,
            "A resource-like identifier produced materially different public responses.",
            "Original length={} alternate length={}".format(
                len(original.text), len(alternate_response.text)
            ),
            "Enforce authorization for every object access and verify ownership server-side.",
            "A01:2021", "access_control.heuristic", "low"
        )]
    return []