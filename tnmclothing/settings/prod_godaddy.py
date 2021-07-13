from .base import *
from decouple import config
from dj_database_url import parse as dburl

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'api.sfmdropship.com']

CORS_ALLOWED_ORIGINS = [
    "https://sfmdropship.com",
    "https://www.sfmdropship.com",
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
default_dburl = 'sqlite:///' + str(BASE_DIR.joinpath('db.sqlite3'))

DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl)
}

if DATABASES['default']['ENGINE']!='django.db.backends.sqlite3':
    DATABASES['default']['ENGINE'] = 'mysql.connector.django'
    options_dict = {'autocommit': True}
    DATABASES['default']['OPTIONS'] = options_dict

# print(DATABASES)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent.joinpath('public_html/api.sfmdropship.com/media/')

FRONTEND_URL = "https://sfmdropship.com"

BACKEND_URL = "https://api.sfmdropship.com"