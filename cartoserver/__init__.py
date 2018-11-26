APP_NAME = 'cartoserver'
ARCGIS_SUPPORTED_VERSION = 10.2
# templates
MANAGER_BASE_TPL = APP_NAME + "/manager/base.html"
MANAGER_HOME_TPL = APP_NAME + "/manager/index.html"
MANAGER_GEOTABLES_ADD_TPL = APP_NAME + "/manager/geotables_add.html"

REST_ENDPOINT_BASE_HTML_TPL = APP_NAME + "/REST_endpoint/html/base.html"
REST_ENDPOINT_FOLDER_TPL = APP_NAME + "/REST_endpoint/html/folder.html"
REST_ENDPOINT_SERVICE_TPL = APP_NAME + "/REST_endpoint/html/service.html"
REST_ENDPOINT_LAYER_TPL = APP_NAME + "/REST_endpoint/html/layer.html"
REST_ENDPOINT_LAYER_QUERY_TPL = APP_NAME + "/REST_endpoint/html/layer_query.html"


# urls
MANAGER_HOME_URL_NAME = APP_NAME + '_home'
MANAGER_GEOTABLES_ADD_URL_NAME  = APP_NAME + '_geotable_add'
# NEW_URL_NAME = APP_NAME + '_new'
# PUBLISH_URL_NAME = APP_NAME + '_publish'
# SAVE_NEW_LAYER_URL_NAME = APP_NAME + "_save_new_layer"

# GeoServices REST end point urls
SERVER_INFO_URL_NAME = APP_NAME + '_server_info'
FOLDER_INFO_URL_NAME = APP_NAME + '_folder_info'
SERVICE_INFO_URL_NAME = APP_NAME + '_service_info'
LAYER_INFO_URL_NAME = APP_NAME + "_layer_home"
LAYER_QUERY_URL_NAME = APP_NAME + "_layer_query"
FEATURE_ATTACHMENT_URL_NAME = APP_NAME + "_feature_attachment"
FEATURE_DELETE_ATTACHMENT_URL_NAME = APP_NAME + "_feature_delete_attachment"
FEATURE_ATTACHMENT_INFO_URL_NAME = APP_NAME + "_feature_attachment_info"
FEATURE_ADD_ATTACHMENT_URL_NAME = APP_NAME + "_feature_add_attachment"
LAYER_APPLY_EDITS_URL_NAME = APP_NAME + "_layer_applyEdits"
LAYER_ADD_FEATURES_URL_NAME = APP_NAME + "_layer_addFeatures"
LAYER_UPDATE_FEATURES_URL_NAME = APP_NAME + "_layer_updateFeatures"
LAYER_DELETE_FEATURES_URL_NAME = APP_NAME + "_layer_deleteFeatures"

TILES_SERVICE_URL_NAME = APP_NAME + "_tiles_service"
TILES_PREVIEW_URL_NAME = APP_NAME + "_tiles_preview"

# templates

# settings templates
SETTINGS_TPL = APP_NAME + '/settings.html'

# urls

NEW_URL_NAME = APP_NAME + '.new'
PUBLISH_URL_NAME = APP_NAME + '.publish'
SAVE_NEW_LAYER_URL_NAME = APP_NAME + ".save_new_layer"

# settings urls
SETTINGS_URL_NAME = APP_NAME + '.settings'

# permissions
ADD_SERVICE_PERMISSION = APP_NAME + '.add_service'
CHANGE_SERVICE_PERMISSION = APP_NAME + '.change_service'

ANGULAR_TEMPLATE_BASE = APP_NAME + '/manager/angular/'
ANGULAR_TEMPLATE_URL_NAME = APP_NAME + ".angular.templates"



