from typing import Dict

from .models import Recipe, Comment


def pending_counts(request) -> Dict[str, int]:
    """Return pending counts for staff users.

    Adds `pending_recipes_count` and `pending_comments_count` to the template
    context. If the current user is not authenticated or not staff, both counts
    are 0 to avoid leaking information.
    """
    user = getattr(request, "user", None)
    if user and user.is_authenticated and user.is_staff:
        recipes = Recipe.objects.filter(status="draft").count()
        comments = Comment.objects.filter(approved=False).count()
        return {"pending_recipes_count": recipes, "pending_comments_count": comments}
    return {"pending_recipes_count": 0, "pending_comments_count": 0}
