# Source code for NewsInspector's server
Goal, API that delivers meta data for headlines and articles from Norwegian newspapers.

The server has two jobs:
1. Provide a API that retrieve data from database
2. Scrape data from the newspapers

## Setup
This installation guide assumes that you have root access and are running Ubuntu.

### Step by Step Guide
Start the virtual environment or create one.
```bash
# Creates a virtualenv that is calles venv
# Skip this if you already have the environment set up
$ virtualenv -p Python3 venv
```
Activate it
```bash
# Activate environment so we can work in independent of the system settings
$ source venv/bin/activate
```
Move to root directory for the server (the place where you have the manage.py file)
```bash
$ cd bait-block-server
# Install requirements
$ pip install -r requirements.txt
```

The fixtures are data previously stored in the database that we can reload into the database.
The fixtures in this project is the templates for the news pages that the plugin is supporting.
This is a step you can skip, but then you need to add support for the pages you want the server to support by population the database with templates.

```bash
### This will load predefined fixtures in the correct order
### Skip this step if you ONLY want to add pages of your choosing
$ python3 LoadFixtures.py
```

### Scrape data from all sites to create test data
Start the Django shell

```bash
$ ./manage.py shell
```
Now import task and run it eagerly
```python3
from scraper.tasks import scrape_all_sites
scrape_all_sites.apply()
```


## Celery
Celery is a framework to run asynchronous tasks. These tasks can be run periodically and that is what is used in this project to scrape the pages every 20 minutes. A periodic task can be started by the user, but a better practise is to set up a service that starts with the operating system.
This service is called a beat or something on ubuntu and looks like this:
