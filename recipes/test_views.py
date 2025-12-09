"""View tests (GET and POST) adapted from the bootcamp walkthrough."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Recipe, Comment, Rating


User = get_user_model()


class TestRecipeViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)
        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Soup",
            slug="soup-1",
            description="Warm soup",
            ingredients="Water\nSalt",
            steps="Boil\nServe",
            status="published",
        )

    def test_recipe_detail_get_contains_form_and_content(self):
        resp = self.client.get(reverse("recipe_detail", kwargs={"slug": self.recipe.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.recipe.title.encode(), resp.content)
        self.assertIsNotNone(resp.context.get("comment_form"))

    def test_comment_post_requires_login(self):
        resp = self.client.post(reverse("recipe_detail", kwargs={"slug": self.recipe.slug}), {"body": "Nice!"})
        self.assertEqual(resp.status_code, 302)  # redirected to login

    def test_comment_post_creates_unapproved_comment(self):
        self.client.login(username="alice", password="pass")
        resp = self.client.post(reverse("recipe_detail", kwargs={"slug": self.recipe.slug}), {"body": "Nice!"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        c = Comment.objects.get(recipe=self.recipe, user=self.user)
        self.assertFalse(c.approved)

    def test_rating_post_creates_rating(self):
        self.client.login(username="alice", password="pass")
        resp = self.client.post(reverse("recipe_detail", kwargs={"slug": self.recipe.slug}), {"rating": "4"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Rating.objects.filter(recipe=self.recipe, user=self.user).exists())

    def test_invalid_empty_rating_does_not_create_and_no_500(self):
        self.client.login(username="alice", password="pass")
        resp = self.client.post(reverse("recipe_detail", kwargs={"slug": self.recipe.slug}), {"rating": ""}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Rating.objects.filter(recipe=self.recipe, user=self.user).exists())

    def test_pending_recipes_access_control(self):
        # non-staff gets redirected
        self.client.login(username="alice", password="pass")
        resp = self.client.get(reverse("pending_recipes"))
        self.assertEqual(resp.status_code, 302)
        # staff can access
        self.client.login(username="staff", password="pass")
        resp2 = self.client.get(reverse("pending_recipes"))
        self.assertEqual(resp2.status_code, 200)
