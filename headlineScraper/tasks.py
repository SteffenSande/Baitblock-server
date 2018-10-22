from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings

from helpers.utilities import text_differ, save_file


@shared_task(name='Scrape headlines')
def scrape_headlines(site):
    """
        Scrapes all headlines on the front page of a site

        Args:
            site (NewsSite): NewsSite to be scraped

        Returns:
            Scraping status
    """

    from helpers.utilities import format_url_for_site, find_headline_id

    from headlineScraper.scraper import HeadlineScraper
    from headlineScraper.models import Headline
    from articleScraper.models import ArticleUrlTemplate

    from django.db import IntegrityError

    import uuid
    scraper = HeadlineScraper(site)
    headlines_with_rank = scraper.scrape()

    if not headlines_with_rank:
        return 'Failed to scrape site {}'.format(site.name)

    site.current_headline_count_on_front_page = len(headlines_with_rank)
    if site.current_headline_count_on_front_page > site.max_headlines_count:
        site.max_headlines_count = site.current_headline_count_on_front_page

    site.save()
    url_templates = ArticleUrlTemplate.objects.filter(news_site=site)

    # Creates or updates all headlines
    for revision, headline, rank in headlines_with_rank:
        headline_id = find_headline_id(headline.url, url_templates)
        try:
            new_url = format_url_for_site(headline.url, site.url())

            try:
                if headline_id:
                    headline = Headline.objects.get(url_id=headline_id, news_site=site)
                else:
                    headline = Headline.objects.get(url=new_url, news_site=site)
            except Headline.MultipleObjectsReturned:
                # Hack because old data...
                # If clean install remove this try except block and replace with
                # headline = Headline.objects.get(url_id=headline_id, news_site=site)
                # That should work....
                continue

            headline.url = new_url

            if revision is None:
                headline.save()

            elif headline.revision is None:
                # Save new url
                headline.save()

                # Save new revision
                revision.headline = headline
                revision.version = 1
                revision.file = uuid.uuid1()
                revision.save()
            elif text_differ(headline.revision.title, revision.title):
                # Save new url
                headline.save()

                # Save diff between last revision and current
                new_title = revision.title
                if new_title is None:
                    new_title = ''
                old_title = headline.revision.title
                if old_title is None:
                    old_title = ''
                save_diff(new_title, old_title, headline.revision.file_path(settings.HEADLINE_TITLE_DIFF_FOLDER))

                new_sub_title = revision.sub_title
                if new_sub_title is None:
                    new_sub_title = ''
                old_sub_title = headline.revision.sub_title
                if old_sub_title is None:
                    old_sub_title = ''

                save_diff(new_sub_title, old_sub_title, headline.revision.file_path(settings.HEADLINE_SUB_TITLE_DIFF_FOLDER))

                # Save new revision
                revision.headline = headline
                revision.version = len(headline.revisions) + 1
                revision.file = headline.revision.file
                revision.save()

        except Headline.DoesNotExist:
            headline.url_id = headline_id

            try:
                headline.save()
            except IntegrityError:
                continue

            # Save new
            revision.headline = headline
            revision.version = 1
            revision.file = uuid.uuid1()
            revision.save()
        except IntegrityError:
            continue

        # Always want to save a new rank.
        # TODO for optimization check last rank if it was the same.
        rank.headline = headline
        rank.save()

    if site and site.name:
        return 'Scraping headlines from site {} was a success!'.format(site.name)
    else:
        return 'Site was None... Could not scrape'


def save_diff(new_content, old_content, file_path):
    """
        Saves the diff between old and new content
        Args:
    """
    from differ.diff import Differ

    differ = Differ('', old_content=old_content, new_content=new_content)
    diff = differ.create_diff_of_text()

    if diff:
        save_file(file_path, diff)
