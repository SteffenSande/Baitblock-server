from django.db import models


class RevisionBase(models.Model):
    timestamp = models.DateTimeField(null=True)
    version = models.IntegerField()

    class Meta:
        ordering = ['version']
        abstract = True


class BaseItem(models.Model):
    news_site = models.ForeignKey('scraper.NewsSite', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['modified']
        abstract = True

    @property
    def revisions(self):
        return []
