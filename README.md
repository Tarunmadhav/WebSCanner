# WebSCanner

------------------------------------------------------------------------

## 1. What is WebSCanner?

WebSCanner is a modular web-application vulnerability scanner designed
to automatically discover pages and endpoints within an authorized web
application, inspect HTTP responses, perform passive security checks,
and run selected low-impact active heuristics.

The scanner converts observations into structured security findings
containing:

-   Vulnerability title and description
-   Severity and confidence
-   Risk score
-   OWASP Top 10 mapping
-   Affected URL
-   Evidence
-   Remediation guidance
-   Detection source

Reports can be generated in **JSON** and **HTML** formats.

> **Important:** WebSCanner is intended only for applications that you
> own or have explicit permission to test. Active checks are
> deliberately controlled and low-impact.

------------------------------------------------------------------------

## 2. Project Goals

WebSCanner is designed to demonstrate a complete vulnerability-scanning
workflow rather than a collection of unrelated checks.

### Core goals

1.  Discover application pages automatically.
2.  Stay within the target's same-origin scope.
3.  Reuse an HTTP session for consistent requests.
4.  Detect common security weaknesses.
5.  Normalize all results into a common finding model.
6.  Map findings to OWASP categories.
7.  Calculate severity, confidence, and risk.
8.  Preserve useful evidence for every finding.
9.  Provide actionable remediation guidance.
10. Produce professional machine-readable and human-readable reports.
11. Support optional OWASP ZAP findings.
12. Evaluate the scanner against a controlled local demonstration
    application.

------------------------------------------------------------------------

# 3. Architecture

## 3.1 High-Level Architecture

``` text
                         +----------------------+
                         |      Target URL      |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |  Scope & Config      |
                         |  - URL validation    |
                         |  - same-origin rule  |
                         |  - scan limits       |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |       Crawler        |
                         |  - BFS traversal     |
                         |  - link discovery    |
                         |  - page collection   |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |     HTTP Client      |
                         |  - requests.Session  |
                         |  - timeout           |
                         |  - delay             |
                         +----------+-----------+
                                    |
                                    v
              +---------------------+---------------------+
              |                                           |
              v                                           v
   +-------------------------+                +-------------------------+
   |   Passive Detection     |                | Controlled Active       |
   |                         |                | Detection               |
   | - Headers               |                | - Reflected input       |
   | - Cookies               |                | - Injection indicators |
   | - Disclosure            |                | - Access-control        |
   | - CORS                  |                |   heuristics             |
   | - Redirects             |                |                         |
   +------------+------------+                +------------+------------+
                |                                          |
                +-------------------+----------------------+
                                    |
                                    v
                         +----------------------+
                         | Optional ZAP Layer   |
                         | - ZAP API client     |
                         | - ZAP result parser  |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |  Finding Manager      |
                         | - Finding model       |
                         | - OWASP mapping       |
                         | - Severity            |
                         | - Confidence          |
                         | - Risk score          |
                         | - Evidence            |
                         | - Remediation         |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |      Reporting       |
                         | - JSON               |
                         | - HTML               |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         | Evaluation / Demo    |
                         | - Coverage            |
                         | - Reliability         |
                         | - False positives     |
                         +----------------------+
```

------------------------------------------------------------------------

## 3.2 Data Flow

``` text
Target
  |
  v
Validate + Normalize
  |
  v
Create Scan Configuration
  |
  v
Crawl Same-Origin Pages
  |
  v
Collect HTTP Responses
  |
  +----> Passive Checks
  |
  +----> Controlled Active Checks
  |
  +----> Optional ZAP Findings
              |
              v
        Normalize Findings
              |
              v
       Score + Classify
              |
              v
       Attach Evidence
              |
              v
     Add Remediation Advice
              |
              v
       Generate Reports
```

------------------------------------------------------------------------

# 4. Design Principles

## 4.1 Modular Design

Each major scanner responsibility is separated into its own module.

``` text
Scope
  -> Crawler
  -> HTTP Client
  -> Detection Checks
  -> Finding Model
  -> Scoring
  -> Evidence
  -> Remediation
  -> Reporting
```

This makes individual checks easier to test, replace, and extend.

## 4.2 Safety by Design

WebSCanner does not attempt unrestricted exploitation.

The active checks use controlled techniques such as:

-   Unique harmless reflection markers
-   Generic injection-error indicators
-   Heuristic comparisons
-   No destructive database queries
-   No command execution
-   No brute-force authentication bypass
-   No denial-of-service behavior

The scanner should always be used against authorized targets.

## 4.3 Scope Control

The crawler follows same-origin URLs by default.

For example, if the target is:

``` text
https://example.test
```

the crawler can follow:

``` text
https://example.test/login
https://example.test/products
https://example.test/about
```

but should not automatically leave the target origin for unrelated
hosts.

## 4.4 Evidence-Based Findings

A finding should contain enough evidence to explain why it was reported.

Typical evidence can include:

-   URL
-   HTTP status
-   Header value
-   Cookie attribute
-   Response fragment
-   Detection reason
-   Confidence

This makes the report more useful for debugging and remediation.

------------------------------------------------------------------------

# 5. Detection Architecture

## 5.1 Passive Checks

Passive checks inspect information already returned by the application.

### Security Headers

The scanner checks for important browser security controls such as:

-   Strict-Transport-Security
-   Content-Security-Policy
-   X-Content-Type-Options
-   Referrer-Policy

### Cookie Security

The scanner evaluates cookie attributes including:

-   `Secure`
-   `HttpOnly`
-   `SameSite`

### Information Disclosure

The scanner looks for unnecessary technology or server information such
as:

-   `Server`
-   `X-Powered-By`

### CORS

The scanner evaluates suspicious cross-origin response behavior,
particularly overly permissive origin handling.

### Redirects

The scanner evaluates redirect behavior and records potentially
interesting redirect characteristics.

------------------------------------------------------------------------

# 6. Controlled Active Checks

## 6.1 Reflected Input / XSS Heuristic

The scanner can submit a harmless unique marker through supported input
points and check whether that marker is reflected in the response.

Conceptually:

``` text
Input
  |
  v
Unique marker
  |
  v
Application
  |
  v
HTTP response
  |
  v
Marker reflected?
  |
  +---- Yes ---> Potential reflected-input finding
  |
  +---- No ----> No reflection detected
```

This is a **heuristic**, not proof of exploitability.

## 6.2 Injection Error Indicators

The scanner can use controlled input strings and look for generic
database/parser error indicators.

Examples of indicator categories include:

-   SQL/database error messages
-   Parser errors
-   Database driver errors

The scanner does not execute destructive queries.

## 6.3 Access-Control Heuristic

The access-control module provides a limited heuristic based on
observable response behavior.

It is not an authentication bypass engine and does not attempt
brute-force authorization testing.

------------------------------------------------------------------------

# 7. Finding Model

All detection modules produce a common finding structure.

Conceptually:

``` text
Finding
├── title
├── description
├── severity
├── confidence
├── risk_score
├── category
├── OWASP mapping
├── URL
├── evidence
├── remediation
└── source
```

This standardization allows findings from different detectors to be
processed by the same reporting pipeline.

------------------------------------------------------------------------

# 8. Severity and Risk

WebSCanner separates **severity** from **confidence**.

### Severity

Represents the potential impact of the issue.

Typical levels:

``` text
Critical
High
Medium
Low
Info
```

### Confidence

Represents how strongly the scanner's evidence supports the finding.

This distinction is important because a heuristic detector may identify
something interesting without proving exploitability.

The final risk score combines these concepts to help prioritize
findings.

------------------------------------------------------------------------

# 9. OWASP Mapping

WebSCanner associates relevant findings with OWASP Top 10 categories
where an appropriate mapping exists.

The mapping layer is intentionally separated from the detection code:

``` text
Detector
   |
   v
Finding
   |
   v
OWASP Mapping
   |
   v
Severity / Risk
   |
   v
Report
```

This allows detection logic and security taxonomy to evolve
independently.

------------------------------------------------------------------------

# 10. Evidence and Remediation

## Evidence

Evidence explains what the scanner observed.

For example:

``` text
URL:
https://target.example/login

Observation:
X-Content-Type-Options header was not present.

Confidence:
High
```

## Remediation

Every meaningful finding should provide practical remediation guidance.

Examples:

-   Configure missing security headers.
-   Restrict CORS to trusted origins.
-   Add appropriate cookie security attributes.
-   Remove unnecessary server disclosure.
-   Validate and encode user-controlled input.
-   Apply server-side authorization checks.

------------------------------------------------------------------------

# 11. Reporting

WebSCanner supports two primary report formats.

## JSON Report

Designed for:

-   Automation
-   Evaluation
-   CI pipelines
-   Machine processing
-   Future dashboards

Example:

``` text
reports/
└── report.json
```

## HTML Report

Designed for:

-   Human review
-   Demonstrations
-   Academic evaluation
-   Security findings presentation

Example:

``` text
reports/
└── report.html
```

The HTML report organizes findings into a readable security assessment.

------------------------------------------------------------------------

# 12. Project Structure

``` text
WebSCanner/
│
├── webscanner/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   ├── http_client.py
│   │
│   ├── core/
│   │   ├── scope.py
│   │   ├── session.py
│   │   └── orchestrator.py
│   │
│   ├── crawler/
│   │   └── basic.py
│   │
│   ├── checks/
│   │   ├── headers.py
│   │   ├── cookies.py
│   │   ├── disclosure.py
│   │   ├── cors.py
│   │   ├── redirects.py
│   │   ├── xss.py
│   │   ├── injection.py
│   │   └── access_control.py
│   │
│   ├── models/
│   │   └── finding.py
│   │
│   ├── scoring/
│   │   └── severity.py
│   │
│   ├── owasp/
│   │   ├── mappings.py
│   │   └── top10.py
│   │
│   ├── evidence/
│   │   └── collector.py
│   │
│   ├── remediation/
│   │   └── guidance.py
│   │
│   ├── zap/
│   │   ├── client.py
│   │   ├── parser.py
│   │   └── scanner.py
│   │
│   └── reporting/
│       ├── json_report.py
│       └── html_report.py
│
├── lab/
│   └── demo_app.py
│
├── evaluation/
│   └── evaluate_demo.py
│
├── tests/
│   ├── test_scope.py
│   ├── test_scoring.py
│   └── test_imports.py
│
├── reports/
│   ├── report.json
│   ├── report.html
│   ├── demo_report.json
│   └── evaluation.json
│
├── docs/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
├── PROJECT_INFO.md
├── THIRD_PARTY_NOTICES.md
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

# 13. Installation

## Requirements

-   Windows 10/11
-   Python 3.11 or newer
-   Git
-   Internet access for installing Python dependencies
-   Optional: OWASP ZAP for ZAP-assisted scanning

Check Python:

``` powershell
python --version
```

Check Git:

``` powershell
git --version
```

------------------------------------------------------------------------

## Create Virtual Environment

From the project directory:

``` powershell
cd E:\WEBBIEE\WebSCanner
```

Create the environment:

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

``` powershell
python -m pip install -r requirements.txt
```

------------------------------------------------------------------------

# 14. How to Run

## Show CLI Help

``` powershell
python -m webscanner --help
```

------------------------------------------------------------------------

## Basic Scan

``` powershell
python -m webscanner https://example.com
```

Use only an authorized target.

------------------------------------------------------------------------

## Limit the Number of Pages

``` powershell
python -m webscanner https://example.com --max-pages 10
```

------------------------------------------------------------------------

## Set Request Timeout

``` powershell
python -m webscanner https://example.com --timeout 10
```

------------------------------------------------------------------------

## Add Request Delay

``` powershell
python -m webscanner https://example.com --delay 0.5
```

This can reduce request pressure on the target.

------------------------------------------------------------------------

## Passive-Only Scan

For the safest basic assessment:

``` powershell
python -m webscanner https://example.com --passive-only
```

------------------------------------------------------------------------

## Generate JSON

``` powershell
python -m webscanner https://example.com --json reports/report.json
```

------------------------------------------------------------------------

## Generate HTML

``` powershell
python -m webscanner https://example.com --html reports/report.html
```

------------------------------------------------------------------------

## Generate Both

``` powershell
python -m webscanner https://example.com --json reports/report.json --html reports/report.html
```

------------------------------------------------------------------------

## Optional ZAP Integration

If OWASP ZAP is configured and available:

``` powershell
python -m webscanner https://example.com --zap
```

ZAP is an optional detection source. WebSCanner remains the primary
orchestration, normalization, scoring, evidence, and reporting layer.

------------------------------------------------------------------------

# 15. Recommended First Run

After installation, use a passive scan first:

``` powershell
cd E:\WEBBIEE\WebSCanner
.\.venv\Scripts\Activate.ps1
python -m webscanner --help
python -m webscanner https://example.com --passive-only --max-pages 3 --json reports/report.json --html reports/report.html
```

Then inspect:

``` text
reports/report.json
reports/report.html
```

------------------------------------------------------------------------

# 16. Controlled Local Demo

The repository includes a small local demonstration application for
testing and evaluation.

Run:

``` powershell
python lab/demo_app.py
```

The demo is intended to provide controlled security characteristics that
can be detected by WebSCanner.

In another terminal, scan the local application using the appropriate
local URL exposed by the demo.

This provides a reproducible environment without testing an unrelated
third-party application.

------------------------------------------------------------------------

# 17. Evaluation

The evaluation component is intended to measure scanner behavior against
the controlled demo.

Run:

``` powershell
python evaluation/evaluate_demo.py
```

The evaluation can produce:

``` text
reports/demo_report.json
reports/evaluation.json
```

Evaluation areas include:

-   Detection coverage
-   Expected findings
-   False-positive observations
-   Reliability
-   Remediation quality

The evaluation environment should remain controlled and reproducible.

------------------------------------------------------------------------

# 18. Testing

Run the automated test suite:

``` powershell
python -m pytest -q
```

Run Python compilation checks:

``` powershell
python -m compileall webscanner
```

Run CLI validation:

``` powershell
python -m webscanner --help
```

These checks are also suitable for continuous integration.

------------------------------------------------------------------------

# 19. Continuous Integration

GitHub Actions can automatically validate the project.

The CI workflow is located at:

``` text
.github/workflows/ci.yml
```

The workflow is intended to verify that:

1.  Python is available.
2.  Dependencies install correctly.
3.  The package compiles.
4.  Automated tests pass.

This helps prevent broken changes from being pushed to the repository.

------------------------------------------------------------------------

# 20. Strix Relationship and Attribution

WebSCanner is an **original student capstone implementation inspired by
the high-level architecture and ideas of Strix**.

It should not be represented as:

-   A renamed Strix repository
-   A fork of Strix
-   A direct copy of Strix
-   An official Strix project

The architectural inspiration is limited to concepts such as modular
scanning, orchestration, multiple detection sources, evidence handling,
and structured reporting.

Where third-party source code is actually incorporated, the applicable
license and attribution requirements must be preserved and documented
in:

``` text
THIRD_PARTY_NOTICES.md
```

------------------------------------------------------------------------

# 21. Security and Ethical Use

WebSCanner is a security testing tool.

Use it only when you have explicit authorization.

### Allowed use

-   Your own web applications
-   Local laboratory applications
-   Academic test environments
-   Authorized penetration-testing engagements
-   Deliberately vulnerable applications used for learning

### Do not use it to

-   Scan systems without permission
-   Circumvent access controls
-   Steal credentials
-   Perform destructive exploitation
-   Attack third-party infrastructure
-   Conduct denial-of-service activity

The scanner's controlled active checks are intentionally designed to
reduce unnecessary impact.

------------------------------------------------------------------------

# 22. Limitations

WebSCanner is an academic and engineering project, not a replacement for
a full commercial penetration-testing platform.

Important limitations include:

-   Detection is partly heuristic.
-   Reflected-input detection does not prove exploitable XSS.
-   Injection indicators do not prove successful database exploitation.
-   Access-control analysis is heuristic.
-   Crawler coverage depends on discoverable links.
-   JavaScript-heavy applications may require additional crawling
    support.
-   Authenticated scanning requires further session/authentication
    handling.
-   Complex APIs may require specialized endpoint discovery.
-   False positives and false negatives are possible.
-   ZAP integration is optional.

The scanner should therefore be treated as a security-assessment aid
rather than absolute proof that an application is secure.

------------------------------------------------------------------------

# 23. Future Enhancements

Potential future work includes:

-   JavaScript-aware crawling
-   API/OpenAPI discovery
-   Authentication/session support
-   Better parameter discovery
-   Form-aware scanning
-   More OWASP checks
-   Improved XSS analysis
-   SQL injection confirmation workflows
-   SSRF detection
-   CSRF analysis
-   Security misconfiguration detection
-   Screenshot/evidence capture
-   PDF reporting
-   Dashboard UI
-   Database-backed scan history
-   Parallel scanning with safe rate limits
-   More comprehensive benchmark datasets
-   Improved false-positive reduction

------------------------------------------------------------------------

# 24. End-to-End Workflow

``` text
1. User supplies authorized target
              |
              v
2. Scope validation
              |
              v
3. Scanner configuration
              |
              v
4. Same-origin crawling
              |
              v
5. HTTP response collection
              |
              v
6. Passive security checks
              |
              v
7. Controlled active checks
              |
              v
8. Optional ZAP integration
              |
              v
9. Finding normalization
              |
              v
10. OWASP classification
              |
              v
11. Severity + confidence
              |
              v
12. Risk scoring
              |
              v
13. Evidence collection
              |
              v
14. Remediation guidance
              |
              v
15. JSON + HTML reporting
              |
              v
16. Evaluation and review
```

------------------------------------------------------------------------

# 25. Example Project Output

A completed scan is expected to provide a result similar to:

``` text
WebSCanner
   |
   +-- Target: https://authorized-target.example
   |
   +-- Pages discovered: 12
   |
   +-- Findings
   |      +-- Missing security header
   |      +-- Cookie security issue
   |      +-- Information disclosure
   |      +-- CORS observation
   |      +-- Reflected-input observation
   |
   +-- Risk classification
   |
   +-- Evidence
   |
   +-- Remediation guidance
   |
   +-- reports/report.json
   +-- reports/report.html
```

The exact findings depend on the target and should never be fabricated.

------------------------------------------------------------------------

# 26. Quick Start

``` powershell
cd E:\WEBBIEE\WebSCanner

.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

python -m webscanner --help

python -m webscanner https://example.com `
    --passive-only `
    --max-pages 3 `
    --json reports/report.json `
    --html reports/report.html

python -m pytest -q
```

------------------------------------------------------------------------

# 27. Project Status

WebSCanner currently provides the foundation for a modular automated
web-application vulnerability scanner with:

-   Scope control
-   Same-origin crawling
-   HTTP session handling
-   Passive security checks
-   Controlled active heuristics
-   Finding normalization
-   OWASP mapping
-   Severity and risk scoring
-   Evidence collection
-   Remediation guidance
-   Optional ZAP integration
-   JSON reporting
-   HTML reporting
-   Local demonstration environment
-   Automated evaluation
-   Automated tests
-   GitHub Actions CI

------------------------------------------------------------------------

## License and Third-Party Components

See:

-   `PROJECT_INFO.md`
-   `THIRD_PARTY_NOTICES.md`

for project information, architecture notes, attribution, and
third-party licensing details.
