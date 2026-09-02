REMEDIATION = {
    "Security Headers":
        "Review and configure appropriate HTTP security headers.",
    "Cookies":
        "Review Secure, HttpOnly and SameSite cookie attributes.",
    "Information Disclosure":
        "Minimize unnecessary technology and version disclosure.",
}


def get_guidance(category):
    return REMEDIATION.get(
        category,
        "Review the finding and apply appropriate security controls."
    )
