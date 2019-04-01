from __future__ import absolute_import, unicode_literals

from celery import shared_task

from articleScraper.models.child import Child
from scraper.models import NewsSite


@shared_task(name='Scrape articles')
def scrape_articles(site):
    """
        Scrape a news sites articles which has a corresponding headline on the front page

         Args:
             site (NewsSite): News site to be scraped
    """
    from articleScraper.models import Article
    from headlineScraper.models import Headline
    headlines = Headline.objects.headlines_on_front_page(site.id)

    if len(headlines) == 0:
        return "No Headlines on front page for {}".format(site.name)

    for headline in headlines:
        if site.base_url not in headline.url:
            not_an_article(headline, Article.EXTERNAL)
        elif any(not_url in headline.url for not_url in headline.news_site.urls_is_not_an_article):
            not_an_article(headline, Article.FEED)
        else:
            scrape_article(headline)
    return 'SUCCESS'


def not_an_article(headline, article_type):
    """
        Creates a empty article, which is either an external or a feed type

        Args:
            headline (Headline): The headline for the article
            article_type (str): The article type
    """
    from articleScraper.models import Article

    article = Article(headline=headline,
                      news_site=headline.news_site,
                      category=article_type)
    Article.objects.update_or_create(headline=headline, defaults=article.update_or_create_defaults())
    return 'SUCCESS created {}'.format(article_type)


@shared_task(name="Scrape one article")
def scrape_article(headline):
    """
        Scrapes one article based on a headline.

        Args:
            headline (Headline): The article headline
    """
    from articleScraper.models import Article
    from articleScraper.scraper import ArticleScraper

    # Scrapes the article
    scraper = ArticleScraper(headline)
    revision, article, journalists, images, content_list = scraper.scrape()

    # Article.published is none when encounter a subscription article
    # Or if the "article" is a on a weird feed
    if article is None:
        return "Article is None {}".format(headline.url)

    article, created = Article.objects.update_or_create(headline=article.headline,
                                                        defaults=article.update_or_create_defaults())
    last_revision = None
    # This is were the next implementation phase is.


    if article.revisions:
        print('This is the content found on page' + article.headline.url)
        print(list(article.revisions)[0].content)

    if last_revision is None:
        revision.article = article
        # add_article_journalists(revision, journalists)
        # add_article_images(revision, images)
        revision.version = 1
        revision.save()
        # create_diffs_of_articles_for_site(article, headline.news_site)
        content_list.sort(lambda key, value: key.pos)
        for content, children in content_list:
            content.revision = revision
            content.save()
            for child in children:
                Child(child=child, parent=content).save()

    else:
        print(last_revision)

    return 'SUCCESS scrape one article'


def add_article_journalists(revision, journalists):
    """
        Adds journalists to the article
        Args:
            revision (Revision): The article revision
            journalists (Journalist): Journalists for the article.
    """
    from articleScraper.models import Journalist
    for j in journalists:

        try:
            journalist, created = Journalist.objects.get_or_create(firstName=j.firstName, lastName=j.lastName,
                                                                   news_site=revision.article.news_site)
        except Journalist.MultipleObjectsReturned:
            journalist = Journalist.objects.filter(firstName=j.firstName,
                                                   lastName=j.lastName, news_site=revision.article.news_site)[0]
            created = False

        if created:
            revision.journalists.add(journalist)
        else:
            try:
                revision.journalists.get(id=journalist.id)
            except Journalist.DoesNotExist:
                revision.journalists.add(journalist)


def add_article_images(revision, images):
    """
        Adds journalists to the article
        Args:
            revision (Revision): The article revision
            images (ArticleImage): images for the article.
    """

    from articleScraper.models import ArticleImage
    from django.db import utils

    for img, photographers in images:

        image, created = ArticleImage.objects.get_or_create(url=img.url, defaults={'text': img.text})

        if created:
            try:
                revision.images.add(image)
            except utils.IntegrityError:
                pass
        else:
            try:
                revision.images.get(id=image.id)
            except ArticleImage.DoesNotExist:
                try:
                    revision.images.add(image)
                except utils.IntegrityError:
                    pass

        add_photographers_for_image(image, photographers)


def add_photographers_for_image(image, photographers):
    """
        Adds photographers to the article image
        Args:
            image (ArticleImage): The image taken bt the photographers
            photographers (Photographers): The photographers
    """
    from articleScraper.models import Photographer
    from django.db import utils

    # Creates or fetches all photographers
    photographers_for_image = []
    for p in photographers:
        photographer, photograph_created = Photographer.objects.get_or_create(firstName=p.firstName,
                                                                              lastName=p.lastName)
        photographers_for_image.append(photographer)

    # Adds the photographers to the images
    all_photographers = image.photographers.all()
    for photographer in photographers_for_image:
        if photographer not in all_photographers:
            try:
                image.photographers.add(photographer)
            except utils.IntegrityError:
                pass

    return photographers_for_image


@shared_task(name='Diff articles for site')
def create_diffs_of_articles_for_site(article, site: NewsSite):
    """
        Creates a diff for between an articles versions

         Args:
             article (Article): The article we want to create diff with
             site (NewsSite): Site the article belongs to
    """
    from django.conf import settings
    from helpers.utilities import read_file_content_as_string as file_content, save_file
    from differ.diff import Differ

    if not article:
        return 'Article was None'

    if len(article.revisions) <= 1:
        return 'Article {} had only {} revision(s)'.format(article.headline.id, len(article.revisions))

    try:
        new_file_content = file_content(article.revisions[0].file_path(settings.FILE_PATH_FIELD_DIRECTORY))
        old_file_content = file_content(article.revisions[1].file_path(settings.FILE_PATH_FIELD_DIRECTORY))
        if new_file_content is None or old_file_content is None:
            return 'An error has occurred. Cannot create diff for Article {}'.format(article.headline.id)
        selector = site.articleTemplate.selector

        differ = Differ(selector, old_file_content, new_file_content)
        diff = differ.create_diff_of_html()
        save_file(article.revisions[1].file_path(settings.ARTICLE_DIFF_FOLDER), diff)
    except FileNotFoundError:
        pass
    return 'DIFFS SUCCESS'
