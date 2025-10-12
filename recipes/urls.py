"""URL routes for recipes app."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("recipe/<slug:slug>/", views.recipe_detail, name="recipe_detail"),
]