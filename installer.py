__author__ = 'kamal'
from .models import map_all_layers
from django.contrib.contenttypes.models import ContentType

info = {
    "title": "Cartoserver",
    "description": "Cartoview ArcGIS Feature Server implements ArcGIS Geoservices REST API and serves your GIS data stored in geonode as an ESRI ArcGIS featureservice.",
    "author": 'Cartologic',
    "home_page": 'http://cartologic.com/cartoview/apps/cartoserver',
    "help_url": "http://cartologic.com/cartoview/apps/cartoserver/help/",
    "tags": ['Feature Server'],
    "licence": 'BSD',
    "author_website": "http://www.cartologic.com",
    "single_instance": True
}


def install():
    # import os, sys
    # current_folder = os.path.dirname(__file__)
    # sys.path.append(os.path.join(current_folder, 'libs'))
    # from django.conf import settings
    # settings.INSTALLED_APPS += ('cartoview.apps.cartoview_arcgis_feature_server.cartoserver',)
    # from django.db.models.loading import load_app
    # load_app('cartoview.apps.cartoview_arcgis_feature_server.cartoserver')


def uninstall():
    # ContentType.objects.filter(app_label="cartoserver").delete()
    # ContentType.objects.filter(app_label="cartoview_arcgis_feature_server").delete()
