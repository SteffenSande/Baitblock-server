from django.contrib import admin
from django.db import models


class UserReportAdmin(admin.ModelAdmin):
    search_fields = ('report',)
    list_display = ('report', 'ip')


class UserReport(models.Model):
    report = models.ForeignKey("submission.Report", on_delete=models.CASCADE,)

    ip = models.GenericIPAddressField()
    explanation = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip


admin.site.register(UserReport, UserReportAdmin)
