"""Admin registrations/config for recipe app models."""

from django.contrib import admin
from .models import Recipe, Comment, Rating

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin config for Recipe."""
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "author")
    search_fields = ("title", "description", "ingredients", "steps")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin config for Comment."""
    list_display = ("recipe", "user", "approved", "created_at")
    list_filter = ("approved", "created_at")
    search_fields = ("body",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Admin config for Rating."""
    list_display = ("recipe", "user", "stars", "created_at")
    list_filter = ("stars", "created_at")
    search_fields = ("recipe__title", "user__username")
