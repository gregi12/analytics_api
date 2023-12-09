from django.contrib import admin
from .models import EmailUser, SiteInfo

admin.site.register(EmailUser)
admin.site.register(SiteInfo)