__author__ = 'Ahmed Nour Eldeen'

from django.db import models
from django.conf import settings

class Token(models.Model):
    token = models.CharField(max_length=64, blank=False, null=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s')
    expiration_date = models.BigIntegerField()

    class Meta:
        app_label = 'arcportal'
