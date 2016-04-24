__author__ = 'Ahmed Nour Eldeen'

from django.db import models
from uuidfield import UUIDField
import datetime
from django.conf import settings
from ..models import Item


class Group(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    isInvitationOnly = models.BooleanField(default=False, null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s')
    description = models.TextField(null=True, blank=True)
    snippet = models.CharField(max_length=50, null=False, blank=False)
    tags = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    thumbnail = models.ImageField(null=False, blank=False, upload_to='GIS_Portal/')
    created = models.DateTimeField(null=False, blank=False, default=datetime.datetime.today())
    modified = models.DateTimeField(null=False, blank=False, default=datetime.datetime.today())
    # The access privileges of the group that determine who can see and access the group. Can be: private, org, or public.
    # access = models.CharField()
    items = models.ManyToManyField(Item)

    class Meta:
        app_label = 'arcportal'