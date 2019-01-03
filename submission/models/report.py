from django.contrib import admin
from django.db import models


class ReportAdmin(admin.ModelAdmin):
    list_display = ('headline', 'category', 'reports')
    search_fields = ('headline', 'category',)
    list_filter = ('category',)


class Report(models.Model):
    headline = models.ForeignKey('headlineScraper.Headline', on_delete=models.CASCADE,)
    category = models.ForeignKey("submission.ReportCategory", on_delete=models.CASCADE,)

    def __str__(self):
        return self.headline.__str__()

    @property
    def reports(self):
        from .user_report import UserReport
        return UserReport.objects.filter(report=self)

admin.site.register(Report, ReportAdmin)
