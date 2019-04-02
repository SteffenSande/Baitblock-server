from __future__ import absolute_import, unicode_literals

from celery import shared_task

from helpers.utilities import text_differ


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
    scraper = HeadlineScraper(site)
    headlines_with_rank = scraper.scrape()

    if not headlines_with_rank:
        return 'Failed to scrape site {}'.format(site.name)

    site.current_headline_count_on_front_page = len(headlines_with_rank)

    if site.current_headline_count_on_front_page > site.max_headlines_count:
        site.max_headlines_count = site.current_headline_count_on_front_page

    site.save()
    url_templates = ArticleUrlTemplate.objects.filter(news_site=site)

    added_ids = []
    # Creates or updates all headlines
    for revision, headline, rank, article_type in headlines_with_rank:

        # Check if revision title or subtitle is different than revision
        headline_id = find_headline_id(headline.url, url_templates)  # Finds id of headline

        try:
            new_url = format_url_for_site(headline.url, site.url())

            if headline_id:
                headline = Headline.objects.get(url_id=headline_id, news_site=site)
            else:
                headline = Headline.objects.get(url=new_url, news_site=site)

            headline.category = article_type
            headline.url = new_url
            headline.save()

            if headline.url_id not in added_ids and (headline.category is not Headline.EXTERNAL):
                # Revision is none only when we cannot locate the title of the headline
                added_ids.append(headline.url_id)
                headline_revisions = list(headline.revisions)
                headline_revisions.sort(key=lambda rev: rev.version, reverse=True)
                last_revision = headline_revisions[0]

                # There is headlines that represent the same case, this is mainly because of the paid version
                # Showing different content then the free version.
                # A way to remove this is a slow search trough earlier added headlines
                # could create a list over headline urls and check if it is added already

                if text_differ(last_revision.title, revision.title) \
                        or text_differ(last_revision.sub_title, revision.sub_title):
                    # Save new url
                    headline.save()
                    # Save new revision
                    revision.headline = headline
                    revision.version = len(headline.revisions) + 1
                    revision.save()

        except Headline.DoesNotExist:
            headline.url_id = headline_id
            try:
                headline.category = article_type
                headline.save()
            except IntegrityError:
                continue
            # Save new
            revision.headline = headline
            revision.version = 1
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
