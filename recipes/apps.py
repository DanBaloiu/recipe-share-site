"""Application configuration for the recipes app.

This module exposes the :class:`RecipesConfig` AppConfig used by Django to
perform app-specific initialization such as registering signal handlers.
"""

from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Django AppConfig for the `recipes` app.

    When the app is ready we import ``recipes.signals`` which registers
    handlers for user login/logout messaging.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'

    def ready(self):
        """Register signal handlers when the app is loaded.

        Import is local to avoid import-time side-effects when Django is
        collecting app configurations.
        """
        # register signal handlers
        from . import signals  # noqa: F401
