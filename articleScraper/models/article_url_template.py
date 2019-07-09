from django.contrib import admin
from django.db import models


class ArticleUrlTemplate(models.Model):
    """
        An parsing template object.

        Is used to find where in the url to extract what
    """
    ALPHA_NUMERIC = 'ALPHA_NUMERIC'
    NUMBERS_ONLY = 'NUMBERS_ONLY'
    LETTERS_ONLY = 'LETTERS_ONLY'
    OTHER = 'OTHER'
    URL_ID_TYPE = (
        (ALPHA_NUMERIC, 'AlphaNumeric'),
        (NUMBERS_ONLY, 'Numbers only'),
        (LETTERS_ONLY, 'Letters only'),
        (OTHER, 'Other'),
    )

    news_site = models.ForeignKey("scraper.NewsSite", on_delete=models.CASCADE,)

    name = models.CharField(max_length=255)
    id_position = models.IntegerField()
    id_separator = models.CharField(max_length=1, blank=True)
    id_length = models.IntegerField()
    id_type = models.CharField(choices=URL_ID_TYPE, max_length=255)
    placement = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        ordering = ['placement']


