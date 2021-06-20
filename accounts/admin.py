from django.contrib import admin
from django.conf import settings


# Register your models here.
admin.site.site_url = settings.FRONTEND_URL
