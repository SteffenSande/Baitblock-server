### This is a project that aims to make an api that gives information about norwegian news
### Create test Data
Start the virtual environment or create one.
```bash
# Creates a virtualenv that is calles venv
# Skip this if you already have the environment set up
virtualenv -p Python3 venv
```
Activate it
```bash
# Activate environment so we can work in independent of the system settings
source venv/bin/activate
```
Move to root directory for the server (the place where you have the manage.py file)
```bash
cd bait-block-server
# Install requirements
pip install -r requirements.txt
```
Start the django shell

```bash
./manage.py shell
```
Now import task and run it eagerly

```python3
from scraper.tasks import scrape_all_sites
scrape_all_sites.apply()
```
