from __future__ import absolute_import, unicode_literals

import datetime
import sys

from celery import shared_task

from differ.diff import Differ
from helpers.utilities import text_differ

from helpers.utilities import format_url_for_site, find_headline_id
from headlineScraper.scraper import HeadlineScraper
from headlineScraper.models import Headline
from headlineScraper.models.revision import HeadlineRevision
from headlineScraper.models.diff import Diff as Diff_Model
from headlineScraper.models.change import Change
from articleScraper.models import ArticleUrlTemplate
from django.db import IntegrityError


@shared_task(name='Scrape headlines')
def scrape_headlines(site):
    """Scrapes all headlines on the front page of a site

    Args:
        site (NewsSite): NewsSite to be scraped

    Returns:
        Scraping status
    """

    scraper = HeadlineScraper(site)
    headlines_with_rank = scraper.scrape()
    update_site_object(headlines_with_rank, site)
    url_templates = ArticleUrlTemplate.objects.filter(news_site=site)
    # This is what stores all the headlines and checks to see if there has been a change since last time
    store_headlines(headlines_with_rank, site, url_templates)

    if site and site.name:
        return 'Scraping headlines from site {} was a success!'.format(site.name)
    else:
        return 'Site was None... Could not scrape'


def update_site_object(headlines_with_rank, site):
    """Update headline count

    Args:
        headlines_with_rank ([Headline]): I need to look closer on what rank means
        site (NewsSite): NewsSite object from db and defined in scraper.models NewsSite

    Returns:
        None
    """
    site.current_headline_count_on_front_page = len(headlines_with_rank)
    if site.current_headline_count_on_front_page > site.max_headlines_count:
        site.max_headlines_count = site.current_headline_count_on_front_page
    site.save()


def store_headlines(headlines_with_rank, site, url_templates):
    """Store all headlines for site

    Args:
        headlines_with_rank ([Headline]): I need to look closer on what rank means
        site (NewsSite): NewsSite object from db and defined in scraper.models NewsSite
        url_templates: Where in the URL the id is

    Returns:
        None
    """
    # Creates or updates all headlines
    added_ids = []

    for revision, headline, rank, article_type in headlines_with_rank:

        # Check if revision title or subtitle is different than revision
        headline_id = find_headline_id(headline.url, url_templates)  # Finds id of headline

        try:
            headline = store_headline(headline_id, headline, revision, article_type, site, added_ids)
        except Headline.DoesNotExist:
            headline.url_id = headline_id
            try:
                headline = store_new_headline(revision, headline, article_type)
            except IntegrityError:
                continue
        except IntegrityError:
            continue
        except TypeError:
            print('There is a nonetype error at ', site)
            sys.exit(1)

        rank.headline = headline
        rank.save()


def store_headline(headline_id, headline, revision, article_type, site, added_ids):
    """Store a headline for site

    Args:
        headline (Headline): Headline object from db
        revision (Revision): Revision object form db
        article_type (string): The type of article it is
        site (NewsSite): NewsSite object from db
        headline_id (int): Unique id for the article and headline object.
        added_ids ([int]): id of the headlines added

    Returns:
        None
    """
    new_url = format_url_for_site(headline.url, site.url())

    if headline_id:
        headline = Headline.objects.get(url_id=headline_id, news_site=site)
    else:
        headline = Headline.objects.get(url=new_url, news_site=site)

    headline.category = article_type
    headline.url = new_url
    headline.save()

    if headline.url_id not in added_ids:
        # Revision is none only when we cannot locate the title of the headline
        added_ids.append(headline.url_id)
        headline_revisions = list(headline.revisions)
        headline_revisions.sort(key=lambda rev: rev.version, reverse=True)
        last_revision = headline_revisions[0]

        if text_differ(last_revision.title, revision.title) \
                or text_differ(last_revision.sub_title, revision.sub_title):

            headline.save()

            # Save new revision
            revision.headline = headline
            revision.version = len(headline.revisions) + 1
            revision.save()

            # Store new diff
            diff_model = Diff_Model()
            diff_model.headline = headline
            diff_model.save()

            # Store diff changes - title
            diff = Differ(last_revision.title, revision.title)
            changes = diff.create_diff_of_text()
            for index, (type_of_change, text) in enumerate(changes):
                change = Change(type_of_change=type_of_change, text=text)
                change.diff = diff_model
                change.pos = index
                change.title = True
                change.save()

            # Store diff changes - subtitle
            diff = Differ(last_revision.sub_title, revision.sub_title)
            changes = diff.create_diff_of_text()

            for index, (type_of_change, text) in enumerate(changes):
                change = Change(type_of_change=type_of_change, text=text)
                change.diff = diff_model
                change.pos = index
                change.title = False
                change.save()
    return headline


def store_new_headline(revision, headline, article_type):
    """Store a new headline

    Args:
        revision (Revision): Revision object
        headline (Headline): The new headline objects
        article_type (str): What article type is it, video, article, advertisement

    Raises:
        IntegrityError: Might not be able to save the headline or revision object
    """
    headline.category = article_type
    headline.save()
    revision.headline = headline
    revision.version = 1
    revision.save()

    # There needs to be a diff that only contains the first headline
    diff_model = Diff_Model()
    diff_model.headline = headline
    diff_model.save()

    # Store diff changes
    # Type 0 is normal text
    # Position is 0 cause we always star counting at 0

    change = Change(type_of_change=0, text=revision.title, title=True)
    change.diff = diff_model
    change.pos = 0
    change.title = True
    change.save()

    change = Change(type_of_change=0, text=revision.sub_title, title=False)
    change.diff = diff_model
    change.pos = 0
    change.title = False
    change.save()
    return headline


@shared_task(name='Create a change in all the headlines and store them')
def store_headlines_with_change(headlines_with_rank, site, url_templates, change):
    """Store all headlines for site

    Args:
        headlines_with_rank ([Headline]): I need to look closer on what rank means
        site (NewsSite): NewsSite object from db and defined in scraper.models NewsSite
        change (str): The change which we introduce in the headlines
        url_templates: Where in the url is the unique id of the article

    Returns:
        headlines
    """
    # Creates or updates all headlines
    headlines = []
    added_ids = []
    for revision, headline, rank, article_type in headlines_with_rank:
        # Check if revision title or subtitle is different than revision
        headline_id = find_headline_id(headline.url, url_templates)  # Finds id of headline
        try:
            revision = HeadlineRevision(title=change, sub_title=change, timestamp=datetime.datetime.now())
            headline = store_headline(headline_id, headline, revision, article_type, site, added_ids)
            headlines.append(headline)
        except Headline.DoesNotExist:
            headline.url_id = headline_id
            try:
                revision = HeadlineRevision(title=change, sub_title=change, timestamp=datetime.datetime.now())
                headline = store_new_headline(revision, headline, article_type)
                headlines.append(headline)
            except IntegrityError:
                continue
        except IntegrityError:
            continue
        rank.headline = headline
        rank.save()
    return headlines


@shared_task(name='Download all the headlines with a change in them')
def scrape_headlines_with_change(site, change: str):
    """Download the headlines and introduce a change in them and see if the system detects the change

    Args:
        site (NewsSite): NewsSite objects from the scraper.models NewsSite model
        change (str): The change we introduce in the article and headlines

    Returns:
        headlines

    """
    scraper = HeadlineScraper(site)
    headlines_with_rank = scraper.scrape()
    url_templates = ArticleUrlTemplate.objects.filter(news_site=site)
    return store_headlines_with_change(headlines_with_rank, site, url_templates, change)


@shared_task(name='Download a article that is of type article and create a test version that has a change in it')
def scrape_site_for_a_headline_of_type_article(site):
    scraper = HeadlineScraper(site)
    url_templates = ArticleUrlTemplate.objects.filter(news_site=site)
    headlines_with_rank = scraper.scrape()
    change = 'This is a change'
    added_ids = []
    for revision, headline, rank, article_type in headlines_with_rank:
        # Check if revision title or subtitle is different than revision
        headline_id = find_headline_id(headline.url, url_templates)  # Finds id of headline
        try:
            headline = store_headline(headline_id, headline, revision, article_type, site, added_ids)
            return headline

        except Headline.DoesNotExist:
            headline.url_id = headline_id

            try:
                headline = store_new_headline(revision, headline, article_type)
                revision = HeadlineRevision(title=change, sub_title=change, timestamp=datetime.datetime.now())
                headline = store_headline(headline_id, headline, revision, article_type, site, added_ids)
                return headline

            except IntegrityError:
                continue

        except IntegrityError:
            continue

        rank.headline = headline
        rank.save()
