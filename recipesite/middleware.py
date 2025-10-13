"""Security-related middleware for HTTP response headers.

This lightweight middleware adds conservative security headers such as
``X-Content-Type-Options`` and a minimal ``Permissions-Policy``.  The goal
is to improve default security without breaking common third-party
resources (for example, Cloudinary-hosted images).

The middleware is intentionally small and safe to enable in production.
"""

from django.conf import settings


class SecurityHeadersMiddleware:
    """Middleware that sets a small set of response headers.

    The middleware intentionally uses ``response.setdefault`` so it does
    not override headers set earlier by other middleware or the application.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Apply headers to the response before returning it.

        Args:
            request: Django HttpRequest

        Returns:
            HttpResponse with additional security headers set.
        """

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
