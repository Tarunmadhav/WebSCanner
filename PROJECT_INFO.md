# WebSCanner

Automated Web-Application Vulnerability Scanner

Batch: C2C-109

The project is intended for authorized and controlled security testing.

Architecture:
Target -> Scope -> Crawler -> HTTP Client -> Detection Engine ->
Finding Manager -> OWASP/Severity/Evidence/Remediation -> Reporting -> Evaluation.

Active checks are deliberately low-impact. They use harmless markers, controlled
test strings, and heuristics. No destructive queries, command execution,
brute force, or authentication bypass is implemented.