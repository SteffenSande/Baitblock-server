from django.contrib import admin
from django.db import models
from headlineScraper.models.headline import Headline

from helpers.base_models import RevisionBase


class HeadlineRevisionAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('title', 'sub_title',)
    list_display = ['title', 'sub_title', ]


class HeadlineRevision(RevisionBase):
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE)


admin.site.register(HeadlineRevision, HeadlineRevisionAdmin)
