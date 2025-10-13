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
