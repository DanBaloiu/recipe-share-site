"""List & detail views for recipes."""

from django.http import HttpResponse
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView
from .models import Recipe, Rating
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.urls import reverse
from django.views.generic.edit import CreateView
from .forms import RecipeForm

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

    # handle POST actions: rating or comment
    if request.method == "POST":
        # rating submitted
        if "rating" in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to rate.")
                return redirect("accounts:login")
            try:
                stars = int(request.POST.get("rating", 0))
            except (TypeError, ValueError):
                stars = 0
            if stars < 1 or stars > 5:
                messages.error(request, "Invalid rating value.")
                return redirect("recipe_detail", slug=recipe.slug)
            # create or update the user's rating for this recipe
            Rating.objects.update_or_create(
                recipe=recipe, user=request.user, defaults={"stars": stars}
            )
            # use a message tag to indicate this is a rating so the frontend shows a stars modal
            messages.success(request, str(stars), extra_tags="rating")
            return redirect("recipe_detail", slug=recipe.slug)

        # handle comment submission (new or edit)
        if "body" in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to comment.")
                return redirect("accounts:login")
            form = CommentForm(request.POST)
            if form.is_valid():
                edit_id = request.POST.get("edit_comment_id")
                if edit_id:
                    # editing an existing comment — must be owner
                    try:
                        existing = Comment.objects.get(pk=int(edit_id), recipe=recipe)
                    except (Comment.DoesNotExist, ValueError):
                        messages.error(request, "Comment not found.")
                        return redirect("recipe_detail", slug=recipe.slug)
                    if existing.user != request.user:
                        messages.error(request, "You don't have permission to edit that comment.")
                        return redirect("recipe_detail", slug=recipe.slug)
                    existing.body = form.cleaned_data["body"]
                    existing.approved = False  # require re-approval after edit
                    existing.save()
                    messages.success(request, "Comment updated and submitted for re-approval.")
                    return redirect("recipe_detail", slug=recipe.slug)
                else:
                    # create new comment
                    comment = form.save(commit=False)
                    comment.recipe = recipe
                    comment.user = request.user
                    comment.approved = False
                    comment.save()
                    messages.success(request, "Comment submitted for approval.")
                    return redirect("recipe_detail", slug=recipe.slug)
            else:
                messages.error(request, "Please fix the errors and try again.")
    else:
        # support server-side prefill when user clicks Edit (GET ?edit=<pk>)
        edit_id = request.GET.get("edit") if request.method == "GET" else None
        if edit_id and request.user.is_authenticated:
            try:
                existing = Comment.objects.get(pk=int(edit_id), recipe=recipe)
                if existing.user == request.user:
                    form = CommentForm(instance=existing)
                    # pass edit id to template via form.initial is not enough, set variable below
                    edit_comment_id = str(existing.pk)
                else:
                    form = CommentForm()
                    edit_comment_id = None
            except (Comment.DoesNotExist, ValueError):
                form = CommentForm()
                edit_comment_id = None
        else:
            form = CommentForm()
            edit_comment_id = None

    comments = recipe.comments.filter(approved=True).order_by("created_at")

    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "recipe": recipe,
            "user_rating": user_rating,
            "comments": comments,
            "comment_form": form,
            "edit_comment_id": locals().get('edit_comment_id', None),
        },
    )


def signup_view(request):
    """Simple signup view that creates a user and logs them in."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("recipe_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def recipe_create(request):
    """Allow logged-in users to submit a recipe for admin approval."""
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            # ensure author
            recipe.author = request.user
            # auto-generate a unique slug if not provided
            base = slugify(recipe.title)[:200]
            slug = base
            i = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            recipe.slug = slug
            # always save user submissions as draft for admin approval
            recipe.status = "draft"
            recipe.save()
            messages.success(request, "Recipe submitted — pending admin approval.")
            return redirect("recipe_detail", slug=recipe.slug)
        else:
            messages.error(request, "Please fix the errors and try again.")
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_create.html", {"form": form})


@login_required
def recipe_edit(request, slug):
    """Allow the recipe owner or staff to edit a recipe. Edits require re-approval."""
    recipe = get_object_or_404(Recipe, slug=slug)
    if not (request.user == recipe.author or request.user.is_staff):
        messages.error(request, "You don't have permission to edit that recipe.")
        return redirect("recipe_detail", slug=recipe.slug)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            updated = form.save(commit=False)
            # ensure slug remains the same (do not overwrite)
            updated.slug = recipe.slug
            # edits by non-staff require admin approval
            updated.status = "draft"
            updated.save()
            messages.success(request, "Recipe updated — submitted for re-approval.")
            return redirect("recipe_detail", slug=updated.slug)
        else:
            messages.error(request, "Please fix the errors and try again.")
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "recipes/recipe_edit.html", {"form": form, "recipe": recipe})


def recipe_delete(request, slug):
    """Allow the recipe owner or staff to delete a recipe from the front-end."""
    recipe = get_object_or_404(Recipe, slug=slug)
    if not (request.user == recipe.author or request.user.is_staff):
        messages.error(request, "You don't have permission to delete that recipe.")
        return redirect("recipe_detail", slug=recipe.slug)

    if request.method == "POST":
        recipe.delete()
        messages.success(request, "Recipe deleted.")
        return redirect("recipe_list")

    return render(request, "recipes/recipe_confirm_delete.html", {"recipe": recipe})


def comment_edit(request, pk):
    """Allow a user to edit their own comment; edited comments require re-approval."""
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        messages.error(request, "You don't have permission to edit that comment.")
        return redirect("recipe_detail", slug=comment.recipe.slug)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = False  # require admin re-approval
            comment.save()
            messages.success(request, "Comment updated and submitted for re-approval.")
            return redirect("recipe_detail", slug=comment.recipe.slug)
        else:
            messages.error(request, "Please fix the errors and try again.")
    else:
        form = CommentForm(instance=comment)

    return render(request, "recipes/comment_edit.html", {"form": form, "comment": comment})


def comment_delete(request, pk):
    """Allow a user to delete their own comment immediately."""
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.user:
        messages.error(request, "You don't have permission to delete that comment.")
        return redirect("recipe_detail", slug=comment.recipe.slug)

    if request.method == "POST":
        recipe_slug = comment.recipe.slug
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect("recipe_detail", slug=recipe_slug)

    return render(request, "recipes/comment_confirm_delete.html", {"comment": comment})


@login_required
def pending_recipes(request):
    """Staff view: list recipes awaiting approval (status='draft')."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view that page.")
        return redirect("recipe_list")
    recipes = Recipe.objects.filter(status="draft").order_by("-created_at")
    return render(request, "recipes/pending_recipes.html", {"recipes": recipes})


@login_required
def pending_comments(request):
    """Staff view: list comments awaiting approval (approved=False)."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to view that page.")
        return redirect("recipe_list")
    comments = Comment.objects.filter(approved=False).order_by("-created_at")
    return render(request, "recipes/pending_comments.html", {"comments": comments})


@login_required
def approve_recipe(request, slug):
    """Approve a draft recipe (POST only)."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform that action.")
        return redirect("recipe_list")
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == "POST":
        recipe.status = "published"
        recipe.save()
        messages.success(request, f"Recipe '{recipe.title}' approved and published.")
        return redirect("pending_recipes")
    return render(request, "recipes/pending_action_confirm.html", {"object": recipe, "type": "recipe", "action": "approve"})


@login_required
def reject_recipe(request, slug):
    """Reject (delete) a draft recipe. POST only."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform that action.")
        return redirect("recipe_list")
    recipe = get_object_or_404(Recipe, slug=slug)
    if request.method == "POST":
        recipe.delete()
        messages.success(request, f"Recipe '{recipe.title}' rejected and removed.")
        return redirect("pending_recipes")
    return render(request, "recipes/pending_action_confirm.html", {"object": recipe, "type": "recipe", "action": "reject"})


@login_required
def approve_comment(request, pk):
    """Approve a pending comment."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform that action.")
        return redirect("recipe_list")
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment.approved = True
        comment.save()
        messages.success(request, "Comment approved.")
        return redirect("pending_comments")
    return render(request, "recipes/pending_action_confirm.html", {"object": comment, "type": "comment", "action": "approve"})


@login_required
def reject_comment(request, pk):
    """Reject (delete) a pending comment."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to perform that action.")
        return redirect("recipe_list")
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment rejected and removed.")
        return redirect("pending_comments")
    return render(request, "recipes/pending_action_confirm.html", {"object": comment, "type": "comment", "action": "reject"})

