from django.conf.urls import url

from wordcloud_generator.views import word_cloud_of_article, word_cloud_of_news_site, word_cloud_of_news_site_at_date
urlpatterns = [
    url(r'^wordcloud_generator/site/(?P<site>\d+)/date/(?P<date>\d{2}-\d{2}-\d{4})/$', word_cloud_of_news_site_at_date),
    url(r'^wordcloud_generator/article/(?P<pk>\d+)/$', word_cloud_of_article),
    url(r'^wordcloud_generator/site/(?P<pk>\d+)/$', word_cloud_of_news_site),
]

