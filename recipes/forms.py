from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Minimal comment form: one text area.
    """
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a helpful comment…"})
        }
        labels = {"body": ""}


from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Form for users to submit recipes from the front-end."""
    class Meta:
        model = Recipe
        # intentionally include slug so view can leave it blank and we'll auto-generate
        # remove 'slug' and 'status' from the front-end form; they are generated/controlled server-side
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
            "excerpt": forms.Textarea(attrs={"rows": 2}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "ingredients": forms.Textarea(attrs={"rows": 6, "placeholder": "One ingredient per line"}),
            "steps": forms.Textarea(attrs={"rows": 8, "placeholder": "One step per line"}),
        }
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    Minimal comment form: one text area.
    """
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a helpful comment…"})
        }
        labels = {"body": ""}
