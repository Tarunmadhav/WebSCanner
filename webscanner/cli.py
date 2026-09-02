import argparse
from pathlib import Path
from .config import ScanConfig
from .core.orchestrator import scan
from .reporting.json_report import save as save_json
from .reporting.html_report import save as save_html

def main():
    parser = argparse.ArgumentParser(
        description="WebSCanner passive and low-impact web security scanner"
    )
    parser.add_argument("target", help="HTTP/HTTPS target you are authorized to scan")
    parser.add_argument("--max-pages", type=int, default=25)
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--delay", type=float, default=0.15)
    parser.add_argument("--passive-only", action="store_true")
    parser.add_argument("--zap", action="store_true")
    parser.add_argument("--json", default="reports/report.json")
    parser.add_argument("--html", default="reports/report.html")
    args = parser.parse_args()

    config = ScanConfig(
        target=args.target,
        max_pages=args.max_pages,
        timeout=args.timeout,
        delay=args.delay,
        active=not args.passive_only,
        zap=args.zap
    )

    target, pages, findings = scan(config)
    data = save_json(args.json, target, findings, len(pages))
    save_html(args.html, data)

    print("Scanned:", target)
    print("Pages:", len(pages))
    print("Findings:", len(findings))
    print("JSON:", Path(args.json).resolve())
    print("HTML:", Path(args.html).resolve())