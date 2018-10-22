import datetime
import os

from django.conf import settings
from django.http import JsonResponse

from articleScraper.scraper import ArticleScraper
from articleScraper.models import Article
from articleScraper.models import Revision
from headlineScraper.models import Headline

from wordcloud_generator.helper import generate, word_cloud_of_headlines


def word_cloud_of_article(request, pk):
    """
        Fetches a pregnerated a word cloud based on the words in a article
    """
    try:
        article = Article.objects.get(headline__id=pk)
        revision = article.revision_set.latest('timestamp')
    except (Article.DoesNotExist, Revision.DoesNotExist) as e:
        return JsonResponse({'error': 'Article or revision not found'}, status=404)

    link = os.path.join(settings.WORD_CLOUD_FOLDER, article.file_folder())
    wordcloud_link = os.path.join(link, revision.filename('png'))

    return JsonResponse({'link': wordcloud_link})


def generate_word_cloud_of_article(request, pk):
    """
        Generates a word cloud based on the words in a article
    """
    try:
        article = Article.objects.get(headline__id=pk)
        revision = article.revision_set.latest('timestamp')
    except (Article.DoesNotExist, Revision.DoesNotExist) as e:
        return JsonResponse({'error': 'Article or revision not found'}, status=404)

    # Construct the filename with full path
    path = os.path.join(settings.FILE_PATH_FIELD_DIRECTORY, article.file_folder())
    file = os.path.join(path, revision.filename('html'))
    scraper = ArticleScraper(article.headline)

    text = scraper.scrape_file(file)
    if not text:
        return JsonResponse({'error': 'No text in article'}, status=404)

    link = generate(text, article.file_folder(), revision.filename('png'))

    if link == 0:
        return JsonResponse({'error': 'Could not generate wordcloud'}, status=404)

    return JsonResponse({'word_cloud': link})


def generate_word_cloud_by_headlines(headlines):
    """
        Generates a word cloud based on headlines
    """
    if len(headlines) == 0:
        return JsonResponse({'error': 'No headlines on front page'}, status=404)

    file_folder = headlines[0].file_folder()
    link = word_cloud_of_headlines(headlines, file_folder, 'frontpage.png')
    if link == 0:
        return JsonResponse({'error': 'Could not generate wordcloud'}, status=404)

    return JsonResponse({'link': link})


def word_cloud_of_news_site_at_date(request, site, date):
    """
        Generates a word cloud based on all the headlines on a news site on a given date
    """
    try:
        parsed_date = datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        return JsonResponse({'error': 'Could not parse date'}, status=404)

    return generate_word_cloud_by_headlines(
        Headline.objects.filter(news_site=site, created__day=parsed_date.day, created__month=parsed_date.month,
                                created__year=parsed_date.year))


def word_cloud_of_news_site(request, pk):
    """
        Generates a word cloud based on all the headlines on a news site
    """

    headlines = Headline.objects.headlines_on_front_page(pk)

    return generate_word_cloud_by_headlines(headlines)
