from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models


class NewsSiteManager(models.Manager):
    def active_news_sites(self):
        return self.filter(is_active=True)


class NewsSite(models.Model):
    """
        An news site object.
    """
    headlineTemplate = models.ForeignKey('headlineScraper.HeadlineTemplate', on_delete=models.CASCADE, )
    articleTemplate = models.ForeignKey('articleScraper.ArticleTemplate', on_delete=models.CASCADE, )

    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=255)
    base_url = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    current_headline_count_on_front_page = models.IntegerField(default=0)
    max_headlines_count = models.IntegerField(default=0)
    urls_is_not_an_article = ArrayField(models.CharField(max_length=255, blank=True), default=list, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = NewsSiteManager()

    def __str__(self):
        return '{}'.format(self.name)

    def file_folder(self):
        return str(self.name).replace(' ', '')

    def url(self):
        return '{}{}'.format('https://www.', self.base_url)


@admin.register(NewsSite)
class NewsSiteAdmin(admin.ModelAdmin):
    readonly_fields = ('current_headline_count_on_front_page', 'max_headlines_count', 'created', 'modified',)

    list_display = ['name', 'is_active']
