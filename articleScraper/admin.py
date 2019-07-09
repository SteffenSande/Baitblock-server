from django.contrib import admin

from articleScraper.models import Article, ArticleUrlTemplate, Content, Photographer, Revision, ArticleTemplate, \
    ArticleImage
from articleScraper.models.article import ArticleAdmin
from articleScraper.models.article_image import ArticleImageAdmin
from articleScraper.models.child import Child
from articleScraper.models.diff import Diff
from articleScraper.models.journalist import JournalistAdmin, Journalist
from articleScraper.models.photographer import PhotographerAdmin
from articleScraper.models.revision import RevisionAdmin

admin.site.register(Article, ArticleAdmin)
admin.site.register(Diff)
admin.site.register(Child)
admin.site.register(ArticleUrlTemplate)
admin.site.register(Content)
admin.site.register(Photographer, PhotographerAdmin)
admin.site.register(Journalist, JournalistAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(ArticleTemplate)
admin.site.register(ArticleImage, ArticleImageAdmin)
