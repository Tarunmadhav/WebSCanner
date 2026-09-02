from html import escape
from pathlib import Path

def save(path, data):
    rows = []
    for finding in data["findings"]:
        rows.append(
            "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><pre>{}</pre></td></tr>".format(
                escape(finding["severity"].upper()),
                escape(finding["title"]),
                escape(finding["owasp"]),
                escape(finding["url"]),
                escape(finding["evidence"])
            )
        )
    body = "".join(rows) or "<tr><td colspan='5'>No findings</td></tr>"
    html = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>WebSCanner Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 8px; vertical-align: top; }}
th {{ background: #eee; }}
pre {{ white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>WebSCanner Report</h1>
<p><b>Target:</b> {target}</p>
<p><b>Pages:</b> {pages} <b>Findings:</b> {count}</p>
<table>
<tr><th>Severity</th><th>Title</th><th>OWASP</th><th>URL</th><th>Evidence</th></tr>
{body}
</table>
</body>
</html>
""".format(
        target=escape(data["target"]),
        pages=data["pages"],
        count=data["finding_count"],
        body=body
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(html, encoding="utf-8")