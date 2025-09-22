from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from books.models import Book


class Command(BaseCommand):
    help = 'Re-saves Book.image files so they are uploaded to the configured storage (e.g., Cloudinary).'

    def handle(self, *args, **options):
        processed_count = 0
        skipped_count = 0
        for book in Book.objects.all():
            image_field = book.image
            if not image_field:
                skipped_count += 1
                continue
            try:
                # Open existing file content from current storage (local or remote)
                with default_storage.open(image_field.name, 'rb') as f:
                    content = f.read()
                # Save back through the storage backend to trigger upload
                image_name = image_field.name.split('/')[-1]
                book.image.save(image_name, ContentFile(content), save=True)
                processed_count += 1
                self.stdout.write(self.style.SUCCESS(f'Synced image for book id={book.id}'))
            except Exception as exc:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'Skipped book id={book.id}: {exc}'))

        self.stdout.write(self.style.SUCCESS(f'Completed. Synced={processed_count}, Skipped={skipped_count}'))