from ..models.finding import Finding

ERROR_MARKERS = (
    "sql syntax", "sqlite error", "mysql", "postgresql",
    "odbc", "ora-", "syntax error at or near",
    "unclosed quotation mark"
)

def check(session, url, timeout=8.0):
    if "?" not in url:
        return []
    base, query = url.split("?", 1)
    first = query.split("&", 1)[0]
    key = first.split("=", 1)[0]
    if not key:
        return []
    test_url = base + "?" + key + "=%27"
    try:
        response = session.get(test_url, timeout=timeout, allow_redirects=True)
    except Exception:
        return []
    body = response.text.lower()
    hits = [x for x in ERROR_MARKERS if x in body]
    if not hits:
        return []
    return [Finding(
        "Potential injection error indicator", "medium", test_url,
        "A controlled quote test produced a generic database or parser error indicator.",
        "Indicators: " + ", ".join(hits[:3]),
        "Use parameterized queries and safe error handling; manually verify.",
        "A03:2021", "injection.error", "low"
    )]