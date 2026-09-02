import requests

def build_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "WebSCanner/0.3.0 authorized-security-testing"
    })
    return session