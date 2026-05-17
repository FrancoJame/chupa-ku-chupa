import mimetypes

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404, HttpResponseRedirect


def serve_media(request, path):
    """Serve uploaded files in production (S3 presigned redirect or local file)."""
    if not default_storage.exists(path):
        raise Http404('File not found')

    if settings.USE_S3:
        return HttpResponseRedirect(default_storage.url(path))

    content_type, _ = mimetypes.guess_type(path)
    return FileResponse(
        default_storage.open(path),
        content_type=content_type or 'application/octet-stream',
    )
