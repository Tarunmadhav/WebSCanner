import json
import subprocess
import sys
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DEMO_JSON = REPORTS / "demo_report.json"
DEMO_HTML = REPORTS / "demo_report.html"
EVAL_JSON = REPORTS / "evaluation.json"

def main():
    REPORTS.mkdir(exist_ok=True)
    process = subprocess.Popen([sys.executable, "-m", "lab.demo_app"])
    try:
        time.sleep(1)
        subprocess.run([
            sys.executable, "-m", "webscanner",
            "http://127.0.0.1:8765",
            "--max-pages", "5",
            "--json", str(DEMO_JSON),
            "--html", str(DEMO_HTML)
        ], check=True)
        data = json.loads(DEMO_JSON.read_text(encoding="utf-8"))
        expected = {
            "headers.missing",
            "cookies.secure",
            "disclosure.header",
            "cors.wildcard",
            "xss.reflection",
        }
        found = {f["check_id"] for f in data["findings"]}
        detected = len(expected & found)
        result = {
            "expected_checks": sorted(expected),
            "detected_expected": detected,
            "coverage_ratio": round(detected / len(expected), 3),
            "finding_count": data["finding_count"],
        }
        EVAL_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    main()