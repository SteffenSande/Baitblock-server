from django.db import models

from headlineScraper.models.headline import Headline


class Diff(models.Model):
    """ A model that represents the relationship between the content nodes """

    headline = models.ForeignKey(Headline, on_delete=models.CASCADE)

    @property
    def title_changes(self):
        changes = self.change_set.all()
        titles = []
        for change in changes:
            if change.title:
                titles.append(change)
        return titles

    @property
    def sub_title_changes(self):
        changes = self.change_set.all()
        sub_titles = []
        for change in changes:
            if not change.title:
                sub_titles.append(change)
        return sub_titles

    class Meta:
        ordering = ('id',)

