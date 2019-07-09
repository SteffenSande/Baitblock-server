from django.contrib.postgres.fields import ArrayField
from django.contrib import admin
from django.db import models


class ArticleTemplate(models.Model):
    """
        An parsing template object.

        Is used for the actual html scraping.
        Lists where to find what.
    """
    name = models.CharField(max_length=255)
    journalist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    selector = models.CharField(max_length=255, default='article')
    published = models.CharField(max_length=255)
    updated = models.CharField(max_length=255)
    datetime_attribute = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=255, default='Europe/Oslo')
    image_attribute = models.CharField(default='src', max_length=255)
    image_text = models.CharField(max_length=255)
    image_photographer = models.CharField(max_length=255, blank=True)
    image_element = models.CharField(max_length=255)
    photographer_delimiter = ArrayField(models.CharField(max_length=255, blank=True), default=list, blank=True)
    photograph_ignore_text = ArrayField(models.CharField(max_length=255, blank=True), default=list, blank=True)
    ignore_content_tag = models.CharField(max_length=255, blank=True)
    subscription = models.CharField(max_length=255, blank=True)
    video = models.CharField(max_length=255, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


