import re

from articleScraper.models import ArticleUrlTemplate


def persist_or_get_latest_revision(latest, revision, document=None):
    """
            Creates a new revision if there does not exists already one,
            or if the one existing has a older timestamp

            Args:
                latest:
                    The latest revision from the database
                revision:
                    Current scraped revision
                document:
                    Html document of the revision

            Return:
                returns the new or latest revision
        """
    from django.conf import settings

    if not latest.timestamp:
        if not revision.timestamp:
            return latest
    elif not revision.timestamp:
        return latest
    elif revision.timestamp <= latest.timestamp:
        return latest

    revision.file = latest.file
    revision.version = latest.version + 1
    revision.save()

    if document:
        save_file(revision.file_path(settings.FILE_PATH_FIELD_DIRECTORY), document)
    return revision


def format_url_for_site(url, site_url):
    """
        Formats a url to follow standard http(s)://example.com

        Args:
            url (str):
                The url to format

            site_url (str):
                Base url for the news site
    """

    regex = re.compile('http://|https://')
    non_alpha_numeric_regex = r'^[^«0-9a-zA-Z]*'
    url = re.sub(non_alpha_numeric_regex, '', url.replace('\n', ' '))

    if url.endswith('/'):
        url = url[:-1]

    if url.startswith('www'):
        return 'https://' + url

    if not regex.match(url):
        if url[0] == '/':
            url = url[1:]

        return '{}/{}'.format(site_url, url)

    return url


def get_user_ip(request):
    return request.META.get('HTTP_X_FORWARDED_FOR', '0.0.0.0')


def text_differ(text1, text2):
    """
    Checks if the two strings are equal or not.
    Args:
        text1 (str):
        text2 (str):

    Returns:
        True if not equal, False otherwise
    """
    return text1 != text2


def read_file_content_as_string(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return ''.join(file.readlines())


def save_file(file_path: str, content: str)-> None:
    """
    Creates a file with content.
    If the path does not exists, i.e folders in the path does not exists, then they will be created.

    Args:
        file_path (str): Path to the location where the file is saved
        content (str): Content of the file

    Returns (None): None

    """
    import os
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, encoding='utf-8', mode='w') as file:
        file.write(content)


def string_is_number(s):
    """
        Wrapper for isdigit()
        Replaces first . with space, so it includes float.


        Based on https://stackoverflow.com/a/23639915

        Returns:
            Returns True is string is a number.
    """
    return s.replace('.', '', 1).isdigit()


def find_headline_id(headline_url, url_templates):
    """
    Retrieves the id portion of a url based
        Args:
            headline_url (str): The url of a headline .
            url_templates (List[ArticleUrlTemplate]): Templates for a particular site
                which specify where in the url the id portion is at.

        Returns (str): The id portion of the url or empty string.
    """
    url = headline_url.split('/')

    # Iterate thorough all url tempaltes for that site
    for url_template in url_templates:

        url_id = url[url_template.id_position]
        if url_template.id_separator:
            url_id = url_id.split(url_template.id_separator)[-1]

        if len(url_id) == url_template.id_length:

            # Checks id type
            if url_template.id_type == ArticleUrlTemplate.ALPHA_NUMERIC:
                if url_id.isalnum():
                    return url_id
            elif url_template.id_type == ArticleUrlTemplate.LETTERS_ONLY:
                if url_id.isalpha():
                    return url_id
            elif url_template.id_type == ArticleUrlTemplate.NUMBERS_ONLY:
                if string_is_number(url_id):
                    return url_id
            elif url_template.id_type == ArticleUrlTemplate.OTHER:
                return url_id

    # No match...
    return ""


def extract_hostname(url):
    from urllib.parse import urlparse

    netloc = urlparse(url).netloc
    if not netloc:
        return None

    # In case the netloc is abc.site.com
    # then remove all subdomains
    splitted_hostname = netloc.replace('www.', '').split('.')
    return '{}.{}'.format(splitted_hostname[-2], splitted_hostname[-1])
