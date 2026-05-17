from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Upload files from the local media/ folder into the configured storage backend.'

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        if not media_root.exists():
            self.stderr.write(f'No media folder at {media_root}')
            return

        uploaded = 0
        for file_path in media_root.rglob('*'):
            if not file_path.is_file():
                continue

            storage_name = file_path.relative_to(media_root).as_posix()
            if default_storage.exists(storage_name):
                self.stdout.write(f'Skip (exists): {storage_name}')
                continue

            with file_path.open('rb') as handle:
                default_storage.save(storage_name, ContentFile(handle.read()))
            uploaded += 1
            self.stdout.write(f'Uploaded: {storage_name}')

        self.stdout.write(self.style.SUCCESS(f'Done. Uploaded {uploaded} file(s).'))
