__author__ = 'Ahmed Nour Eldeen'

from token_manager.models import *
from content.models import *
from community.models import *

"""
This File to contain common models and sub-packages models
"""


# TODO: use ItemBase model as a base model for items and groups (this model is not used yet).

class ItemBase(models.Model):
    id = UUIDField(primary_key=True, auto=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s')
    # resource = models.ForeignKey(Resource, related_name='%(app_label)s_%(class)s')
    created = models.DateTimeField(null=False, blank=False, default= datetime.datetime.today())
    modified = models.DateTimeField(null=False, blank=False, default=datetime.datetime.today())
    title = models.CharField(max_length=50, null=False, blank=False)
    type_keywords = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=200, null=False, blank=False)
    snippet = models.CharField(max_length=50, null=False, blank=False)
    thumbnail = models.ImageField(null=False, blank=False, upload_to='GIS_Portal/')
    # access

    class Meta:
        app_label = 'arcportal'
        abstract = True

