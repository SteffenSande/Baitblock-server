import os

from django.conf import settings
from wordcloud import WordCloud


def generate(text, store_folder, filename):
    """
        Generates a word cloud

        Args:
            text (str): Text to generate word cloud from
            store_folder (str): Folder to store the generated image in
            filename (str): The word cloud filename

        Stop words:
            Ref: https://www.wis.no/999/147/33899-170.html

        Returns:
            relative path to the generated image file from the media folder
    """

    with open(os.path.join(os.path.dirname(__file__), 'norwegian_stop_words.txt'), 'r', encoding='utf-8') as f:
        stop_words = set(map(str.strip, f.readlines()))

    wordcloud = WordCloud(width=1280, height=720, stopwords=stop_words)
    wordcloud.generate(text)

    folder = os.path.join(settings.WORD_CLOUD_FOLDER, store_folder)

    try:
        os.makedirs(folder)
    except OSError:
        # Directory exists, no need to create
        pass

    path = os.path.join(folder, filename)

    file = wordcloud.to_file(path)
    return os.path.join(settings.MEDIA_URL, path.split(settings.MEDIA_ROOT)[-1][1:])


def word_cloud_of_headlines(headlines, file_folder, filename):
    """
        Generates a word cloud based on headlines

        Args:
            headlines (list[Headline]): Headlines to generate word cloud from
            file_folder (str): Folder to store the generated image in
            filename (str): The word cloud filename

        Returns:
            relative path to the generated image file from the media folder
    """

    def get_title_from_headline(headline):
        try:
            return headline.revision.title + ' '
        except AttributeError:
            return ' '

    text = ''.join(list(map(get_title_from_headline, headlines)))
    return generate(text, file_folder, filename)
