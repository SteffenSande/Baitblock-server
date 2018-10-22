import os
from django.contrib import admin
from django.db import models

from helpers.base_models import RevisionBase


class HeadlineRevisionAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('title', 'sub_title',)
    list_display = ['title', 'sub_title', ]


class HeadlineRevision(RevisionBase):
    headline = models.ForeignKey('headlineScraper.headline')

    def file_path(self, folder: str, file_type='html') -> str:
        return os.path.join(folder, os.path.join(self.headline.news_site.file_folder(), self.filename(file_type)))



admin.site.register(HeadlineRevision, HeadlineRevisionAdmin)
