from django.contrib.postgres.fields import ArrayField
from django.contrib import admin
from django.db import models


class HeadlineTemplate(models.Model):
    """
        An parsing template object.

        Is used for the actual html scraping.
        Lists where to find what.
    """
    name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    exclude = ArrayField(models.CharField(max_length=255, blank=True), default=list, blank=True)
    list = ArrayField(models.CharField(max_length=255, blank=True), default=list, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    feed = models.CharField(default=None, null=True, max_length=255)
    video = models.CharField(default='/video/', max_length=255)

    def __str__(self):
        return "{}".format(self.name)


admin.site.register(HeadlineTemplate)
