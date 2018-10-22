from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task(name='Generate wordclouds')
def generate_word_clouds(site):
    """
        Generates word clouds for a new site

        Args:
             site (NewsSite): The news site ti generate word clouds from

        Returns (str):
            A status message
    """
    from headlineScraper.models import Headline
    from articleScraper.models import Article

    all_headlines = Headline.objects.headlines_on_front_page(site.id)

    if not all_headlines:
        if site and site.name:
            return 'Could not create front page word cloud for {} because there exists no headlines'.format(site.name)
        return 'Could not create front page word cloud because there exists no headlines and site or site.name was None'

    # TODO this step is only for this thesis because of limited server space....
    empty_all_word_clouds_for_site(all_headlines[0].file_folder())
    headlines = []
    max_headlines = 5
    for headline in reversed(all_headlines):
        try:
            article = Article.objects.get(pk=headline.id)

            if article.revision and article.category == Article.ARTICLE and not article.revision.subscription:
                headlines.append(headline)

                if len(headlines) == max_headlines:
                    break
        except Article.DoesNotExist:
            pass

    generate_front_page_word_cloud(headlines)

    # Generate a word cloud for each headline on the front page
    for headline in headlines:
        generate_a_word_cloud(headline)


def empty_all_word_clouds_for_site(folder):
    """
        Empties the sites word cloud directory for word clouds.
        This is only done because the server for this thesis does not have enough room for a word cloud per headline.
        So we compromise and only generates a word cloud per headline on the front page.

        Args:
             folder (str): Name of the sites word cloud folder in the media word cloud folder.

        Returns (str):
            A status message
    """
    import os
    from django.conf import settings

    word_cloud_folder = os.path.join(settings.WORD_CLOUD_FOLDER, folder)
    if os.path.isdir(word_cloud_folder):
        for f in os.listdir(word_cloud_folder):
            os.remove(os.path.join(word_cloud_folder, f))


@shared_task(name='Generate a wordcloud for frontpage')
def generate_front_page_word_cloud(headlines):
    """
        Generates word clouds for a list of headlines

        Args:
             headlines (List<Headline>): The headlines which get generate a word cloud each of its text content

        Returns (str):
            A status message
    """
    from wordcloud_generator.helper import word_cloud_of_headlines

    try:
        file_folder = headlines[0].file_folder()
    except IndexError:
        return 'Culd not gerenate front page wordclouds'
    link = word_cloud_of_headlines(headlines, file_folder, 'frontpage.png')
    return 'Frontpage wordcloud generation success. {}'.format(link)


@shared_task(name='Generate a word cloud')
def generate_a_word_cloud(headline):
    """
        Generates a word cloud for a  headline

        Args:
             headline (Headline): The headline which to generate a word cloud from its text content

        Returns (str):
            A status message
    """
    from django.conf import settings
    from articleScraper.models import Revision
    from articleScraper.scraper import ArticleScraper
    from articleScraper.models import Article
    from wordcloud_generator.helper import generate

    try:
        article = headline.article
    except Article.DoesNotExist:
        return 'Headline {} has no article is then not a article per definition'.format(headline)

    try:
        revision = article.revision
    except Revision.DoesNotExist:
        return 'Headline {} had no revision and is properly not an article'.format(headline)

    scraper = ArticleScraper(headline)

    text = scraper.scrape_file(revision.file_path(settings.FILE_PATH_FIELD_DIRECTORY))
    if not text:
        return 'Article for headline {} was empty'.format(headline)

    link = generate(text, headline.file_folder(), revision.filename('png'))
    return 'Word cloud for headline {} was generated {}'.format(headline, link)