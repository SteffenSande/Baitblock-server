from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from articleScraper.models import ArticleUrlTemplate
from headlineScraper.models import Headline
from headlineScraper.serializers import HeadlineSerializer
from helpers.utilities import extract_hostname, find_headline_id
from scraper.models import NewsSite

@csrf_exempt
def search_for_links(request, *args, **kwargs):
    response = {}
    links = [y for y in request.POST.values()]

    for link in links:
        if link in response:
            continue

        # Extracts hostname from url
        base_url = extract_hostname(link)
        if not base_url:
            continue

        # Retrieves the site
        try:
            site = NewsSite.objects.get(base_url=base_url)
        except NewsSite.DoesNotExist:
            continue

        # Retrieve url templates for site
        templates = ArticleUrlTemplate.objects.filter(news_site=site)
        headline_id = find_headline_id(link, templates)
        if not headline_id:
            continue

        # Match headline with headline id and site
        try:
            headline = Headline.objects.get(url_id=headline_id, news_site=site)
            serializer = HeadlineSerializer(headline)
            response.update({link: serializer.data})
        except Headline.DoesNotExist:
            pass

    return JsonResponse(response)
