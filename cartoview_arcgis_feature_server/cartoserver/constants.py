__author__ = 'kamal'
from . import *
import json

MIMETYPES = dict(
    HRML="text/html",
    JSON="application/json",
    PJSON="application/json",
)
MAP_SERVER = "MapServer"

WFS_TYPES_TO_ESRI = dict(

    integer="esriFieldTypeInteger",
    float="esriFieldTypeSingle",
    number="esriFieldTypeDouble",
    double="esriFieldTypeDouble",
    long="esriFieldTypeInteger",

    string="esriFieldTypeString",
    object="esriFieldTypeString",
    timestamp="esriFieldTypeDate",

    point="esriFieldTypeGeometry",
    multipoint="esriFieldTypeGeometry",
    linestring="esriFieldTypeGeometry",
    multilinestring="esriFieldTypeGeometry",
    polygon="esriFieldTypeGeometry",
    multipolygon="esriFieldTypeGeometry",

    # esriFieldTypeSmallInteger="esriFieldTypeSmallInteger",
    # esriFieldTypeOID="esriFieldTypeOID",
    # esriFieldTypeBlob="esriFieldTypeBlob",
    # esriFieldTypeRaster="esriFieldTypeRaster",
    # esriFieldTypeGUID="esriFieldTypeGUID",
    # esriFieldTypeGlobalID="esriFieldTypeGlobalID",
    # esriFieldTypeXML="esriFieldTypeXML"
)

GEOMETRY_TYPES = dict(
    point="esriGeometryPoint",
    multipoint="esriGeometryMultiPoint",
    linestring="esriGeometryPolyline",
    multilinestring="esriGeometryMultiLine",
    polygon="esriGeometryPolygon",
    multipolygon="esriGeometryMultiPolygon",
)

SPATIAL_REF_DEFAULTS = {
    "wkid": 4326,
    "latestWkid": 4326
}
EXTENT_DEFAULTS = {
    "xmin": -180,
    "ymin": -90,
    "xmax": 180,
    "ymax": 90,
    "spatialReference": {
        "wkid": 4326,
        "latestWkid": 4326
    }
}
FOLDER_INFO_DEFAULTS = dict(
    currentVersion=ARCGIS_SUPPORTED_VERSION,
    services=[],
    folders=[]
)
SERVICE_INFO_DEFAULTS = {
    "currentVersion": ARCGIS_SUPPORTED_VERSION,
    "serviceDescription": "",
    "hasVersionedData": False,
    "supportsDisconnectedEditing": False,
    "hasStaticData": False,
    "maxRecordCount": 1000,
    "supportedQueryFormats": "JSON",
    "capabilities": "Query",
    "description": "",
    "copyrightText": "",
    "spatialReference": SPATIAL_REF_DEFAULTS,
    "initialExtent": EXTENT_DEFAULTS,
    "fullExtent": EXTENT_DEFAULTS,
    "allowGeometryUpdates": True,
    "units": "esriDecimalDegrees",
    "syncEnabled": False,
    "syncCapabilities": {
        "supportsASync": False,
        "supportsRegisteringExistingData": False,
        "supportsSyncDirectionControl": False,
        "supportsPerLayerSync": False,
        "supportsPerReplicaSync": False,
        "supportsRollbackOnFailure": False
    },
    "editorTrackingInfo": {
        "enableEditorTracking": False,
        "enableOwnershipAccessControl": False,
        "allowOthersToUpdate": False,
        "allowOthersToDelete": False
    },
    "documentInfo": None,
    # the feature layers published by this service
    "layers": [],
    # the non-spatial tables published by this service
    "tables": [],
    "enableZDefaults": False,
    "zDefault": None
}

#     {
#     "minScale": 0,
#     "maxScale": 0,
#     "units": "esriDecimalDegrees",
#     "supportedImageFormatTypes": "PNG",#"PNG32,PNG24,PNG,JPG,DIB,TIFF,EMF,PS,PDF,GIF,SVG,SVGZ,BMP",
#     "capabilities": "Query",
#     "supportedQueryFormats": "JSON",
#     "exportTilesAllowed": False,
#     "maxRecordCount": 1000,
#     "maxImageHeight": 4096,
#     "maxImageWidth": 4096,
#     "supportedExtensions": " WMSServer",
#     "currentVersion": ARCGIS_SUPPORTED_VERSION,
#     "copyrightText": "",
#     "supportsDynamicLayers": False,
#     "tables": [],
#     "spatialReference": SPATIAL_REF_DEFAULTS,
#     "initialExtent": EXTENT_DEFAULTS,
#     "fullExtent": EXTENT_DEFAULTS,
# }

LAYER_INFO_DEFAULTS = {
    "currentVersion": ARCGIS_SUPPORTED_VERSION,  # Added at 10.0 SP1
    # properties applicable to both feature layers and tables
    "id": 0,
    "name": "<layerOrTableName>",
    "type": "Feature Layer",  # or "Table"
    "displayField": None,
    "description": "",
    "copyrightText": "",
    "defaultVisibility": True,  # Added at 10.1
    # Added at 10.1
    "editFieldsInfo": None,
    # {
    #   "creationDateField": "<creationDateField>",
    #      "creatorField": "<creatorField>",
    #   "editDateField": "<editDateField>",
    #   "editorField": "<editorField>",
    #   "realm":"<realm>"
    # },
    # Added at 10.1
    "ownershipBasedAccessControlForFeatures": {
        "allowOthersToUpdate": False,
        "allowOthersToDelete": False,
        "allowOthersToQuery": False
    },
    # Added at 10.1
    "syncCanReturnChanges": False,
    "relationships": [],
    "isDataVersioned": False,  # Added at 10.1
    "supportsRollbackOnFailureParameter": False,  # Added at 10.1
    "supportsStatistics": False,  # Added at 10.1
    "supportsAdvancedQueries": False,  # Added at 10.1
    # properties applicable to feature layers only
    "geometryType": None,
    "minScale": 0,
    "maxScale": 0,
    "effectiveMinScale": 0,
    "effectiveMaxScale": 0,
    "extent": None,

    # for feature layers only
    "drawingInfo": None,
    "hasM": False,  # if the features in the layer have M values, the hasM property will be true
    "hasZ": False,  # if the features in the layer have Z values, the hasZ property will be true
    # if the layer / table supports querying based on time
    "enableZDefaults": False,  # Added at 10.1
    "zDefault": None,  # Added at 10.1
    "allowGeometryUpdates": True,  # Added at 10.1
    "timeInfo": None,

    # if the layer / table has attachments, the hasAttachments property will be true
    "hasAttachments": False,

    # from 10 onward - indicates whether the layer / table has htmlPopups
    "htmlPopupType": "esriServerHTMLPopupTypeNone",
# "<esriServerHTMLPopupTypeNone | esriServerHTMLPopupTypeAsURL | esriServerHTMLPopupTypeAsHTMLText>",

    # layer / table fields
    "objectIdField": "",
    "globalIdField": "",
    "typeIdField": "",
    # from 10.0 fields of type (String, Date, GlobalID, GUID and XML) have an additional length property, editable properties
    # from 10.1 fields have an additional nullable property
    "fields": [],

    # layer / table templates - usually present when the layer / table has no sub-types
    "templates": [],
    # Maximum number of records returned in a query result
    "maxRecordCount": 1000,  # Added at 10.1
    "supportedQueryFormats": "JSON",  # Added at 10.1
    "hasStaticData": False,
    # comma separated list of supported capabilities - e.g. "Create,Delete,Query,Update,Editing"
    "capabilities": "Create,Delete,Query,Update,Editing",

}

LAYER_QUERY_PARAMS_MAP = {
    'outfields': '',
    'gdbversion': '',
    'text': '',
    'returnm': False,
    'outsr': '',
    'returngeometry': True,
    'returnidsonly': False,
    'relationparam': '',
    'returnz': 'false',
    'orderbyfields': '',
    'geometrytype': 'esrigeometryenvelope',
    'maxallowableoffset': '',
    'groupbyfieldsforstatistics': '',
    'spatialrel': 'esrispatialrelintersects',
    'outstatistics': '',
    'returncountonly': 'false',
    'geometryprecision': '',
    'f': 'html',
    'geometry': '',
    'returndistinctvalues': 'false',
    'insr': '',
    'objectids': '',
    'time': '',
    'where': '',
    'callback': ''
}

QUERY_RESULT_DEFAULTS = dict(
    displayFieldName="NAME",
    fieldAliases={},
    spatialReference=SPATIAL_REF_DEFAULTS,
    fields=[],
    features=[]
)
OBJECTID_FIELD_DEFAULT = dict(
    name="OBJECTID",
    type="esriFieldTypeOID",
    alias="OBJECTID"
)
FEATURE_DEFAULTS = dict(
    attributes={},
    geometry={}
)

POINT_DRAWING_INFO_DEFAULTS = json.dumps({
    "renderer": {
		"type": "simple",
		"symbol": {
			"color": [
				77,
				77,
				77,
				255
			],
			"size": 6,
			"angle": 0,
			"xoffset": 0,
			"yoffset": 0,
			"type": "esriSMS",
			"style": "esriSMSCircle",
			"outline": {
				"color": [
					255,
					255,
					255,
					255
				],
				"width": 0.75,
				"type": "esriSLS",
				"style": "esriSLSSolid"
			}
		}
	}
}, indent=4)
LINE_DRAWING_INFO_DEFAULTS = json.dumps({
    "renderer": {
        "type": "simple",
        "symbol": {
            "type": "esriSLS",
            "style": "esriSLSDot",
            "color": [0, 0, 0, 255],
            "width": 1
        }
    }
}, indent=4)
POLYGON_DRAWING_INFO_DEFAULTS = json.dumps({
    "renderer": {
        "type": "simple",
        "symbol": {
            "type": "esriSFS",
            "style": "esriSFSSolid",
            "color": [255, 235, 59, 160],
            "outline": {
                "color": [200, 200, 200, 255],
                "width": 1
            }
        }
    }
}, indent=4)

DRAWING_INFO_DEFAULTS = dict(
    esriGeometryPoint=POINT_DRAWING_INFO_DEFAULTS,
    esriGeometryMultipoint=POINT_DRAWING_INFO_DEFAULTS,
    esriGeometryPolyline=LINE_DRAWING_INFO_DEFAULTS,
    esriGeometryPolygon=POLYGON_DRAWING_INFO_DEFAULTS,
    esriGeometryAny=POLYGON_DRAWING_INFO_DEFAULTS,
)

GEODJANGO_GEOMETRY_TYPES_TO_ESRI = dict(
    GEOMETRY="esriGeometryAny",
    POINT="esriGeometryPoint",
    LINESTRING="esriGeometryPolyline",
    POLYGON="esriGeometryPolygon",
    MULTIPOINT="esriGeometryMultipoint",
    MULTILINESTRING="esriGeometryPolyline",
    MULTIPOLYGON="esriGeometryPolygon",
    GEOMETRYCOLLECTION="",
)

from django.contrib.gis.db import models
DJANGO_FIELDS_TYPES_TO_ESRI = [
    [models.AutoField,"esriFieldTypeOID"],
    [models.SmallIntegerField,"esriFieldTypeSmallInteger"],
    [models.BigIntegerField,"esriFieldTypeInteger"],
    [models.IntegerField,"esriFieldTypeInteger"],
    [models.FloatField,"esriFieldTypeDouble"],
    [models.CharField,"esriFieldTypeString"],
    [models.DateTimeField,"esriFieldTypeDate"],
    [models.DateField,"esriFieldTypeDate"],
    [models.GeometryField,"esriFieldTypeGeometry"],
    [models.Field,"esriFieldTypeString"]
    # esriFieldTypeSmallInteger="esriFieldTypeSmallInteger",
    # esriFieldTypeOID="esriFieldTypeOID",
    # esriFieldTypeBlob="esriFieldTypeBlob",
    # esriFieldTypeRaster="esriFieldTypeRaster",
    # esriFieldTypeGUID="esriFieldTypeGUID",
    # esriFieldTypeGlobalID="esriFieldTypeGlobalID",
    # esriFieldTypeXML="esriFieldTypeXML"
]