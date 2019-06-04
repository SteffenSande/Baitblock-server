from django.db import models
from django.contrib import admin

from articleScraper.models import Article


class Diff(models.Model):
    """ A model that represents the relationship between the content nodes """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    diff = models.TextField(default=None, null=True)

    def __str__(self):
        result = 'The diff is ' + str(self.diff) + ' is connected to article with id: ' + str(self.article)
        return result


admin.site.register(Diff)
