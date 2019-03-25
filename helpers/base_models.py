from django.conf import settings
from django.db import models


class RevisionBase(models.Model):
    timestamp = models.DateTimeField(null=True)
    version = models.IntegerField()
    title = models.TextField()
    sub_title = models.TextField()

    class Meta:
        ordering = ['-timestamp']
        abstract = True

    def __str__(self):
        return self.title


class BaseItem(models.Model):
    news_site = models.ForeignKey('scraper.NewsSite', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified']
        abstract = True

    @property
    def revisions(self):
        return []
