"""Forms for the recipes app.

This module defines ModelForm classes used by the public-facing recipe
views.  Docstrings explain which model each form operates on.
"""

from django import forms
from .models import Comment, Recipe


class CommentForm(forms.ModelForm):
    """Form for creating or editing a `Comment`.

    Model: ``Comment``

    Fields:
    - ``body``: the comment text rendered as a textarea.
    """

    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write a helpful comment…",
                    "class": "form-control",
                }
            )
        }
        labels = {"body": ""}


class RecipeForm(forms.ModelForm):
    """Form for front-end recipe submission/editing.

    Model: ``Recipe``

    This form intentionally omits administrative fields such as ``status``
    and ``slug`` which are controlled server-side in the views.
    """

    class Meta:
        model = Recipe
        # Do not expose slug/status to front-end; server generates/controls them.
        fields = [
            "title",
            "image",
            "excerpt",
            "description",
            "ingredients",
            "steps",
            "tags",
            "prep_minutes",
            "cook_minutes",
            "servings",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "excerpt": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "ingredients": forms.Textarea(
                attrs={"rows": 6, "placeholder": "One ingredient per line", "class": "form-control"}
            ),
            "steps": forms.Textarea(
                attrs={"rows": 8, "placeholder": "One step per line", "class": "form-control"}
            ),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
            "prep_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "cook_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "servings": forms.NumberInput(attrs={"class": "form-control"}),
        }
