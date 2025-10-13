"""URL routes for recipes app."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("recipe/new/", views.recipe_create, name="recipe_create"),
    path("recipe/<slug:slug>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<slug:slug>/", views.recipe_detail, name="recipe_detail"),
    path("comment/<int:pk>/edit/", views.comment_edit, name="comment_edit"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
    path("accounts/signup/", views.signup_view, name="signup"),
]