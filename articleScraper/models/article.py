from django import forms
from django.contrib import admin
from django.db import models

from helpers.base_models import BaseItem


class ArticleManager(models.Manager):
    def articles_on_front_page(self, site_id):
        from scraper.models import NewsSite
        try:
            print('heeeeeee')
            site = NewsSite.objects.get(id=site_id)
            return self.filter(
                news_site=site_id)[:site.current_headline_count_on_front_page]
        except NewsSite.DoesNotExist:
            return []


class Article(BaseItem):
    headline = models.OneToOneField(
        'headlineScraper.Headline',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    objects = ArticleManager()

    def __str__(self):
        return '{}'.format(self.headline.__str__())

    def update_or_create_defaults(self):
        return {'news_site': self.news_site}

    @property
    def revisions(self):
        return self.revision_set.all()

    @property
    def diffs(self):
        return self.diff_set.all()


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

    list_filter = ['news_site']

    form = ArticleModelAdminForm

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


