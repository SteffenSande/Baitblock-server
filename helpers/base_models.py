from django.db import models

from newsSite.models import NewsSite


class RevisionBase(models.Model):
    timestamp = models.DateTimeField(null=True, verbose_name='time of revision')
    version = models.IntegerField(verbose_name='version number')

    class Meta:
        ordering = ['version']
        abstract = True


class BaseItem(models.Model):
    news_site = models.ForeignKey(NewsSite, on_delete=models.CASCADE, verbose_name='news site name')
    modified = models.DateTimeField(null=True, verbose_name='time Of Edit')

    class Meta:
        ordering = ['modified']
        abstract = True

    @property
    def revisions(self):
        return []
