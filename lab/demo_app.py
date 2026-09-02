from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import html

class Handler(BaseHTTPRequestHandler):
    def send_html(self, body, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Server", "DemoLab/1.0")
        self.send_header("X-Powered-By", "DemoFramework/1.0")
        self.send_header("Set-Cookie", "lab_session=demo123; Path=/")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        name = query.get("name", ["visitor"])[0]
        item = query.get("id", ["1"])[0]
        body = (
            "<html><body><h1>WebSCanner Demo</h1>"
            "<p>Hello " + name + "</p>"
            "<p>Item " + html.escape(item) + "</p>"
            '<a href="/?name=visitor&id=1">home</a>'
            "</body></html>"
        )
        self.send_html(body)

if __name__ == "__main__":
    print("Demo target: http://127.0.0.1:8765")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()