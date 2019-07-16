from django.contrib import admin
from django.db import models

from helpers.base_models import BaseItem


class HeadlineAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )

    list_filter = [
        'news_site',
    ]


class HeadlineManager(models.Manager):
    def headlines_on_front_page(self, site_id):
        """ Only get the headlines that are currently on the front page.
        :site_id: The number that represents the site that owns this headline
        :returns: All the current headlines that are on the
                  front page of this news site
                  na not really, it returns the news objects that are currently on the frontpage.
                  This is not good pratise and i will therefore change this.

        """
        from scraper.models import NewsSite
        try:
            site = NewsSite.objects.get(id=site_id)
            return self.filter(
                news_site=site_id)[:site.current_headline_count_on_front_page]
        except NewsSite.DoesNotExist:
            return []


class Headline(BaseItem):
    """
        An news headline object.
    """
    ARTICLE = 'ARTICLE'
    FEED = 'FEED'
    EXTERNAL = 'EXTERNAL'
    VIDEO = 'VIDEO'
    HEADLINE_CATEGORIES = (
        (ARTICLE, 'Article'),
        (FEED, 'Feed'),
        (EXTERNAL, 'External'),
        (VIDEO, 'Video'),
    )
    category = models.CharField(
        default=ARTICLE, choices=HEADLINE_CATEGORIES, max_length=255)

    url_id = models.CharField(max_length=255, default="")
    url = models.URLField(unique=True, max_length=2500)

    objects = HeadlineManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "The headline id: " + str(self.id) + " with revisions: " + str(list(self.revisions));

    def __repr__(self):
        representation = "news_site__id: " + str(self.news_site)
        print(representation)
        return representation

    @property
    def revisions(self):
        return self.headlinerevision_set.all()

    @property
    def diffs(self):
        return self.diff_set.all()

admin.site.register(Headline, HeadlineAdmin)
