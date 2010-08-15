from templator.conf.settings import *

DEBUG = True

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = os.path.join(PROJECT_PATH, 'conf', 'local', 'dev.db')

UNSAFE_PATHS = (
    '/path/to/site-packages/',
    '/path/to/django-templator/',
)

ROOT_URLCONF = 'templator.conf.local.urls'

