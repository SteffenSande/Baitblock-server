from django.urls import path
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
from api.views.api_root import api_root



urlpatterns = [
    path('', api_root, name='api_root'),
    path('test/<int:pk>/', test, name='test'),
    path('submission/category', CategoryList.as_view(), name='category'),
    path('submission/headline/report/', report_headline, name='report'),
    path('submission/headline/summary/', headline_summary, name='summary'),
    path('search/headlines/', search_for_links, name='headline_search'),
    path('limit/', LimitList.as_view(), name='limit'),
    path('image/', ArticleImageList.as_view(), name='images'),
    path('image/<int:pk>/', ArticleImageDetail.as_view(), name='image'),
    path(
        'photographer/', PhotographerList.as_view(), name='photographer_list'),
    path(
        'photographer/<int:pk>/',
        PhotographerDetail.as_view(),
        name='photographer'),
    path(
        'site/<int:pk>/journalist/<int:journalist_id>/',
        JournalistDetail.as_view(),
        name='journalist'),
    path(
        'site/<int:pk>/journalist/',
        JournalistList.as_view(),
        name='journalist_list'),
    path(
        'site/<int:pk>/article/<int:article_id>/',
        ArticleDetail.as_view(),
        name='article'),
    path('site/<int:pk>/article/', ArticleList.as_view(), name='article_list'),
    path(
        'site/<int:pk>/article/search/',
        ArticleSearch.as_view(),
        name='article_search'),
    path('site/<int:pk>/headline/', HeadlineList.as_view(), name='headlines'),
    path(
        'site/<int:pk>/headline/<int:headline_id>/',
        HeadlineDetail.as_view(),
        name='headline'),
    path('site/<int:pk>/', SiteDetail.as_view(), name='site'),
    path('site/', SiteList.as_view(), name='site_list')
]
