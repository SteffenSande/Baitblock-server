from django.contrib import admin
from django.db import models


class HeadlineSummaryAdmin(admin.ModelAdmin):
    list_display = ('one_line', 'headline', 'ip')
    search_fields = ('headline', 'one_line',)


class HeadlineSummary(models.Model):
    headline = models.ForeignKey('headlineScraper.headline', on_delete=models.CASCADE,)

    one_line = models.TextField(max_length=2000)
    ip = models.GenericIPAddressField()

    created = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.one_line


admin.site.register(HeadlineSummary, HeadlineSummaryAdmin)
