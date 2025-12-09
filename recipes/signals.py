"""Simple user session signals for UX messaging.

Handlers in this module attach to Django's authentication signals and add
flash messages when users log in or out.  The handlers are connected at
import-time so that ``RecipesConfig.ready`` can safely import this
module to register them.
"""

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib import messages


def handle_login(sender, request, user, **kwargs):
    """Show a success message when a user logs in.

    Args:
        sender: signal sender (unused)
        request: HttpRequest instance
        user: the authenticated User instance
    """
    try:
        messages.success(request, "Logged in successfully.")
    except Exception:
        # In test environments the request may not have message storage
        # (middleware not applied to the login signal request). Avoid
        # raising during automated tests by swallowing message failures.
        pass


def handle_logout(sender, request, user, **kwargs):
    """Show an informational message when a user logs out.

    Args:
        sender: signal sender (unused)
        request: HttpRequest instance
        user: the User that logged out
    """
    try:
        messages.info(request, "You have been logged out.")
    except Exception:
        # Same defensive behaviour as handle_login
        pass


# Connect handlers to Django auth signals.
user_logged_in.connect(handle_login)
user_logged_out.connect(handle_logout)
