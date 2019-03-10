import abc
import collections
import datetime

import pytz
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parser


class Scraper(object):
    '''
    Abstract class that makes an object implement the method scrape.
    A scrape is basically downloading a page and grabbing the information that is needed from it.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, site, parsing_template):
        self.news_site = site
        self.parsing_template = parsing_template
        self.url = ""

    @abc.abstractmethod
    def scrape(self):
        pass

    def download(self):
        return requests.get(self.url)

    @staticmethod
    def base_get_text(element: BeautifulSoup, class_: str, method):
        text = ''
        text_set = element.select_one(class_)
        if text_set:
            text = method(text_set)
            if text:
                text = ' '.join(text.split()) # Is this to remove new lines and spaces, whyyyy
                text = text.rstrip()
        return text

    def get_text(self, element: BeautifulSoup, class_: str):
        return self.base_get_text(element, class_, lambda x: x.get_text())

    def get_text_no_children(self, element: BeautifulSoup, class_: str):
        return self.base_get_text(element, class_, lambda x: x.find(text=True, recursive=False))

    def parse_date(self, d):
        try:
            date, tokens = date_parser(self.replace_local_month(d), fuzzy_with_tokens=True)

            if date.tzinfo is not None and date.tzinfo.utcoffset(date) is not None:
                return date

            local = pytz.timezone(self.parsing_template.timezone)
            return local.localize(date, is_dst=None)
        except ValueError:
            return None
        except pytz.exceptions.NonExistentTimeError:
            return None

    @staticmethod
    def remove_words_in_date_string(key, date: datetime):
        if key in date:
            data_split_on_keyword = date.split(key)
            if len(data_split_on_keyword) > 1:
                data_split_on_keyword[1] = data_split_on_keyword[1].replace('.', ':')
            return ''.join(data_split_on_keyword)
        return date

    def replace_local_month(self, date):
        replace_in_datetime = collections.OrderedDict()
        replace_in_datetime['januar'] = '01'
        replace_in_datetime['februar'] = '02'
        replace_in_datetime['mars'] = '03'
        replace_in_datetime['april'] = '04'
        replace_in_datetime['mai'] = '05'
        replace_in_datetime['juni'] = '06'
        replace_in_datetime['juli'] = '07'
        replace_in_datetime['august'] = '08'
        replace_in_datetime['september'] = '09'
        replace_in_datetime['oktober'] = '10'
        replace_in_datetime['november'] = '11'
        replace_in_datetime['desember'] = '12'
        replace_in_datetime['okt'] = '10'

        localized_date = date.lower()

        localized_date = self.remove_words_in_date_string('kl.', localized_date)

        for key, value in replace_in_datetime.items():
            localized_date = localized_date.replace(key, value)

        return localized_date

    def get_datetime(self, article: BeautifulSoup, selector: str):
        node = article.select_one(selector)
        if node:
            try:
                if self.parsing_template.datetime_attribute:
                    date = node.attrs[self.parsing_template.datetime_attribute]
                    return self.parse_date(date)
                else:
                    date_text = self.get_text_no_children(article, selector)
                    return self.parse_date(date_text)
            except KeyError:
                date_text = self.get_text_no_children(article, selector)
                return self.parse_date(date_text)
        return None
