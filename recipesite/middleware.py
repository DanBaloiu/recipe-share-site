"""Lightweight middleware to add security headers to all responses.

Keep headers conservative to avoid breaking third-party resources (e.g. Cloudinary).
"""
from django.conf import settings


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Prevent MIME-sniffing
        response.setdefault("X-Content-Type-Options", "nosniff")

        # Stronger referrer policy
        response.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")

        # Minimal permissions policy: disable powerful features by default
        response.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), interest-cohort=()",
        )

        # XSS protection header (legacy; harmless fallback)
        response.setdefault("X-XSS-Protection", "1; mode=block")

        return response
