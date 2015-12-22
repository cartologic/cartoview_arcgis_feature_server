from django.conf.urls import patterns, include, url
from . import *
from cartoserver.urls import geo_services_rest_patterns
from .views import layer_list, layer_edit

manager_urls = patterns('',
    url(r'^$', layer_list, name=LAYER_LIST_URL_NAME),
    url(r'^layer/edit/(?P<layer_name>[^/]*)$', layer_edit, name=LAYER_EDIT_URL_NAME),
)

urlpatterns = patterns('',
   url(r'^', include(manager_urls)),
   url(r'^arcgis/rest/', include(geo_services_rest_patterns)),
)
