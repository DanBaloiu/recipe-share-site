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
    messages.success(request, "Logged in successfully.")


def handle_logout(sender, request, user, **kwargs):
    """Show an informational message when a user logs out.

    Args:
        sender: signal sender (unused)
        request: HttpRequest instance
        user: the User that logged out
    """
    messages.info(request, "You have been logged out.")


# Connect handlers to Django auth signals.
user_logged_in.connect(handle_login)
user_logged_out.connect(handle_logout)
