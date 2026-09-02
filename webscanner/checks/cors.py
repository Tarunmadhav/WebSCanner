from ..models.finding import Finding

def check(resp):
    value = resp.headers.get("Access-Control-Allow-Origin")
    if value == "*":
        return [Finding(
            "Wildcard CORS policy", "medium", resp.url,
            "Access-Control-Allow-Origin is wildcard.",
            "Access-Control-Allow-Origin: *",
            "Restrict origins when cross-origin access can expose sensitive data.",
            "A05:2021", "cors.wildcard", "medium"
        )]
    return []