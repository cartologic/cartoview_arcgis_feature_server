__author__ = 'kamal'
from cartoview.settings import CARTOVIEW_APPS
import os, sys
APP_NAME = 'cartoview_arcgis_feature_server'
import cartoview_arcgis_feature_server

current_folder = os.path.dirname(cartoview_arcgis_feature_server.__file__)
sys.path.append(os.path.join(current_folder, 'libs'))
CARTOVIEW_APPS += (
    '%s.cartoserver' % APP_NAME,
    '%s.cartoportal' % APP_NAME,
    '%s.cartoportal.arcportal' % APP_NAME,
)
GEO_SERVICES_LAYERS_PROVIDER = '%s.layers_providers.GeonodeLayersProvider' % APP_NAME