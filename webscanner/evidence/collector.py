def collect_evidence(url, response):
    return {
        "url": url,
        "status_code": response.status_code,
        "headers": dict(response.headers),
    }
