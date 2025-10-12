"""List & detail views for recipes."""

from django.http import HttpResponse
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Recipe, Rating

# Create your views here.


class RecipeListView(ListView):
    """Paginated list of published recipes with optional search/tag filter."""
    model = Recipe
    template_name = "recipes/recipe_list.html"
    context_object_name = "recipes"
    paginate_by = 9

    def get_queryset(self):
        """Return queryset filtered by ?q= and ?tag=."""
        qs = Recipe.objects.filter(status="published")
        q = self.request.GET.get("q")
        tag = self.request.GET.get("tag")
        if q:
            qs = qs.filter(
                models.Q(title__icontains=q)
                | models.Q(description__icontains=q)
                | models.Q(ingredients__icontains=q)
                | models.Q(steps__icontains=q)
            )
        if tag:
            qs = qs.filter(tags__icontains=tag)
        return qs


def recipe_detail(request, slug):
    """Render the detail page for a single recipe with comments and ratings."""
    recipe = get_object_or_404(Recipe, slug=slug)
    if recipe.status != "published" and (
        not request.user.is_staff and recipe.author != request.user
    ):
        return redirect("recipe_list")

    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(recipe=recipe, user=request.user).first()

    comments = recipe.comments.filter(approved=True).order_by("created_at")

    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "recipe": recipe,
            "user_rating": user_rating,
            "comments": comments,
        },
    )

