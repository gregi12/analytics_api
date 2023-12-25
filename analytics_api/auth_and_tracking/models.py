from django.db import models
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import datetime
from urllib.parse import urlparse
from analytics_api import settings


class EmailUser(AbstractUser, PermissionsMixin):

    username = models.EmailField(unique=True, default="")
    url = models.URLField(max_length=1000, default="")
    domain = models.CharField(max_length=1000, default="")
    groups = models.ManyToManyField(Group, related_name='email_users')

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='email_users',
        blank=True,
        )

    def make_domain(self):
        parsed_url = urlparse(self.url)
        domain_name = parsed_url.netloc
        self.domain = domain_name
    
    def save(self, *args, **kwargs):
        self.make_domain()
        super().save(*args, **kwargs)
 
    REQUIRED_FIELDS = ['url']

    def __str__(self):
        return self.email
    
class SiteInfo(models.Model):

    user_id = models.IntegerField(default=0)
    url = models.URLField(max_length=1000)
    ip_address = models.GenericIPAddressField()
    http_header = models.CharField(max_length=1000,default="")
    user_agent_header = models.CharField(max_length=1000)
    window_width= models.IntegerField(default=0)
    window_height = models.IntegerField(default=0)
    max_touch_points = models.IntegerField(default=0)
    language = models.CharField(max_length=30)
    time = models.DateTimeField(default = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    domain = models.CharField(max_length=1000, default="")

    def make_domain(self):
        parsed_url = urlparse(self.url)
        domain_name = parsed_url.netloc
        self.domain = domain_name
    
    
    def save(self, *args, **kwargs):
        self.make_domain()
        super().save(*args, **kwargs)