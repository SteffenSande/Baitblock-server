from django.contrib import admin
from django.db import models
from django.db.models import SET_NULL

from helpers.base_models import BaseItem


class HeadlineAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    search_fields = ('revision', 'revision',)
    list_display = ['revision', 'revision', ]

    list_filter = [
        'news_site',
    ]


class HeadlineManager(models.Manager):
    def headlines_on_front_page(self, site_id):

        from scraper.models import NewsSite
        try:
            site = NewsSite.objects.get(id=site_id)
            return self.filter(news_site=site_id)[:site.current_headline_count_on_front_page]
        except NewsSite.DoesNotExist:
            return []


class Headline(BaseItem):
    """
        An news headline object.
    """
    summary = models.ForeignKey('submission.HeadlineSummary', null=True, blank=True, related_name='summary',
                                on_delete=SET_NULL)
    url_id = models.CharField(max_length=255, default="")

    url = models.URLField(unique=True, max_length=2500)

    objects = HeadlineManager()

    def __str__(self):
        return self.revision.__str__()

    def filename(self, file_type):
        return '{}.{}'.format(self.id, file_type)

    @property
    def revisions(self):
        from headlineScraper.models.revision import HeadlineRevision
        return HeadlineRevision.objects.filter(headline=self)

    @property
    def revision(self):
        from headlineScraper.models.revision import HeadlineRevision
        try:
            return HeadlineRevision.objects.filter(headline=self)[0]
        except IndexError:
            return None

    @property
    def diffs(self):

        from django.conf import settings
        from helpers.utilities import read_file_content_as_string

        diffs = []
        for revision in self.revisions:

            try:
                title_diff_path = revision.file_path(settings.HEADLINE_TITLE_DIFF_FOLDER)

                title_diff_content = read_file_content_as_string(title_diff_path)
            except FileNotFoundError:
                title_diff_content = ''  # TODO set to last value?

            try:
                sub_title_diff_path = revision.file_path(settings.HEADLINE_SUB_TITLE_DIFF_FOLDER)

                sub_title_diff_content = read_file_content_as_string(sub_title_diff_path)
            except FileNotFoundError:
                sub_title_diff_content = ''  # TODO set to last value?

            if title_diff_content or sub_title_diff_content:
                diffs.append({
                    'title': title_diff_content,
                    'sub_title': sub_title_diff_content
                })
        return diffs


admin.site.register(Headline, HeadlineAdmin)
