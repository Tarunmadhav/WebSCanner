from collections import deque
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


def crawl(target, client, max_pages):
    parsed_target = urlparse(target)

    target_origin = (
        parsed_target.scheme,
        parsed_target.netloc.lower()
    )

    queue = deque([target])
    visited = set()
    results = []

    while queue and len(results) < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        try:
            response = client.get(url)
        except requests.RequestException:
            continue
        except Exception:
            continue

        results.append({
            "url": url,
            "response": response
        })

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        if "text/html" not in content_type:
            continue

        try:
            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )
        except Exception:
            continue

        for link in soup.find_all("a", href=True):
            next_url = urljoin(
                response.url,
                link.get("href")
            )

            parsed = urlparse(next_url)

            if parsed.scheme not in {
                "http",
                "https"
            }:
                continue

            origin = (
                parsed.scheme,
                parsed.netloc.lower()
            )

            if origin != target_origin:
                continue

            clean_url = next_url.split("#")[0]

            if clean_url not in visited:
                queue.append(clean_url)

    return results
