from django.conf import settings
from django.db import models


class RevisionBase(models.Model):
    timestamp = models.DateTimeField(null=True)
    file = models.FilePathField(path=settings.FILE_PATH_FIELD_DIRECTORY, blank=True)
    version = models.IntegerField()
    title = models.TextField()
    sub_title = models.TextField()

    class Meta:
        ordering = ['-timestamp']
        abstract = True

    def filename(self, file_type):
        return '{}__{}.{}'.format(self.file, self.version, file_type)

    def file_path(self, folder: str, file_type='html') -> str:
        return ""

    def __str__(self):
        return self.title


class BaseItem(models.Model):
    news_site = models.ForeignKey('scraper.NewsSite', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']
        abstract = True

    def file_folder(self):
        return self.news_site.file_folder()

    @property
    def revisions(self):
        return []

    @property
    def revision(self):
        return None

    @property
    def diffs(self):
        return None
