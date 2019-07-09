from django.db import models

from articleScraper.models import Article


class Diff(models.Model):
    """ A model that represents the relationship between the content nodes """
    diff = models.TextField(default=None, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ('article',)

    def __str__(self):
        result = 'The diff is ' + str(self.diff) + ' is connected to article with id: ' + str(self.article)
        return result
