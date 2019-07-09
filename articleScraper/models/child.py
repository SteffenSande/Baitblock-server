from django.db import models

from articleScraper.models import Content


class Child(models.Model):
    """ A model that represents the relationship between the content nodes """
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    child = models.IntegerField(default=-1, null=False)

    class Meta:
        ordering = ('content',)

    def __str__(self):
        result = 'content ' + str(self.content.id) + 'has a child at id: ' + str(self.child)
        return result
