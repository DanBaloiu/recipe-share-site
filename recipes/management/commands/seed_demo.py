"""Management command to seed demo data: users, recipes, comments, and ratings.

Usage:
    python manage.py seed_demo

This is safe to run multiple times; it will create or update items idempotently.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from recipes.models import Recipe, Comment, Rating


class Command(BaseCommand):
    """Django management command entry point for seeding demo data."""

    help = "Seed demo users, recipes, comments, and ratings."

    def handle(self, *args, **options):
        """Create users, recipes, comments, and ratings, then print a summary."""
        with transaction.atomic():
            users = self._ensure_users()
            recipes = self._ensure_recipes(users["alice"])
            self._ensure_comments_and_ratings(recipes, users)

        self.stdout.write(self.style.SUCCESS("✅ Demo data seeded successfully.\n"))
        self._print_summary()

    # ---------- helpers ----------

    def _ensure_users(self) -> dict[str, User]:
        """Create two demo users (alice, bob) with known passwords if missing."""
        users = {}

        alice, _ = User.objects.get_or_create(
            username="alice", defaults={"email": "alice@example.com"}
        )
        if not alice.has_usable_password():
            alice.set_password("testpass123")
            alice.save()

        bob, _ = User.objects.get_or_create(
            username="bob", defaults={"email": "bob@example.com"}
        )
        if not bob.has_usable_password():
            bob.set_password("testpass123")
            bob.save()

        users["alice"] = alice
        users["bob"] = bob
        return users

    def _ensure_recipes(self, author: User) -> dict[str, Recipe]:
        """Create the 6 sample recipes if they do not already exist by slug."""
        data = [
            {
                "title": "Mediterranean Chickpea Salad",
                "slug": "mediterranean-chickpea-salad",
                "excerpt": "A refreshing, protein-packed salad with a zesty dressing.",
                "description": "Quick salad with chickpeas, tomatoes, cucumber, onion, feta and lemon-olive oil dressing.",
                "ingredients": "\n".join([
                    "1 can chickpeas, drained",
                    "1 cup cherry tomatoes, halved",
                    "1 cucumber, diced",
                    "1/4 red onion, thinly sliced",
                    "1/2 cup crumbled feta",
                    "2 tbsp olive oil",
                    "1 tbsp lemon juice",
                    "Salt and pepper to taste",
                ]),
                "steps": "\n".join([
                    "Whisk olive oil, lemon juice, salt, and pepper.",
                    "Add chickpeas, tomatoes, cucumber, and onion.",
                    "Toss and top with feta before serving.",
                ]),
                "tags": "vegetarian, salad, quick",
                "prep_minutes": 10,
                "cook_minutes": 0,
                "servings": 2,
                "status": "published",
            },
            {
                "title": "Classic Spaghetti Carbonara",
                "slug": "classic-spaghetti-carbonara",
                "excerpt": "Italian favorite with eggs, Parmesan, and pancetta.",
                "description": "Creamy yet light; authentic carbonara made silky with eggs and cheese.",
                "ingredients": "\n".join([
                    "200g spaghetti",
                    "100g pancetta or bacon",
                    "2 eggs",
                    "1/2 cup grated Parmesan",
                    "2 cloves garlic",
                    "Salt and pepper",
                ]),
                "steps": "\n".join([
                    "Cook spaghetti in salted water.",
                    "Fry pancetta with garlic until crisp.",
                    "Whisk eggs and Parmesan.",
                    "Toss hot pasta with pancetta, remove from heat, and stir in egg mixture.",
                    "Season with black pepper and serve immediately.",
                ]),
                "tags": "italian, pasta, quick",
                "prep_minutes": 5,
                "cook_minutes": 15,
                "servings": 2,
                "status": "published",
            },
            {
                "title": "Chicken Curry with Coconut Milk",
                "slug": "chicken-curry-coconut",
                "excerpt": "Creamy and flavorful curry made easy with coconut milk.",
                "description": "Mild aromatic curry with tender chicken and rich coconut base—great with rice.",
                "ingredients": "\n".join([
                    "2 chicken breasts, cubed",
                    "1 onion, diced",
                    "2 cloves garlic, minced",
                    "1 tbsp curry powder",
                    "1 tsp turmeric",
                    "1 can coconut milk",
                    "1 tbsp olive oil",
                    "Salt and pepper",
                ]),
                "steps": "\n".join([
                    "Sauté onion and garlic in olive oil.",
                    "Add chicken and brown.",
                    "Stir in curry powder and turmeric.",
                    "Pour coconut milk and simmer 15 minutes.",
                ]),
                "tags": "curry, chicken, dinner",
                "prep_minutes": 10,
                "cook_minutes": 25,
                "servings": 3,
                "status": "published",
            },
            {
                "title": "Fluffy Banana Pancakes",
                "slug": "fluffy-banana-pancakes",
                "excerpt": "Soft and naturally sweet pancakes.",
                "description": "Light and fluffy with crisp edges — no refined sugar.",
                "ingredients": "\n".join([
                    "1 banana",
                    "1 cup flour",
                    "1 tbsp sugar",
                    "1 tsp baking powder",
                    "1 egg",
                    "3/4 cup milk",
                    "Butter for frying",
                ]),
                "steps": "\n".join([
                    "Mash banana, whisk in egg, milk, and sugar.",
                    "Fold in flour and baking powder.",
                    "Cook on a buttered pan until golden.",
                ]),
                "tags": "breakfast, sweet, easy",
                "prep_minutes": 5,
                "cook_minutes": 10,
                "servings": 2,
                "status": "published",
            },
            {
                "title": "Garlic Butter Steak Bites",
                "slug": "garlic-butter-steak-bites",
                "excerpt": "Juicy seared steak cubes in garlic butter.",
                "description": "Quick steak pieces glazed in rich garlic butter; crowd-pleaser.",
                "ingredients": "\n".join([
                    "500g sirloin steak, cubed",
                    "3 tbsp butter",
                    "3 cloves garlic, minced",
                    "Salt and pepper",
                    "1 tbsp parsley, chopped",
                ]),
                "steps": "\n".join([
                    "Season steak with salt and pepper.",
                    "Sear 2–3 minutes per side.",
                    "Add butter and garlic; toss briefly.",
                    "Garnish with parsley.",
                ]),
                "tags": "beef, keto, quick",
                "prep_minutes": 5,
                "cook_minutes": 10,
                "servings": 2,
                "status": "published",
            },
            {
                "title": "Chocolate Mug Cake",
                "slug": "chocolate-mug-cake",
                "excerpt": "A rich, single-serve cake in 90 seconds.",
                "description": "Perfect for a late-night chocolate fix — no oven required.",
                "ingredients": "\n".join([
                    "4 tbsp flour",
                    "2 tbsp cocoa powder",
                    "2 tbsp sugar",
                    "1/4 tsp baking powder",
                    "3 tbsp milk",
                    "1 tbsp vegetable oil",
                ]),
                "steps": "\n".join([
                    "Combine all ingredients in a mug; stir until smooth.",
                    "Microwave 90 seconds; enjoy warm.",
                ]),
                "tags": "dessert, chocolate, microwave",
                "prep_minutes": 2,
                "cook_minutes": 2,
                "servings": 1,
                "status": "published",
            },
        ]

        created = {}
        for item in data:
            recipe, _ = Recipe.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "author": author,
                    "title": item["title"],
                    "excerpt": item["excerpt"],
                    "description": item["description"],
                    "ingredients": item["ingredients"],
                    "steps": item["steps"],
                    "tags": item["tags"],
                    "prep_minutes": item["prep_minutes"],
                    "cook_minutes": item["cook_minutes"],
                    "servings": item["servings"],
                    "status": item["status"],
                },
            )
            created[item["slug"]] = recipe
        return created

    def _ensure_comments_and_ratings(self, recipes: dict[str, Recipe], users: dict[str, User]) -> None:
        """Create 1–2 comments and 2 ratings per recipe (alice & bob)."""
        for slug, recipe in recipes.items():
            # Comments
            Comment.objects.get_or_create(
                recipe=recipe, user=users["alice"],
                body=f"Loved the {recipe.title.lower()} — turned out great!"
            )
            Comment.objects.get_or_create(
                recipe=recipe, user=users["bob"],
                body=f"Nice flavors. I added a tweak and it worked well."
            )

            # Ratings (update_or_create to keep it idempotent)
            Rating.objects.update_or_create(
                recipe=recipe, user=users["alice"], defaults={"stars": 5 if "chocolate" in slug else 4}
            )
            Rating.objects.update_or_create(
                recipe=recipe, user=users["bob"], defaults={"stars": 4 if "salad" in slug else 3}
            )

    def _print_summary(self) -> None:
        """Print a compact summary of counts for quick verification."""
        total_recipes = Recipe.objects.count()
        total_comments = Comment.objects.count()
        total_ratings = Rating.objects.count()

        lines = [
            f"Recipes:  {total_recipes}",
            f"Comments: {total_comments}",
            f"Ratings:  {total_ratings}",
            "",
            "A few sample averages:",
        ]
        for r in Recipe.objects.order_by("-created_at")[:3]:
            lines.append(f"- {r.title}: avg {r.average_rating}★, comments={r.comments.count()}")
        self.stdout.write("\n".join(lines))
