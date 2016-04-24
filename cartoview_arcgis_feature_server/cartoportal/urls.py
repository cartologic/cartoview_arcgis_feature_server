from django.conf.urls import patterns, include, url
from . import *
from .views import map_publish, map_list, map_config_reset, map_edit, map_config_save
from arcportal import urls as arcportal_urls
manager_urls = patterns('',
    url(r'^$', map_list, name=MAP_LIST_URL_NAME),
    url(r'^map/edit/(?P<map_id>[^/]+)$', map_edit, name=MAP_EDIT_URL_NAME),
    url(r'^map/publish/(?P<map_id>[^/]+)$', map_publish, name=MAP_PUBLISH_URL_NAME),
    url(r'^map/config/save/(?P<map_id>[^/]+)$', map_config_save, name=MAP_CONFIG_SAVE_URL_NAME),
    url(r'^map/config/rest/(?P<map_id>[^/]+)$', map_config_reset, name=MAP_CONFIG_RESET_URL_NAME),
)

urlpatterns = patterns('',
   url(r'^', include(manager_urls)),
   url(r'^portal/', include(arcportal_urls)),
)
