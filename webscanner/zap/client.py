import requests

class ZapClient:
    def __init__(self, base_url="http://127.0.0.1:8080", api_key=None, timeout=5):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def available(self):
        try:
            response = requests.get(
                self.base_url + "/JSON/core/view/version/",
                timeout=self.timeout
            )
            return response.ok
        except requests.RequestException:
            return False

    def alerts(self, base_url=None):
        params = {}
        if self.api_key:
            params["apikey"] = self.api_key
        if base_url:
            params["baseurl"] = base_url
        response = requests.get(
            self.base_url + "/JSON/core/view/alerts/",
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json().get("alerts", [])