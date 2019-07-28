try:
    from .base import *
except ImportError:
    print("There was an error importing the base settings")
    pass

DEBUG = True
ALLOWED_HOSTS = ['165.227.136.59', 'localhost', '127.0.0.1']
SECRET_KEY = "13"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'NewsInspector_db',
        'USER': 'NewsInspector_admin',
        'PASSWORD': 'Deb1sesgsS',
        'HOST': 'localhost',
        'PORT': '',
    }
}


FILE_PATH_FIELD_DIRECTORY = os.path.join(BASE_DIR, 'articles')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WORD_CLOUD_FOLDER = os.path.join(MEDIA_ROOT, 'word_cloud')
ARTICLE_DIFF_FOLDER = os.path.join(MEDIA_ROOT, 'article_diffs')
HEADLINE_TITLE_DIFF_FOLDER = os.path.join(MEDIA_ROOT, 'headline_title_diffs')
HEADLINE_SUB_TITLE_DIFF_FOLDER = os.path.join(MEDIA_ROOT, 'headline_sub_title_diffs')
