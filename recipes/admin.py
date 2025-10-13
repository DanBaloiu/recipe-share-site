"""Admin registrations/config for the ``recipes`` app models.

This module registers the primary models with Django admin and documents
the basic admin configuration used for each model.
"""

from django.contrib import admin

from .models import Recipe, Comment, Rating


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin configuration for :class:`recipes.models.Recipe`.

    Shows title/author/status in list view and prepopulates the slug from
    the title for convenience.
    """

    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "author")
    search_fields = ("title", "description", "ingredients", "steps")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for :class:`recipes.models.Comment`."""

    list_display = ("recipe", "user", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("body",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Admin configuration for :class:`recipes.models.Rating`."""

    list_display = ("recipe", "user", "stars", "created_at")
    list_filter = ("stars", "created_at")
    search_fields = ("recipe__title", "user__username")
