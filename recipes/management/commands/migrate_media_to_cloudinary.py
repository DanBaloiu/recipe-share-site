from django.core.management.base import BaseCommand
from django.db import transaction
from recipes.models import Recipe


class Command(BaseCommand):
    help = "Migrate local media files (Recipe.image) to the configured storage (Cloudinary) by re-saving fields."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which files would be uploaded without performing uploads.",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force re-upload even if URL looks remote (starts with http).",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        force = options["force"]

        qs = Recipe.objects.exclude(image__isnull=True).exclude(image__exact="")
        total = qs.count()
        self.stdout.write(f"Found {total} recipes with an image field set.")
        if total == 0:
            return

        migrated = 0
        errors = 0

        for r in qs.iterator():
            img = r.image
            url = getattr(img, "url", None)
            name = getattr(img, "name", None)

            # Skip remote URLs unless --force
            if url and url.startswith("http") and not force:
                self.stdout.write(f"Skipping remote image for {r.slug}: {url}")
                continue

            self.stdout.write(f"Processing {r.slug}: field={name} url={url}")

            if dry_run:
                continue

            try:
                # Re-save the field to trigger the storage backend (uploads to Cloudinary)
                with transaction.atomic():
                    # read the file from storage and reassign (ensures backend.save is called)
                    f = r.image.open("rb")
                    content = f.read()
                    f.close()
                    r.image.save(name, content, save=True)
                migrated += 1
            except Exception as e:  # pragma: no cover - runtime errors
                errors += 1
                self.stderr.write(f"Error migrating {r.slug}: {e}")

        self.stdout.write(f"Done. Migrated={migrated} Errors={errors}")
