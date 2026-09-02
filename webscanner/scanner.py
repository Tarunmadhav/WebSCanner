from urllib.parse import urlparse

from .config import ScanConfig
from .crawler.basic import crawl
from .checks.headers import check_headers
from .checks.cookies import check_cookies
from .checks.disclosure import check_disclosure
from .http_client import HttpClient


class Scanner:
    def __init__(self, config: ScanConfig):
        self.config = config
        self.client = HttpClient(config)

    def scan(self, target):
        parsed = urlparse(target)

        if parsed.scheme not in {"http", "https"}:
            raise ValueError(
                "Target must start with http:// or https://"
            )

        if not parsed.netloc:
            raise ValueError("Invalid target URL")

        responses = crawl(
            target,
            self.client,
            self.config.max_pages
        )

        findings = []

        for item in responses:
            url = item["url"]
            response = item["response"]

            findings.extend(check_headers(url, response))
            findings.extend(check_cookies(url, response))
            findings.extend(check_disclosure(url, response))

        return {
            "target": target,
            "scanned_urls": [
                item["url"]
                for item in responses
            ],
            "findings": findings
        }
