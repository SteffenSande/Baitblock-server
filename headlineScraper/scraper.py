import datetime

from bs4 import BeautifulSoup

from headlineScraper.models import Headline
from headlineScraper.models import Rank
from headlineScraper.models.revision import HeadlineRevision
from helpers.utilities import format_url_for_site
from scraper.models import NewsSite
from scraper.scraper import Scraper


class HeadlineScraper(Scraper):
    """
        Html scraping class.
        Uses BeautifulSoup to scrape certain sites for news headlines.
    """

    def __init__(self, site: NewsSite):
        """
            Constructor

            Args:
                site (NewsSite):
                    The site to be scraped
        """

        super(self.__class__, self).__init__(site, site.headlineTemplate)
        self.headlines = []
        self.url = site.url()

    def scrape(self):
        """
            Extracts values from the html and creates headline object
        """

        # Should raise exception...
        if not self.parsing_template:
            return None

        try:
            response = self.download()
        except:
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        if soup:
            soup = soup.select(self.parsing_template.headline)

        if soup is None:
            soup = []

        for headline in soup:
            if not headline:
                continue

            skip = False
            for exclude in self.parsing_template.exclude:
                if headline.select_one(exclude):
                    skip = True

            if not skip:
                success = self.parse(headline)
                if success:
                    self.headlines.append(success)

        # Post processing
        for revision, headline, rank in self.headlines:
            rank.of_total = len(self.headlines)
        return self.headlines

    def parse(self, headline: BeautifulSoup):
        """
           Extracts values from the html soup and creates headline object
           Args:
               headline (BeautifulSoup4):
                   A headline represented as html.
       """

        title = self.get_title(headline)
        url = self.get_url(headline)

        if not title or not url:
            return None

        sub_title = self.get_sub_title(headline)
        rank = Rank(placement=len(self.headlines) + 1, of_total=0)
        revision = HeadlineRevision(title=title, sub_title=sub_title, timestamp=datetime.datetime.now())
        head = Headline(news_site=self.news_site, url=url)
        return revision, head, rank

    def get_url(self, headline: BeautifulSoup):
        """
        Extracts the headline url

        Args:
            headline (BeautifulSoup): A Headline object represented as html.

        Returns (str): Hopefully the headline url

        """

        url = headline.select_one(self.parsing_template.url)
        if url:
            url = url.get('href')
            if url:
                return format_url_for_site(url, self.news_site.url())
        return url

    def get_title(self, headline: BeautifulSoup):
        """
        Extracts the headline title

        Args:
            headline (BeautifulSoup): A Headline object represented as html.

        Returns (str): Hopefully the headline title

        """
        return self.get_text(headline, self.parsing_template.title)

    def get_sub_title(self, headline: BeautifulSoup):
        """
        Extracts the headline sub_title

        Args:
            headline (BeautifulSoup): A Headline object represented as html.

        Returns (str): Hopefully the headline sub_title

        """
        if self.parsing_template.sub_title:
            return self.get_text(headline, self.parsing_template.sub_title)
        return ''