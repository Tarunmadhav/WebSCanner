from .client import ZapClient
from .parser import parse_alerts

def run_zap(target, base_url="http://127.0.0.1:8080", api_key=None):
    client = ZapClient(base_url, api_key)
    if not client.available():
        return []
    return parse_alerts(client.alerts(target))