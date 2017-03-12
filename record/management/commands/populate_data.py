# coding: utf-8
from uuid import uuid4
from django.utils import timezone

from django.core.management.base import BaseCommand

from record.models import Record, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ['Kate', 'Ilya', 'Denis', 'Dmitry', 'Grigory', 'Stas']
        records = []

        for username in users:
            u = User.objects.create_user(username,
                                         '{}@asd.asd'.format(username), username)

            for _ in range(10):
                r = Record(
                    inode=uuid4().hex,
                    url='http://google.com/' + uuid4().hex,
                    filename=uuid4().hex,
                    server_path='\\\\server\\path\\' + uuid4().hex,
                    size=0,
                    dotcms_updated=timezone.now(),
                    dotcms_author=username,
                    last_reuploaded=None,
                    reupload_author=u,
                    original_file=None
                )
                records.append(r)

        Record.objects.bulk_create(records)
