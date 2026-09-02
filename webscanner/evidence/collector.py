def collect(response):
    return {
        "url": response.url,
        "status": response.status_code,
        "headers": dict(response.headers),
        "body_length": len(response.text or ""),
    }