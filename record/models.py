import os.path
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


def upload_to(instance, filename):
    return os.path.join(settings.MEDIA_PATH,
                        instance.reupload_author.username, filename)


class Record(models.Model):
    inode = models.TextField(unique=True)
    url = models.TextField(unique=True)
    filename = models.TextField()
    server_path = models.TextField(unique=True)
    size = models.IntegerField()
    dotcms_updated = models.DateTimeField()
    dotcms_author = models.TextField()
    last_reuploaded = models.DateTimeField(null=True, default=None,
                                           verbose_name='Manually fixed')
    reupload_author = models.ForeignKey(User, editable=False)
    original_file = models.FileField(null=True, blank=True,
                                     upload_to=upload_to)

    def __str__(self):
        return self.filename
