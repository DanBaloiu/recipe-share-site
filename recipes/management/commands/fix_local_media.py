from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Recipe
from pathlib import Path


def find_best_match(media_root: Path, slug: str):
    """Find a filename in media_root/recipes that best matches the recipe slug.
    Returns the relative path under media_root (e.g. 'recipes/xxx.webp') or None."""
    candidates = []
    recipes_dir = media_root / "recipes"
    if not recipes_dir.exists():
        return None
    for p in recipes_dir.iterdir():
        if not p.is_file():
            continue
        name = p.name.lower()
        if slug.lower() in name:
            candidates.append(p)
    if not candidates:
        return None
    # prefer exact or startswith matches
    candidates.sort(key=lambda p: (0 if p.name.lower().startswith(slug.lower()) else 1, -len(p.name)))
    return Path("recipes") / candidates[0].name


class Command(BaseCommand):
    help = (
        "Fix ImageField paths for local development. "
        "Strips leading 'media/' and attempts to point fields to existing files under media/recipes."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true", help="Do not modify DB; just show proposed changes"
        )

    def handle(self, *args, **options):
        dry = options.get("dry_run")
        media_root = Path(settings.MEDIA_ROOT)
        updated = 0
        missing = 0
        self.stdout.write(f"MEDIA_ROOT = {media_root}")
        for r in Recipe.objects.all():
            raw = (r.image.name or "").strip()
            if not raw:
                continue
            proposed = raw
            # strip leading 'media/' if present
            if proposed.startswith("media/"):
                proposed = proposed[len("media/"):]
                if proposed.startswith("/"):
                    proposed = proposed[1:]

            file_path = media_root / proposed
            if file_path.exists():
                if proposed != raw:
                    self.stdout.write(f"Will update {r.slug}: '{raw}' -> '{proposed}'")
                    if not dry:
                        r.image.name = proposed
                        r.save(update_fields=["image"])
                        updated += 1
                continue

            # not found at proposed path, try to find a best match by slug
            match = find_best_match(media_root, r.slug)
            if match:
                self.stdout.write(f"Found match for {r.slug}: '{raw}' -> '{match.as_posix()}'")
                if not dry:
                    r.image.name = match.as_posix()
                    r.save(update_fields=["image"])
                    updated += 1
            else:
                self.stdout.write(f"Missing file for {r.slug}: stored='{raw}'")
                missing += 1

        self.stdout.write(f"Done: updated={updated}, missing={missing}")