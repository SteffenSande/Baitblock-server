#!/usr/bin/env python3
import os 

comand = './manage.py dumpdata '
options = ' --format=json --indent=4 '

example = './manage.py dumpdata scraper.NewsSite > scraper/fixtures/sites.json --format=json --indent=4'

fixture = '/fixtures'
article = 'articleScraper'
headline = 'headlineScraper'
site = 'scraper'



folder = { 
        'articleTemplates':     article + fixture,
        'urlTemplates':         article + fixture,
        'headlineTemplates':    headline + fixture,
        'sites':                site + fixture
        }



apps = { 
        'articleTemplates':'articleScraper.ArticleTemplate',
        'urlTemplates':'articleScraper.ArticleUrlTemplate',
        'headlineTemplates':'headlineScraper.HeadlineTemplate',
        'sites':'scraper.NewsSite'
        }

def go_root():
    os.system('cd /home/steffen/dev/master/baitBlock-server/')
for app in apps:
    go_root()
    print(comand + apps[app] + options + '>' + folder[app] + '/'+ app + '.json')
    os.system(comand + apps[app] + options + '>' + folder[app] + '/'+ app + '.json')
    print('Created fixture with name: ' + app)




