from django.conf.urls import include, url
from . import *
from cartoserver.urls import geo_services_rest_patterns
from .views import layer_list, layer_edit

manager_urls = [
    url(r'^$', layer_list, name=LAYER_LIST_URL_NAME),
    url(r'^layer/edit/(?P<layer_name>[^/]*)$',
        layer_edit, name=LAYER_EDIT_URL_NAME),
]

urlpatterns = [
    url(r'^', include(manager_urls)),
    url(r'^arcgis/rest/', include(geo_services_rest_patterns)),
    url(r'^portal/',
        include('cartoview_arcgis_feature_server.cartoportal.urls')), ]
