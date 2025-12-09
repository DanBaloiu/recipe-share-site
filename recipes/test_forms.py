"""Form tests adapted from the bootcamp walkthrough, applied to the recipes app."""

from django.test import TestCase

from .forms import CommentForm, RecipeForm


class TestCommentForm(TestCase):
    def test_form_is_valid(self):
        comment_form = CommentForm({"body": "This is a great recipe."})
        self.assertTrue(comment_form.is_valid(), msg="CommentForm is invalid")

    def test_form_is_invalid_when_body_missing(self):
        comment_form = CommentForm({"body": ""})
        self.assertFalse(comment_form.is_valid(), msg="CommentForm should be invalid when body is empty")


class TestRecipeForm(TestCase):
    def test_recipe_form_valid_minimum_fields(self):
        data = {
            "title": "Test Cake",
            "description": "Tasty",
            "ingredients": "Flour\nSugar",
            "steps": "Mix\nBake",
            # include numeric fields required by the ModelForm
            "prep_minutes": 10,
            "cook_minutes": 20,
            "servings": 4,
        }
        form = RecipeForm(data)
        self.assertTrue(form.is_valid(), msg="RecipeForm should be valid with required fields")

    def test_recipe_form_invalid_missing_title(self):
        data = {
            "title": "",
            "description": "Tasty",
            "ingredients": "Flour\nSugar",
            "steps": "Mix\nBake",
        }
        form = RecipeForm(data)
        self.assertFalse(form.is_valid(), msg="RecipeForm should be invalid when title missing")
