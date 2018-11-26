__author__ = 'kamalhg'
from ..views import response_to_json, DynamicObject
from .models import PostGISDataStore


def get_db_settings(request):
    context = DynamicObject(PostGISDataStore.get_default_datasore_settings())
    return response_to_json(request, context)


def save_default_settings(request):
    context = DynamicObject(PostGISDataStore.get_default_datasore_settings())
    return response_to_json(request, context)