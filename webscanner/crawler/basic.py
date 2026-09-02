from collections import deque
import time
import requests
from bs4 import BeautifulSoup
from ..core.scope import same_origin, absolute

def crawl(session, start_url, max_pages=25, timeout=8.0, delay=0.15):
    queue = deque([start_url])
    seen = set()
    pages = []
    while queue and len(pages) < max_pages:
        url = queue.popleft()
        if url in seen:
            continue
        seen.add(url)
        try:
            response = session.get(
                url, timeout=timeout, allow_redirects=True
            )
        except requests.RequestException:
            continue
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type.lower():
            continue
        pages.append(response)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", href=True):
            candidate = absolute(response.url, tag["href"])
            if same_origin(start_url, candidate) and candidate not in seen:
                queue.append(candidate)
        if delay:
            time.sleep(delay)
    return pages