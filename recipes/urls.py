"""URL routes for recipes app."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipe_list"),
    path("recipe/new/", views.recipe_create, name="recipe_create"),
    path("recipe/<slug:slug>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<slug:slug>/delete/", views.recipe_delete, name="recipe_delete"),
    path("recipe/<slug:slug>/", views.recipe_detail, name="recipe_detail"),
    path("comment/<int:pk>/edit/", views.comment_edit, name="comment_edit"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
    path("accounts/signup/", views.signup_view, name="signup"),
    # Staff approval routes
    path("staff/pending/recipes/", views.pending_recipes, name="pending_recipes"),
    path("staff/pending/comments/", views.pending_comments, name="pending_comments"),
    path("staff/recipe/<slug:slug>/approve/", views.approve_recipe, name="approve_recipe"),
    path("staff/recipe/<slug:slug>/reject/", views.reject_recipe, name="reject_recipe"),
    path("staff/comment/<int:pk>/approve/", views.approve_comment, name="approve_comment"),
    path("staff/comment/<int:pk>/reject/", views.reject_comment, name="reject_comment"),
]