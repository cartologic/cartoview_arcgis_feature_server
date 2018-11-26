from django.conf.urls import patterns, include, url

import views
import manager.views as manager_views
# import tiles.views as tiles_views

from . import *

geo_services_rest_patterns = patterns('',
    url(r'^info', views.server_info, name=SERVER_INFO_URL_NAME),


    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/applyEdits',
      views.layer_apply_edits, name=LAYER_APPLY_EDITS_URL_NAME),
    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/addFeatures',
      views.layer_add_features, name=LAYER_ADD_FEATURES_URL_NAME),
    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/updateFeatures',
      views.layer_update_features, name=LAYER_UPDATE_FEATURES_URL_NAME),
    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/deleteFeatures',
      views.layer_delete_features, name=LAYER_DELETE_FEATURES_URL_NAME),

    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/(?P<feature_id>[^/]+)/deleteAttachments',
      views.delete_attachment, name=FEATURE_DELETE_ATTACHMENT_URL_NAME),

    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/(?P<feature_id>[^/]+)/attachments/(?P<attachment_id>[^/]+)',
      views.attachment, name=FEATURE_ATTACHMENT_URL_NAME),
    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/(?P<feature_id>[^/]+)/attachments',
          views.attachment_info, name=FEATURE_ATTACHMENT_INFO_URL_NAME),
    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/(?P<feature_id>[^/]+)/addAttachment',
          views.add_attachment, name=FEATURE_ADD_ATTACHMENT_URL_NAME),

    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0/query', views.layer_query,
      name=LAYER_QUERY_URL_NAME),
    url(r'^services/(?P<service_name>[^/]+)/FeatureServer/0', views.layer_info,
      name=LAYER_INFO_URL_NAME),
    url(r'^services/(?P<service_name>[^/]+)/FeatureServer', views.service_info,
      name=SERVICE_INFO_URL_NAME),
    url(r'^services', views.folder_info, name=FOLDER_INFO_URL_NAME),
)
# tiles_urls_patterns = patterns('',
#     url(r'^(?P<service_slug>[^/]+)/tiles/(?P<z>[^/]+)/(?P<x>[^/]+)/(?P<y>[^/]+)\.(?P<extension>.+)$', tiles_views.tiles, name=TILES_SERVICE_URL_NAME),
#     url(r'^preview/(?P<service_slug>[^/]+)', tiles_views.preview_service, name=TILES_PREVIEW_URL_NAME),
#     url(r'^(?P<service_slug>[^/]+)/style.xml', tiles_views.xml_view),
# )
partial_patterns = patterns('',
    url(r'^(?P<template>.*)$', manager_views.angular_template, name=ANGULAR_TEMPLATE_URL_NAME),
    # ... more partials ...,
)
from tastypie.api import Api
from .rest import  FeatureLayerResource
# from .manager.datastores.rest import DatastoreResource
rest_api = Api()
# rest_api.register(GeoTableResource())
rest_api.register(FeatureLayerResource())
# rest_api.register(DatastoreResource())
# rest_api.register(TilesLayerResource())
# rest_api.register(TilesServiceResource())
# from .manager.datastores.rest import PostGISDataStoreResource
# rest_api.register(PostGISDataStoreResource())


urlpatterns = patterns('',
    url(r'^$', manager_views.home, name=MANAGER_HOME_URL_NAME),
    (r'^rest/', include(rest_api.urls)),
    # url(r'^tiles/', include(tiles_urls_patterns)),
    url(r'^upload/$', manager_views.upload, name=NEW_URL_NAME),
    url(r'^publish/$', manager_views.publish, name=PUBLISH_URL_NAME),
    url(r'^save_new/$', manager_views.save_new, name=SAVE_NEW_LAYER_URL_NAME),
    url(r'^arcgis/rest/', include(geo_services_rest_patterns)),
    url(r'^angular/templates/', include(partial_patterns, namespace=APP_NAME + '_angular_partials')),
)
