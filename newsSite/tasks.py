from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from celery import shared_task
from celery.task import periodic_task
from articleScraper.tasks import scrape_site_for_a_article_of_type_article, scrape_articles
from headlineScraper.tasks import scrape_headlines, scrape_headlines_with_change
from newsSite.models import NewsSite


@periodic_task(
        run_every=timedelta(minutes=20),
        name='Scrape')
def scrape_all_sites():
    """
        Scrapes all active sites for new headlines, then their articles
    """

    sites = NewsSite.objects.active_news_sites()

    for site in sites:
        scrape_a_site(site)

    return 'Started scraping sites {}'.format([site.name for site in sites])


@shared_task(name='Scrape a site')
def scrape_a_site(site):
    """
        Scrapes all active sites for new headlines, then their articles
    """
    scrape_headlines(site)
    scrape_articles(site)

    return 'Scraped success for site {}'.format(site.name)


@shared_task(name='Scrape a site and introduce a change')
def scrape_a_site_with_change(site, change: str):
    """
        Scrapes all active sites for new headlines, then their articles

    Args:
        site (NewsSite): The page where we get the data
        change (str): The change we introduce
    Returns:
        None
    """
    headlines = scrape_headlines_with_change(site, change)
    scrape_site_for_articles_of_type_article(headlines)
    return None


@shared_task(name='create a test for dagbladet')
def test_dag_bladet():
    news_sites = NewsSite.objects.all()
    for news_site in news_sites:
        if 'verdens gang' in news_site.name.lower() or 'dagbladet' in news_site.name.lower():
            create_test_set(news_site, 'This is a change.')


def scrape_site_for_articles_of_type_article(headlines: [any]):

    for headline in headlines:
        scrape_site_for_a_article_of_type_article(headline)
    return None


@shared_task(name='Create test set for a news site')
def create_test_set(site, change: str):
    """ Run scrape_a_site on a site defined by passing a string parameter

    Args:
        site (NewsSite): This is the string representation of the news page, it needs only be a subset of the base URL of the page.
        change (str): The change to introduce to the article

    Returns:
        None
    """
    scrape_a_site(site)
    scrape_a_site_with_change(site, change)
    return None

@shared_task(name='Create test set for only headlines of dagbladet')
def create_test_set_for_headlines_only_dagbladet():
    news_sites = NewsSite.objects.all()
    for news_site in news_sites:
        if 'dagbladet' in news_site.name.lower():
            # Begin with this is change cause it makes the testing more intuitive
            scrape_headlines(news_site)


