from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from celery import shared_task
from celery.task import periodic_task


@periodic_task(
    run_every=timedelta(minutes=20),
    name='Scrape')
def scrape_all_sites():
    """
        Scrapes all active sites for new headlines, then their articles
    """
    from scraper.models import NewsSite

    sites = NewsSite.objects.active_news_sites()
    for site in sites:
        scrape_a_site(site)
    return 'Started scraping sites {}'.format([site.name for site in sites])


@shared_task(name='Scrape a site')
def scrape_a_site(site):
    """
        Scrapes all active sites for new headlines, then their articles
    """
    from articleScraper.tasks import scrape_articles
    from headlineScraper.tasks import scrape_headlines

    scrape_headlines(site)
    scrape_articles(site)

    return 'Scraped success for site {}'.format(site.name)
