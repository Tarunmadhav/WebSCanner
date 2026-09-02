import argparse
from pathlib import Path

from colorama import Fore, Style, init

from .config import ScanConfig
from .scanner import Scanner
from .reporting.json_report import write_json
from .reporting.html_report import write_html


def main():
    init()

    parser = argparse.ArgumentParser(
        description="WebSCanner passive web security scanner"
    )

    parser.add_argument(
        "target",
        help="HTTP/HTTPS target you are authorized to scan"
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=25,
        help="Maximum number of same-origin pages to scan"
    )

    args = parser.parse_args()

    print()
    print(Fore.CYAN + "===================================")
    print("           WebSCANNER")
    print("===================================" + Style.RESET_ALL)
    print()

    print(f"Target: {args.target}")
    print(f"Maximum pages: {args.max_pages}")
    print()

    scanner = Scanner(
        ScanConfig(max_pages=args.max_pages)
    )

    try:
        result = scanner.scan(args.target)
    except Exception as exc:
        print(
            Fore.RED +
            f"Scan failed: {exc}" +
            Style.RESET_ALL
        )
        raise SystemExit(1)

    findings = result["findings"]

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_file = output_dir / "report.json"
    html_file = output_dir / "report.html"

    write_json(findings, json_file)
    write_html(findings, html_file, args.target)

    print()
    print(
        Fore.GREEN +
        f"Pages scanned: {len(result['scanned_urls'])}" +
        Style.RESET_ALL
    )

    print(
        Fore.YELLOW +
        f"Findings: {len(findings)}" +
        Style.RESET_ALL
    )

    print()
    print(f"JSON report: {json_file}")
    print(f"HTML report: {html_file}")
    print()


if __name__ == "__main__":
    main()
