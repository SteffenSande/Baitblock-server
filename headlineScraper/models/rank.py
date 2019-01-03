from django.db import models
from django.contrib import admin


class RankAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    search_fields = ('title', 'placement',)
    list_display = ['headline', 'placement', 'of_total',]


class Rank(models.Model):
    headline = models.ForeignKey('headlineScraper.Headline', related_name='ranks', on_delete=models.CASCADE,)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    placement = models.IntegerField()
    of_total = models.IntegerField()

    def __str__(self):
        return '{0}/{1} {2}'.format(self.placement, self.of_total, self.headline.__str__())


admin.site.register(Rank, RankAdmin)
