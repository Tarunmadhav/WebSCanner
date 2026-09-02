from ..core.scope import normalize_target
from ..core.session import build_session
from ..crawler.basic import crawl
from ..checks import headers, cookies, disclosure, cors, redirects
from ..checks import xss, injection, access_control
from ..scoring.severity import risk_score
from ..zap.scanner import run_zap

def scan(config):
    target = normalize_target(config.target)
    session = build_session()
    pages = crawl(
        session,
        target,
        config.max_pages,
        config.timeout,
        config.delay
    )
    findings = []
    for response in pages:
        findings.extend(headers.check(response))
        findings.extend(cookies.check(response))
        findings.extend(disclosure.check(response))
        findings.extend(cors.check(response))
        findings.extend(redirects.check(response))
        if config.active:
            findings.extend(xss.check_reflection(session, response.url, config.timeout))
            findings.extend(injection.check(session, response.url, config.timeout))
            findings.extend(access_control.check(session, response.url, config.timeout))
    if config.zap:
        findings.extend(run_zap(target))
    for finding in findings:
        finding.risk_score = risk_score(
            finding.severity, finding.confidence
        )
    return target, pages, findings