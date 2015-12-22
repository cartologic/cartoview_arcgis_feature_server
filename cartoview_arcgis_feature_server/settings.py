__author__ = 'kamal'
from geonode.cartoview_settings import CARTOVIEW_APPS
import os, sys
APP_NAME = 'cartoview_arcgis_feature_server'
current_folder = os.path.dirname(__file__)
# because of using execfile instead of import in the project settings file current_folder will refer to project folder
current_folder = os.path.abspath(os.path.join(current_folder, os.path.pardir, 'cartoview', 'apps', APP_NAME))
sys.path.append(os.path.join(current_folder, 'libs'))
CARTOVIEW_APPS += ('cartoview.apps.%s.cartoserver' % APP_NAME,)
GEO_SERVICES_LAYERS_PROVIDER = 'cartoview.apps.%s.layers_providers.GeonodeLayersProvider' % APP_NAME