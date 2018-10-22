from django.conf.urls import url

from api.views.article import ArticleDetail, ArticleList, ArticleSearch
from api.views.article_image import ArticleImageList, ArticleImageDetail
from api.views.catgory import CategoryList
from api.views.headline_summary import headline_summary
from api.views.headline import HeadlineDetail, HeadlineList
from api.views.journalist import JournalistDetail, JournalistList
from api.views.limit import LimitList
from api.views.photographer import PhotographerList, PhotographerDetail
from api.views.reporting import report_headline
from api.views.site import SiteDetail, SiteList
from api.views.search import search_for_links

from api.views.test import test

urlpatterns = [
    url(r'^test/(?P<pk>\d+)/$', test),
    url(r'^submission/category', CategoryList.as_view()),
    url(r'^submission/headline/report/$', report_headline),
    url(r'^submission/headline/summary/$', headline_summary),

    url(r'^search/headlines/$', search_for_links),

    url(r'^limit/$', LimitList.as_view()),

    url(r'^image/$', ArticleImageList.as_view()),
    url(r'^image/(?P<pk>\d+)/$', ArticleImageDetail.as_view()),

    url(r'^photographer/$', PhotographerList.as_view()),
    url(r'^photographer/(?P<pk>\d+)/$', PhotographerDetail.as_view()),

    url(r'^site/(?P<pk>\d+)/journalist/(?P<journalist_id>\d+)/$', JournalistDetail.as_view()),
    url(r'^site/(?P<pk>\d+)/journalist/$', JournalistList.as_view()),
    url(r'^site/(?P<pk>\d+)/article/(?P<article_id>\d+)/$', ArticleDetail.as_view()),
    url(r'^site/(?P<pk>\d+)/article/$', ArticleList.as_view()),
    url(r'^site/(?P<pk>\d+)/article/search/$', ArticleSearch.as_view()),
    url(r'^site/(?P<pk>\d+)/headline/$', HeadlineList.as_view()),
    url(r'^site/(?P<pk>\d+)/headline/(?P<headline_id>\d+)/$', HeadlineDetail.as_view()),
    url(r'^site/(?P<pk>\d+)/$', SiteDetail.as_view()),
    url(r'^site/$', SiteList.as_view()),
]

