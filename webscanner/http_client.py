import requests


class HttpClient:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": config.user_agent
        })

    def get(self, url):
        return self.session.get(
            url,
            timeout=self.config.timeout,
            allow_redirects=True
        )
