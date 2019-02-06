from django import forms
from django.contrib import admin
from django.db import models

from helpers.base_models import BaseItem


class ArticleManager(models.Manager):
    def articles_on_front_page(self, site_id):
        from scraper.models import NewsSite
        try:
            site = NewsSite.objects.get(id=site_id)
            return self.filter(
                news_site=site_id)[:site.current_headline_count_on_front_page]
        except NewsSite.DoesNotExist:
            return []


class Article(BaseItem):
    ARTICLE = 'ARTICLE'
    FEED = 'FEED'
    EXTERNAL = 'EXTERNAL'
    VIDEO = 'VIDEO'
    HEADLINE_CATEGORIES = (
        (ARTICLE, 'Article'),
        (FEED, 'Feed'),
        (EXTERNAL, 'External'),
        (VIDEO, 'Video'),
    )

    headline = models.OneToOneField(
        'headlineScraper.Headline',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    category = models.CharField(
        default=ARTICLE, choices=HEADLINE_CATEGORIES, max_length=255)

    objects = ArticleManager()

    def __str__(self):
        return '{}'.format(self.headline.__str__())

    def update_or_create_defaults(self):
        return {'news_site': self.news_site, 'category': self.category}

    @property
    def revisions(self):
        from articleScraper.models import Revision
        return Revision.objects.filter(article__headline=self.headline)

    @property
    def revision(self):
        from articleScraper.models import Revision
        try:
            return Revision.objects.filter(article__headline=self.headline)[0]
        except IndexError:
            return None

    @property
    def diffs(self):

        from django.conf import settings
        from helpers.utilities import read_file_content_as_string

        diffs = []
        for revision in self.revisions:
            try:
                diff_path = revision.file_path(settings.ARTICLE_DIFF_FOLDER)
                diff_content = read_file_content_as_string(diff_path)
                diffs.append(diff_content)
            except FileNotFoundError:
                pass
        return diffs


class ArticleModelAdminForm(forms.ModelForm):
    revisions = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        super(ArticleModelAdminForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['revisions'].choices = [
                (None, f) for f in kwargs['instance'].revisions
            ]

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created',
        'modified',
    )
    search_fields = (
        'revision__title',
        'revision__sub_title',
    )
    list_display = ['revision', 'category']

    list_filter = ['news_site', 'category']

    form = ArticleModelAdminForm

    def revision(self, obj):
        return obj.revision

    revision.short_description = "Title"

    def get_queryset(self, request):
        """
        Displays only the articles on the headline.
        All articles is too much for the current server
        """
        from scraper.models import NewsSite

        article_query_objects = []

        for site in NewsSite.objects.active_news_sites():
            article_query_objects += [
                x.headline.id
                for x in Article.objects.articles_on_front_page(site.id)
            ]
        return Article.objects.filter(headline__id__in=article_query_objects)


admin.site.register(Article, ArticleAdmin)
