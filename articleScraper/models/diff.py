from django.db import models

from articleScraper.models import Revision


class Diff(models.Model):
    """ A model that represents the relationship between the content nodes """

    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)

    @property
    def changes(self):
        return self.change_set.all()

    class Meta:
        ordering = ('id',)

