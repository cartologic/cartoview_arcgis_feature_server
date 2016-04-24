__author__ = 'Ahmed Nour Eldeen'

from django.db import models
from uuidfield import UUIDField
import datetime
from django.conf import settings
from django.contrib.gis.db import models as gis_models



class Item(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s')
    # resource = models.ForeignKey(Resource, related_name='%(app_label)s_%(class)s')
    created = models.DateTimeField(auto_now_add=True) # changed by kamal to auto assign the creation time
    modified = models.DateTimeField(auto_now=True) # changed by kamal to auto assign the update time
    name = models.CharField(max_length=1000, null=False, blank=False, editable=False)
    title = models.CharField(max_length=1000, null=False, blank=False)
    url = models.URLField(null=True, blank=True)
    #  items can be classified as maps, layers, styles, tools, applications, and datafiles
    type = models.CharField(max_length=50, null=False, blank=False)
    type_keywords = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=200, null=False, blank=False)
    snippet = models.CharField(max_length=200, null=False, blank=False)
    thumbnail = models.ImageField(null=False, blank=False, upload_to='GIS_Portal/', max_length=1000)
    # documentation = models.CharField(max_length=100)
    extent = gis_models.PolygonField('Extent', srid = 4326, null = True, blank = True)
    # spatial_reference
    # access_information
    license_info = models.TextField()
    # culture
    # properties
    # Indicates the level of access to this item: private, shared, org, or public.
    # access

    class Meta:
        app_label = 'arcportal'


class ItemData(models.Model):
    item = models.ForeignKey(Item, related_name='%(app_label)s_%(class)s', primary_key=True)
    text = models.TextField(null=False, blank=False)

    class Meta:
        app_label = 'arcportal'