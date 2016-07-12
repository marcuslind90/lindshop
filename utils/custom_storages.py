from django.conf import settings
from boto.s3.connection import S3Connection
from storages.backends.s3boto import S3BotoStorage
from django.core.files.storage import get_storage_class

# We need a custom Storage Class for our Media files because we
# want to have seperate locations for Static and Media files.
class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION

# S3 storage backend that saves the files locally, too.
class CachedS3BotoStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION
    
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        non_gzipped_file_content = content.file
        name = super(CachedS3BotoStorage, self).save(name, content)
        content.file = non_gzipped_file_content
        self.local_storage._save(name, content)
        return name