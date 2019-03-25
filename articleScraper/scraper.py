import re

from bs4 import BeautifulSoup

from articleScraper.models import Article
from articleScraper.models import ArticleImage
from articleScraper.models import Revision
from articleScraper.models.child import Child
from articleScraper.models.journalist import Journalist
from articleScraper.models.photographer import Photographer
from articleScraper.models.content import Content

from headlineScraper.models import Headline

from scraper.scraper import Scraper


class ArticleScraper(Scraper):
    """
        Html scraping class.
        Uses BeautifulSoup to scrape certain sites for news headlines.
    """

    def __init__(self, headline: Headline):
        """
            Constructor

            Args:
                headline (Headline):
                    The headline for the article
        """
        super(self.__class__, self).__init__(headline.news_site, headline.news_site.articleTemplate)
        self.headline = headline
        self.article = None
        self.source = None

    def scrape(self):
        """
            Extracts values from the html and creates headline object
        """

        self.url = self.headline.url

        # Should raise exception...
        if not self.parsing_template:
            return None, None, None, None, None

        try:
            response = self.download()
            self.source = response.text
        except:
            return None, None, None, None, None

        soup = BeautifulSoup(response.content, "html.parser")

        if soup:
            return self.parse(soup)
        else:
            return None, None, None, None, None

    def scrape_file(self, file: str):
        """
            Extracts all content text from the article

            Args:
                file (str): filepath to the html file
        """
        try:
            with open(file, 'rb') as f:
                soup = BeautifulSoup(f.read().decode('utf-8'), "html.parser")
                return self.get_article_text(soup)
        except FileNotFoundError:
            return ''

    def parse(self, article: BeautifulSoup):
        """
           Extracts values from the html soup and creates a article object
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        title = self.get_title(article)
        sub_title = self.get_sub_title(article)
        published = self.get_published(article)
        updated = self.get_updated(article)
        words = self.get_words(article)
        journalists = self.get_journalist(article)
        images = self.get_images(article)
        subscription = self.get_subscription(article)
        content_list = self.get_content(article)

        if not title:
            title = self.headline.revisions[0].title

        if self.get_video():
            category = Article.VIDEO
        else:
            category = Article.ARTICLE

        if updated:
            time = updated
        else:
            time = published

        revision = Revision(timestamp=time, title=title, sub_title=sub_title, words=words, subscription=subscription)

        article = Article(news_site=self.news_site, headline=self.headline, category=category)

        return revision, article, journalists, images, content_list

    def get_images(self, article: BeautifulSoup):
        """
           Extracts all images from the article body
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        images = []
        content = article.select_one(self.parsing_template.content)

        if content:
            body_images = content.select(self.parsing_template.image_element)
        else:
            body_images = None

        if body_images:
            for element in body_images:

                img = element.find('img')
                if not img:
                    continue
                url = img.get(self.parsing_template.image_attribute)  # TODO format url correctly

                try:
                    text = self.get_text(element, self.parsing_template.image_text)
                except IndexError:
                    text = ''

                try:
                    photographer = self.get_text(element, self.parsing_template.image_photographer)
                except IndexError:
                    photographer = ''

                # Image text and photographer is not separated.
                # Tries to separate out the photographer
                if self.parsing_template.photographer_delimiter:
                    if text and not photographer:
                        text, photographer = self.parse_photographer(text, text)
                    if photographer:
                        text, photographer = self.parse_photographer(text, photographer)

                if url:
                    if photographer:
                        # Removes unwanted text in the photographer
                        for replace in self.parsing_template.photograph_ignore_text:
                            photographer = photographer.replace(replace, '')
                        photographer = photographer.replace('/', ',')

                    if len(text) > 255:
                        text = text[:254]

                    # Separate each photograph
                    photographers = []
                    for photograph in photographer.split(','):
                        photographer_name_split = list(filter(lambda x: x or x != ' ', photograph.split(' ')))
                        if photographer_name_split:
                            if len(photographer_name_split) == 1:
                                lastName = photographer_name_split[0].strip(' ').strip('.')
                                firstName = ''
                            else:
                                firstName = photographer_name_split[0].strip(' ')
                                lastName = photographer_name_split[1].strip(' ').strip('.')
                            photographers.append(Photographer(firstName=firstName, lastName=lastName))

                    images.append((ArticleImage(url=url, text=text), photographers))

        return images

    def parse_photographer(self, text, photographer):
        for delimiter in self.parsing_template.photographer_delimiter:
            if delimiter in photographer:
                image_text = list(filter(lambda x: x or x != ' ', photographer.split(delimiter)))
                if len(image_text) > 1:
                    return image_text[0].strip(), image_text[1].strip()

        return text, photographer

    def get_journalist(self, article: BeautifulSoup):
        """
           Extracts the journalists from the article
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        journalists = []
        journalists_nodes = article.select(self.parsing_template.journalist)
        if journalists_nodes:
            for journalist in list(map(lambda x: ' '.join(x.get_text().split()), journalists_nodes)):
                s = journalist.split(' ')
                journalists.append(Journalist(firstName=' '.join(s[:-1]), lastName=s[-1]))
        return journalists

    def get_article_text(self, article: BeautifulSoup):
        """
           Extracts the article text
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        # Removes unwanted elements in article, like ads
        for elm in article.find_all(self.parsing_template.ignore_content_tag):
            elm.decompose()

        return self.get_text(article, self.parsing_template.content)

    def get_words(self, article: BeautifulSoup):
        """
           Returns the word count of the article
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        return len(re.findall(r'\w+', self.get_article_text(article)))

    def get_title(self, article: BeautifulSoup):
        """
           Extracts the article title
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        return self.get_text(article, self.parsing_template.title)

    def get_sub_title(self, article: BeautifulSoup):
        """
           Extracts article sub title
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        return self.get_text(article, self.parsing_template.sub_title)

    def get_published(self, article: BeautifulSoup):
        """
           Extracts the articles published date
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        return self.get_datetime(article, self.parsing_template.published)

    def get_updated(self, article: BeautifulSoup):
        """
           Extracts the articles updated date
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
       """
        return self.get_datetime(article, self.parsing_template.updated)

    def get_subscription(self, article: BeautifulSoup):
        """
        Checks whether or not this article requires a subscription
           Args:
               article (BeautifulSoup4):
                   A article represented as html.
        """
        if self.parsing_template.subscription and article.select_one(self.parsing_template.subscription):
            return True
        return False

    def get_video(self):
        """
            Checks a url if it indicates that this link is for a video

        Returns (str): The url if it indicates a video, empty if not

        """
        if self.parsing_template.video and self.parsing_template.video in self.headline.url:
            return True
        return False

    def get_content(self, article: BeautifulSoup):
        # make it work for Dagbladet first
        search_for = ['p', 'h1', 'h2']
        content_list = []

        # Det er nok lurt å legge til posisjonen slik at du har noe å gå igjennom med etterpå.
        # Kan slippe det seinere eller du henter jo ut listen med alle content noder og da ligger posisjon der enda.

        def add_nodes_from(pos, node):
            """
            Method to create content nodes from scraped html nodes.

            :param pos: Position of parent
            :param node: What node to process
            :return: position of next node
            """
            if node.name is not None:
                children_list = []
                root = Content(pos=pos, tag=node.name)
                pos += 1
                for child in node.children:
                    pos = add_nodes_from(pos, child) + 1
                    children_list.append(pos)
                content_list.append((root, children_list))
                return pos

            else:
                leaf = Content(pos=pos, content=str(node))
                content_list.append((leaf, []))
                return pos + 1

        current_index = 0
        for content in article.find_all(search_for):
            if content.attrs == {}:  # Can later implement exclude tags
                new_pos = add_nodes_from(current_index, content)
                current_index = new_pos  # Kanskje pluss 1 her

        return content_list
