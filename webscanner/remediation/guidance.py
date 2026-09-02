DEFAULTS = {
    "headers.missing": "Add the missing security header using a tested policy.",
    "cookies.secure": "Set Secure on sensitive cookies.",
    "cookies.httponly": "Set HttpOnly on session cookies when client-side access is unnecessary.",
    "cookies.samesite": "Set an appropriate SameSite value.",
    "disclosure.header": "Minimize unnecessary technology and version disclosure.",
    "cors.wildcard": "Restrict CORS origins where sensitive data is involved.",
    "xss.reflection": "Contextually encode output and validate input.",
    "injection.error": "Use parameterized queries and safe error handling.",
    "access_control.heuristic": "Enforce server-side authorization for every resource.",
    "redirect.external": "Validate redirect destinations.",
}