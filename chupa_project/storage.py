from storages.backends.s3 import S3Storage


class RailwayS3Storage(S3Storage):
    """S3 storage for Railway private buckets (presigned URLs for reads)."""

    default_acl = None
    file_overwrite = False
    querystring_auth = True
