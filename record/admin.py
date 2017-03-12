import os.path
import shutil
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone
from record.models import Record


class EmptyFile(Record):
    class Meta:
        proxy = True
        verbose_name = "Empty File"
        verbose_name_plural = "Empty Files"


class FixedFile(Record):
    class Meta:
        proxy = True
        verbose_name = "Fixed file"
        verbose_name_plural = "Fixed Files"


class Base(admin.ModelAdmin):
    list_display_links = None

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    def save_model(self, request, obj, form, change):
        if obj.size:
            raise ValidationError('Cannot override non-empty file')

        obj.size = form.cleaned_data['original_file'].size
        obj.reupload_author = request.user
        obj.last_reuploaded = timezone.now()

        super().save_model(request, obj, form, change)

        out = os.path.join('/tmp', os.path.basename(obj.original_file.name))
        if os.path.exists(out) and os.path.getsize(out):
            return

        shutil.move(obj.original_file.name, '/tmp')


class EmptyFilesAdmin(Base):
    list_display = ('filename', 'dotcms_updated', 'dotcms_author', 'original_file')
    list_editable = ('original_file', )
    ordering = ('-dotcms_updated', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(size=0)


class FixedAdmin(Base):
    list_display = ('filename', 'dotcms_updated', 'dotcms_author',
                    'last_reuploaded', 'reupload_author')
    ordering = ('-last_reuploaded',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(size__gt=0)


admin.site.register(EmptyFile, EmptyFilesAdmin)
admin.site.register(FixedFile, FixedAdmin)
