import html


def write_html(findings, path, target):
    rows = []

    for finding in findings:
        rows.append(
            "<tr>"
            f"<td>{html.escape(finding.severity)}</td>"
            f"<td>{html.escape(finding.category)}</td>"
            f"<td>{html.escape(finding.title)}</td>"
            f"<td>{html.escape(finding.url)}</td>"
            f"<td>{html.escape(finding.description)}</td>"
            f"<td>{html.escape(finding.recommendation)}</td>"
            "</tr>"
        )

    table = "\n".join(rows)

    document = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>WebSCanner Security Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    background: #f5f5f5;
}}
.container {{
    background: white;
    padding: 30px;
    border-radius: 10px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
}}
th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
    vertical-align: top;
}}
th {{
    background: #eeeeee;
}}
</style>
</head>
<body>
<div class="container">
<h1>WebSCanner Security Report</h1>
<p><strong>Target:</strong> {html.escape(target)}</p>
<p><strong>Total findings:</strong> {len(findings)}</p>
<table>
<thead>
<tr>
<th>Severity</th>
<th>Category</th>
<th>Finding</th>
<th>URL</th>
<th>Description</th>
<th>Recommendation</th>
</tr>
</thead>
<tbody>
{table}
</tbody>
</table>
</div>
</body>
</html>
"""

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(document)
