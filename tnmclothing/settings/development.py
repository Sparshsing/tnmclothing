from .base import *
from decouple import config
from dj_database_url import parse as dburl

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CORS_ALLOWED_ORIGINS = [
    "https://sparshsing.github.io",
    "http://localhost:3000",
    "https://sfmdropship.com",
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
default_dburl = 'sqlite:///' + str(BASE_DIR.joinpath('db.sqlite3'))

DATABASES = {
    'default': config('DATABASE_URL', default=default_dburl, cast=dburl)
}
# print(DATABASES)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

FRONTEND_URL = "http://localhost:3000/tnm-app"

BACKEND_URL = "http://localhost:8000"