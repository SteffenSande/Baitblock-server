from django.contrib import admin
from django.db import models


class Limit(models.Model):
    IGNORE = 'IGNORE'
    HIGH = 'HIGH'
    MID = 'MID'
    LOW = 'LOW'
    LIMITS = (
        (IGNORE, 'Ignore'),
        (HIGH, 'High'),
        (MID, 'Mid'),
        (LOW, 'Low'),
    )

    value = models.IntegerField(default=0)
    key = models.CharField(max_length=255, choices=LIMITS, default=IGNORE, unique=True)

    def __str__(self):
        return self.key


class LimitAdmin(admin.ModelAdmin):
    list_display = ['value', 'key']

admin.site.register(Limit, LimitAdmin)