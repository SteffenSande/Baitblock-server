from django.contrib import admin
from django.db import models


class ReportCategoryAdmin(admin.ModelAdmin):
    list_display = ['category']

    list_filter = [
        'category',
    ]


class ReportCategory(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category

admin.site.register(ReportCategory, ReportCategoryAdmin)
