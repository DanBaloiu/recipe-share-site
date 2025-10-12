"""Database models for the recipe-sharing app."""


from django.db import models
from django.contrib.auth.models import User

# Create your models here.


STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"))


class Recipe(models.Model):
    """A user-authored recipe with ingredients, steps, and optional image."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    excerpt = models.TextField(max_length=300, blank=True)
    description = models.TextField()
    ingredients = models.TextField(help_text="One per line")
    steps = models.TextField(help_text="One step per line")
    tags = models.CharField(max_length=250, blank=True, help_text="Comma-separated tags")
    prep_minutes = models.PositiveIntegerField(default=0)
    cook_minutes = models.PositiveIntegerField(default=0)
    servings = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Newest first."""
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """Readable name in admin/shell."""
        return self.title

    def tag_list(self) -> list[str]:
        """Return tags as a clean list."""
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    @property
    def average_rating(self) -> float:
        """Average star rating rounded to 1 dp."""
        agg = self.ratings.aggregate(models.Avg("stars"))
        return round(agg["stars__avg"] or 0, 1)


class Comment(models.Model):
    """A user comment on a recipe."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Oldest → newest for conversation flow."""
        ordering = ["created_at"]

    def __str__(self) -> str:
        """Readable name in admin/shell."""
        return f"Comment by {self.user} on {self.recipe}"


class Rating(models.Model):
    """A 1–5 star rating that a user gives to a recipe (one per user)."""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Enforce one rating per (user, recipe)."""
        unique_together = ("recipe", "user")

    def __str__(self) -> str:
        """Readable name in admin/shell."""
        return f"{self.stars}★ by {self.user} on {self.recipe}"
    