# Source code for NewsInspector's server
## Goal
API that delivers Meta-Data for headlines and articles from Norwegian newspapers.  The server has two jobs:
1. Provide an API that retrieve data from database
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
# Activate virtual environment
$ source venv/bin/activate
```
Move to root directory for the server (the place where you have `manage.py`)
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
Now import task and run it.

This code is inside the script `scrape.py` in the root folder.
There has been a tendency to type these lines when troubleshooting the program.
Therefore, it could be wise to create a small script for it and place it in the environment's path `venv/bin/your_scirpt_here`.
```python3
from scraper.tasks import scrape_all_sites
scrape_all_sites.apply()
```



## Celery
Celery is a framework to run asynchronous tasks. These tasks can be run periodically and that is what is used in this project to scrape the pages every 20 minutes.
A periodic task can be started by the user, but it is better practice to set up a service that starts with the operating system.
His service is called a beat or something on Ubuntu and looks like this:
