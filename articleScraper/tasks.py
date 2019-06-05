from __future__ import absolute_import, unicode_literals

from celery import shared_task

from articleScraper.models.child import Child
from articleScraper.models.article import Article
from articleScraper.models.diff import Diff
from articleScraper.scraper import ArticleScraper
from differ.diff import Differ
from headlineScraper.models import Headline


@shared_task(name='Scrape articles')
def scrape_articles(site):
    """Download and store the information on the site provided as a parameter
    This is executed after headlines are downloaded and stored.
    This function is called from the scraper task that is being executed every 20 minutes and will scrape all a tags of headlines on the front page

    Args:
        site (NewsSite): The site that we want to grab to headlines from

    Returns:
        None
    """

    # Grab the headlines already scraped from the front pages
    headlines = Headline.objects.headlines_on_front_page(site.id)

    if len(headlines) == 0:
        # This shouldn't happen
        # Because there should be at least one article on the front page!
        # In other words, maybe throw error here
        return "No Headlines on front page for {}".format(site.name)

    for headline in headlines:
        if site.base_url not in headline.url:
            not_an_article(headline)
        elif any(not_url in headline.url for not_url in headline.news_site.urls_is_not_an_article):
            not_an_article(headline)
        else:
            scrape_article(headline)

    return 'SUCCESS'


def not_an_article(headline):
    """This is for all unsupported articles on the front page.

    Args:
        headline (Headline): reference to the headline object that correspond to this article

    Returns:
        None
    """

    article = Article(headline=headline,
                      news_site=headline.news_site)
    Article.objects.update_or_create(headline=headline, defaults=article.update_or_create_defaults())
    return 'SUCCESS created an article object even though it should\'t be supported'


@shared_task(name="Scrape one article")
def scrape_article(headline: Headline):
    """This tasks will be called from scrape_articles and will download and store an article that is found in a headlines a tag.

    Args:
        headline (Headline): reference to the headline object that we are scraping from.

    Returns
        None
    """
    if headline.category == Headline.ARTICLE:
        scraper = ArticleScraper(headline)
        revision, article, journalists, images, content_list = scraper.scrape()

        if article is None:
            return "Article is None {}".format(headline.url)

        article, created = Article.objects.update_or_create(headline=article.headline,
                                                            defaults=article.update_or_create_defaults())

        if len(article.revisions) is 0:
            revision.article = article
            revision.version = 0
            revision.save()
            save_content(content_list, revision)

        else:
            revisions = list(article.revisions)
            revisions.sort(key=lambda rev: rev.version, reverse=True)
            last_revision = revisions[0]
            content = list(map(lambda x: x[0], content_list))
            content.sort(key=lambda content_node: content_node.pos)
            old_content = list(last_revision.contents)
            old_content.sort(key=lambda content_node: content_node.pos)
            # Create a boolean value that if it changes value we know that the content has been altered
            # and therefore save it as a new revision
            same = True
            if len(old_content) != len(content):
                same = False
            else:
                for i in range(len(old_content)):
                    if old_content[i] != content[i]:
                        same = False
                        diff = Diff(diff=Differ(old_content[i].content, content[i].content).diff)
                        diff.article = article
                        diff.save()

            if not same:
                revision.article = article
                revision.version = len(article.revisions)
                revision.save()
                save_content(content_list, revision)

                # for index in range(len(last_revision.contents)):
                #     if index < len(last_revision.contents) and index < len(revision.contents):
                #         if last_revision.contents[index].content != revision.contents[index].content:
                #             diff = Diff(diff=Differ(last_revision.contents[index].content, revision.contents[index].content).diff)
                #             diff.article = article
                #             diff.save()
                #             print(diff)
                #     else:
                #         if len(last_revision.contents) < len(revision.contents):
                #             diff = Diff(diff=Differ('', revision.contents[index].content).diff)
                #         else:
                #             diff = Diff(diff=Differ(last_revision.contents[index].content, '').diff)
                #         diff.article = article
                #         diff.save()
                #         print(diff)



    return 'SUCCESS scrape one article'


def add_article_journalists(revision, journalists):
    """Adds journalists to the article

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
    """Adds journalists to the article

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
    """Adds photographers to the article image

    Args:
        image (ArticleImage): The image taken by the photographers
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


def save_content(content_list, revision) -> None:
    """Save content and connect it to a revision
    A function that adds a foreign key to Content from revision
    It also creates a foreign key to Content from child
    This allows you to use a content node to grab all children nodes
    This makes it possible to recreate the HTML structure from the database

    Args:
        content_list ((str, [int])): (content, children_id_list)
        revision (Revision): Already stored Revision object that we want connect this content to

    Returns:
        None
    """

    visited = [False] * len(content_list)
    for content, children in content_list:
        if not visited[content.pos]:
            visited[content.pos] = True
            content.revision = revision
            content.save()
            for child in children:
                if not visited[child]:
                    visited[child] = True
                    child_content = content_list[child][0]
                    child_content.revision = revision
                    child_content.save()
                    Child(content=content, child=child)


@shared_task(name='Find an article and make a change')
def scrape_site_for_a_article_of_type_article(headline):
    scrape_article(headline)
    scrape_article_with_change(headline, 'This is a change')
    # Need to create a version of the articles content nodes

    return "Scraped article: " + str(headline)

@shared_task(name="Scrape one article with changes")
def scrape_article_with_change(headline, change: str):
    """This tasks will be called from scrape_articles and will download and store an article that is found in a headlines a tag.

    Args:
        headline (Headline): reference to the headline object that we are scraping from.
        change (str): the change to the content nodes

    Returns
        None
    """
    if headline.category == Headline.ARTICLE:

        scraper = ArticleScraper(headline)
        revision, article, journalists, images, content_list = scraper.scrape()

        if article is None:
            return "Article is None {}".format(headline.url)

        article, created = Article.objects.update_or_create(headline=article.headline,
                                                            defaults=article.update_or_create_defaults())
        for content, element in content_list:
            if content.content:
                content.content = change

        if len(article.revisions) is 0:
            revision.article = article
            revision.version = 0
            revision.save()
            save_content(content_list, revision)

        else:
            revisions = list(article.revisions)
            revisions.sort(key=lambda rev: rev.version, reverse=True)
            last_revision = revisions[0]
            content = list(map(lambda x: x[0], content_list))
            content.sort(key=lambda content_node: content_node.pos)
            old_content = list(last_revision.contents)
            old_content.sort(key=lambda content_node: content_node.pos)
            # Create a boolean value that if it changes value we know that the content has been altered
            # and therefore save it as a new revision
            same = True
            if len(old_content) != len(content):
                same = False
            else:
                for i in range(len(old_content)):
                    if old_content[i] != content[i]:
                        same = False
                        diff = Diff(diff=Differ(old_content[i].content, content[i].content).diff)
                        diff.article = article
                        diff.save()
            if not same:
                revision.article = article
                revision.version = len(article.revisions)
                revision.save()
                save_content(content_list, revision)

    return 'SUCCESS scrape one article'
