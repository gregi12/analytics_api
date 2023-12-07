from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class EmailUser(AbstractUser):

    username = models.EmailField(unique=True, default="")
    url = models.URLField(max_length=1000, default="")
    
    REQUIRED_FIELDS = ['url']

    def __str__(self):
        return self.email
    
class SiteInfo(models.Model):

    url = models.URLField(max_length=1000)
    ip_address = models.GenericIPAddressField()
    http_header = models.CharField(max_length=1000)
    user_agent_header = models.CharField(max_length=1000)
    window_width= models.IntegerField()
    window_height = models.IntegerField()
    max_touch_points = models.IntegerField()
    language = models.CharField(max_length=30)