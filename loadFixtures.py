#!/usr/bin/env python3
import os

urls = 'articleScraper/fixtures/urlTemplates.json'
articles = 'articleScraper/fixtures/articleTemplates.json'
headlines = 'headlineScraper/fixtures/*'
scraper = 'scraper/fixtures/*'
comand = './manage.py loaddata '

os.system(comand + articles)
os.system(comand + headlines)
os.system(comand + scraper)
os.system(comand + urls)
