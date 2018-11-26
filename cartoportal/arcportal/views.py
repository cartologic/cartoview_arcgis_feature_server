__author__ = 'Ahmed Nour Eldeen'

from .json_response_utils import JsonResponse, JsonPResponse
from django.conf import  settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt

"""
    Get Portal (information and configuration)
"""


def sharing_home(request):
    response_json = {
        "currentVersion": "3.10"
    }
    if request.GET.get('callback'):
        return JsonPResponse(response_json, callback=request.GET.get('callback'))
    else:
        return JsonResponse(response_json, content_type="application/json")

def info(request):

    response_json = {
        "owningSystemUrl": settings.SITEURL[:-1] + reverse("arcportal_home")[:-1],
        "authInfo": {
            "tokenServicesUrl": settings.SITEURL [:-1] + reverse("arcportal_generate_token"),
            "isTokenBasedSecurity": True
        }
    }
    if request.GET.get('callback'):
        return JsonPResponse(response_json, callback=request.GET.get('callback'))
    else:
        return JsonResponse(response_json, content_type="application/json")

def portal(request):
    # TODO: handle this request with dynamic data(data configured in DB).
    portal_json = {}
    if 'clientAppType' in request.REQUEST:  # handle requests from ArcGIS dashboard and other special apps
        portal_json = {
            "access": "private",
            "basemapGalleryGroupQuery": "title:\"ArcGIS Online Basemaps\" AND owner:esri_en",
            "colorSetsGroupQuery": "title:\"Esri Colors\" AND owner:esri_en",
            "customBaseUrl": "maps.arcgis.com",
            "defaultBasemap": {
                "baseMapLayers": [{
                    "url": "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer",
                    "resourceInfo": {
                        "currentVersion": 10.01,
                        "copyrightText": "Sources: Esri, DeLorme, NAVTEQ, TomTom, Intermap, AND, USGS, NRCAN, Kadaster NL, and the GIS User Community",
                        "spatialReference": {
                            "wkid": 102100
                        },
                        "singleFusedMapCache": True,
                        "tileInfo": {
                            "rows": 256,
                            "cols": 256,
                            "dpi": 96,
                            "format": "JPEG",
                            "compressionQuality": 90,
                            "origin": {
                                "x": -2.0037508342787E7,
                                "y": 2.0037508342787E7
                            },
                            "spatialReference": {
                                "wkid": 102100
                            },
                            "lods": [{
                                "level": 0,
                                "resolution": 156543.033928,
                                "scale": 5.91657527591555E8
                            }, {
                                "level": 1,
                                "resolution": 78271.5169639999,
                                "scale": 2.95828763795777E8
                            }, {
                                "level": 2,
                                "resolution": 39135.7584820001,
                                "scale": 1.47914381897889E8
                            }, {
                                "level": 3,
                                "resolution": 19567.8792409999,
                                "scale": 7.3957190948944E7
                            }, {
                                "level": 4,
                                "resolution": 9783.93962049996,
                                "scale": 3.6978595474472E7
                            }, {
                                "level": 5,
                                "resolution": 4891.96981024998,
                                "scale": 1.8489297737236E7
                            }, {
                                "level": 6,
                                "resolution": 2445.98490512499,
                                "scale": 9244648.868618
                            }, {
                                "level": 7,
                                "resolution": 1222.99245256249,
                                "scale": 4622324.434309
                            }, {
                                "level": 8,
                                "resolution": 611.49622628138,
                                "scale": 2311162.217155
                            }, {
                                "level": 9,
                                "resolution": 305.748113140558,
                                "scale": 1155581.108577
                            }, {
                                "level": 10,
                                "resolution": 152.874056570411,
                                "scale": 577790.554289
                            }, {
                                "level": 11,
                                "resolution": 76.4370282850732,
                                "scale": 288895.277144
                            }, {
                                "level": 12,
                                "resolution": 38.2185141425366,
                                "scale": 144447.638572
                            }, {
                                "level": 13,
                                "resolution": 19.1092570712683,
                                "scale": 72223.819286
                            }, {
                                "level": 14,
                                "resolution": 9.55462853563415,
                                "scale": 36111.909643
                            }, {
                                "level": 15,
                                "resolution": 4.77731426794937,
                                "scale": 18055.954822
                            }, {
                                "level": 16,
                                "resolution": 2.38865713397468,
                                "scale": 9027.977411
                            }, {
                                "level": 17,
                                "resolution": 1.19432856685505,
                                "scale": 4513.988705
                            }, {
                                "level": 18,
                                "resolution": 0.597164283559817,
                                "scale": 2256.994353
                            }, {
                                "level": 19,
                                "resolution": 0.298582141647617,
                                "scale": 1128.497176
                            }
                            ]
                        },
                        "fullExtent": {
                            "xmin": -2.00375070671618E7,
                            "ymin": -1.99718688804086E7,
                            "xmax": 2.00375070671618E7,
                            "ymax": 1.99718688804086E7,
                            "spatialReference": {
                                "wkid": 102100
                            }
                        },
                        "supportedImageFormatTypes": "PNG24,PNG,JPG,DIB,TIFF,EMF,PS,PDF,GIF,SVG,SVGZ,AI,BMP",
                        "capabilities": "Map,Query,Data"
                    }
                }
                ],
                "title": "Topographic"
            },
            "defaultExtent": {
                "xmin": 2750000,
                "ymin": 2350000,
                "xmax": 4000000,
                "ymax": 3800000,
                "spatialReference": {
                    "wkid": 102100
                }
            },
            "description": None,
            "featuredGroups": [{
                "owner": "Federal_User_Community",
                "title": "National Maps for USA"
            }, {
                "owner": "esri",
                "title": "Esri Maps and Data"
            }, {
                "owner": "esri",
                "title": "Community Basemaps"
            }, {
                "owner": "esri",
                "title": "Landsat Community"
            }, {
                "owner": "esri_en",
                "title": "Web Application Templates"
            }, {
                "owner": "ArcGISTeamLocalGov",
                "title": "ArcGIS for Local Government"
            }
            ],
            "featuredItemsGroupQuery": "title:\"Featured Content\" AND owner:Esri_cy_EG",
            "galleryTemplatesGroupQuery": "title:\"Gallery Templates\" AND owner:esri_en",
            "helpBase": "http://doc.arcgis.com/en/arcgis-online/",
            "helpMap": {
                "v": "1.0",
                "m": {
                    "120000503": "administer/view-status.htm",
                    "120000905": "administer/configure-open-data.htm",
                    "120000897": "administer/configure-roles.htm",
                    "120000468": "create-maps/configure-pop-ups.htm",
                    "120000473": "create-maps/configure-time.htm",
                    "120000470": "create-maps/change-symbols.htm",
                    "120000464": "create-maps/make-your-first-map.htm",
                    "120000467": "create-maps/add-layers.htm#FILE",
                    "120000902": "share-maps/publish-features.htm",
                    "120000900": "share-maps/review-addresses.htm",
                    "120000923": "share-maps/share-maps.htm",
                    "120000455": "share-maps/share-items.htm",
                    "120000454": "share-maps/add-items.htm",
                    "120000456": "share-maps/supported-items.htm",
                    "120000899": "use-maps/take-maps-offline.htm",
                    "120000516": "reference/troubleshoot.htm#WEB_STORAGE",
                    "120000815": "reference/about-cityengine-web-viewer.htm",
                    "120000814": "reference/faq.htm",
                    "120000817": "reference/troubleshoot-cityengine-web-viewer.htm",
                    "120000816": "reference/use-cityengine-web-viewer.htm",
                    "120000461": "reference/videos.htm",
                    "120000463": "reference/show-desktop-content.htm",
                    "120000465": "reference/search.htm",
                    "120000466": "reference/troubleshoot-account.htm",
                    "120000469": "reference/shapefiles.htm",
                    "120000592": "reference/manage-trial.htm",
                    "120000471": "reference/kml.htm",
                    "120000597": "reference/arcgis-server-services.htm",
                    "120000966": "reference/scene-viewer-requirements.htm",
                    "120000978": "reference/multifactor.htm",
                    "120000980": "reference/profile.htm#MFA",
                    "120000969": "share-maps/add-items.htm#REG_APP",
                    "120000460": "index.html"
                }
            },
            "helperServices": {
                "geocode": [{
                    "url": "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer",
                    "northLat": "Ymax",
                    "southLat": "Ymin",
                    "eastLon": "Xmax",
                    "westLon": "Xmin"
                }
                ],
                "defaultElevationLayers": [{
                    "url": "https://elevation3d.arcgis.com/arcgis/rest/services/WorldElevation3D/Terrain3D/ImageServer",
                    "id": "globalElevation",
                    "layerType": "ArcGISTiledElevationServiceLayer"
                }
                ],
                "route": {
                    "url": "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World"
                },
                "geometry": {
                    "url": "https://utility.arcgisonline.com/arcgis/rest/services/Geometry/GeometryServer"
                },
                "printTask": {
                    "url": "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task"
                },
                "closestFacility": {
                    "url": "https://route.arcgis.com/arcgis/rest/services/World/ClosestFacility/NAServer/ClosestFacility_World"
                },
                "asyncClosestFacility": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/ClosestFacility/GPServer/FindClosestFacilities"
                },
                "traffic": {
                    "url": "https://traffic.arcgis.com/arcgis/rest/services/World/Traffic/MapServer"
                },
                "serviceArea": {
                    "url": "https://route.arcgis.com/arcgis/rest/services/World/ServiceAreas/NAServer/ServiceArea_World"
                },
                "asyncServiceArea": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/ServiceAreas/GPServer/GenerateServiceAreas"
                },
                "syncVRP": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/VehicleRoutingProblemSync/GPServer/EditVehicleRoutingProblem"
                },
                "asyncVRP": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/VehicleRoutingProblem/GPServer/SolveVehicleRoutingProblem"
                },
                "asyncLocationAllocation": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/LocationAllocation/GPServer"
                },
                "elevation": {
                    "url": "https://elevation.arcgis.com/arcgis/rest/services/Tools/Elevation/GPServer"
                },
                "hydrology": {
                    "url": "https://hydro.arcgis.com/arcgis/rest/services/Tools/Hydrology/GPServer"
                },
                "elevationSync": {
                    "url": "https://elevation.arcgis.com/arcgis/rest/services/Tools/ElevationSync/GPServer"
                },
                "asyncRoute": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/Route/GPServer"
                },
                "geoenrichment": {
                    "url": "https://geoenrich.arcgis.com/arcgis/rest/services/World/GeoenrichmentServer"
                }
            },
            "homePageFeaturedContent": "title:\"Featured Maps\" AND owner:Esri_cy_EG",
            "homePageFeaturedContentCount": 12,
            "isPortal": False,
            "layerTemplatesGroupQuery": "title:\"Esri Layer Templates\" AND owner:esri_en",
            "name": None,
            "portalHostname": "www.arcgis.com",
            "portalMode": "multitenant",
            "portalName": "ArcGIS Online",
            "portalThumbnail": None,
            "rotatorPanels": [{
                "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-1.jpg);display:block;' title='Create and Collaborate on Maps and Apps'><div class='contentWidth'><h1>Create and Collaborate on Maps and Apps<\/h1><p>ArcGIS Online is a cloud-based, collaborative content management system for maps, apps, data, and other geographic information.<\/p><a target='_blank' class='extralarge button green' href='/about/'>Learn More &raquo;<\/a><\/div><\/div><\/div>"
            }, {
                "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-2.jpg);display:block;' title='Your Maps, Your Way'><div class='contentWidth'><h1>Your Maps, Your Way<\/h1><p>Create, store, and manage your own maps, apps, and data with a personal ArcGIS Online account.<\/p><a target='_blank' class='extralarge button blue' href='/about/features.html'>Learn More &raquo;<\/a><\/div><\/div><\/div>"
            }, {
                "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-3.jpg);display:block;' title='The Geospatial Platform for Your Organization'> <div class='contentWidth'> <h1>The Geospatial Platform for Your Organization<\/h1><p>Host your organization's geographic information in Esri's cloud with an ArcGIS Online subscription.<\/p><a target='_blank' class='extralarge button green' href='/about/features.html#your-data-in-the-cloud'>Learn More &raquo;<\/a><\/div><\/div><\/div>"
            }, {
                "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-4.jpg);display:block;' title='Intelligent Web Maps'><div class='contentWidth'><h1>Intelligent Web Maps<\/h1><p>Turn your data into information by creating content-rich, beautiful maps that tell your story.<\/p><a class='extralarge button yellow' href='webmap/viewer.html?useExisting=1'>Get Started &raquo;<\/a><\/div><\/div><\/div>"
            }, {
                "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-5.jpg);display:block;' title='Any Map, Anywhere'><div class='contentWidth'><h1>Any Map, Anywhere<\/h1><p>Whether in the board room, at your desk, or in in the field, access the same map on all your devices.<\/p><a href='http://itunes.apple.com/us/app/arcgis/id379687930'><img src='CDN_SERVER/images/App_Store_Badge_en.png' alt='Download on the App Store'/><\/a>&nbsp;&nbsp;&nbsp;<a href='http://play.google.com/store/apps/details?id=com.esri.android.client'><img src='http://www.android.com/images/brand/android_app_on_play_logo_small.png' alt='Android app on Google Play' /><\/a><br/><br/><a href='http://www.windowsphone.com/en-US/apps/7cb003be-990a-e011-9264-00237de2db9e'><img src='CDN_SERVER/images/Download-en-Small.png' alt='Download for Windows Phone'/>&nbsp;&nbsp;&nbsp;<a href='http://www.amazon.com/gp/product/B007OWF3BI/ref=mas_pm_ArcGIS'><img class='badge esriLeadingMargin2' src='CDN_SERVER/images/amazon.png' alt='Available at Amazon Appstore for Android' /><\/a><\/a><\/div><\/div><\/div>"
            }, {
                "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-6.jpg);display:block;' title='Develop Browser and Mobile Apps'><div class='contentWidth'><h1>Develop Browser and Mobile Apps<\/h1><p>Build mapping applications with powerful APIs that work with your data.<\/p><a target='_blank' class='extralarge button green' href='http://developers.arcgis.com'>Learn More &raquo;<\/a><\/div><\/div><\/div>"
            }
            ],
            "staticImagesUrl": "http://static.arcgis.com/images",
            "stylesGroupQuery": "title:\"Esri Styles\" AND owner:esri_en",
            "supportsHostedServices": True,
            "symbolSetsGroupQuery": "title:\"Esri Symbols\" AND owner:esri_en",
            "templatesGroupQuery": "title:\"Web Application Templates\" AND owner:esri_en",
            "thumbnail": None,
            "urlKey": "ahmednoureldeen",
            "httpPort": 80,
            "httpsPort": 443,
            "ipCntryCode": "EG",
            "supportsOAuth": False
        }
    else:  # Handle normal requests from ArcGIS web app builder and esri templates.
        portal_json = {
            "basemapGalleryGroupQuery": "title:\"ArcGIS Online Basemaps\" AND owner:esri_en",
            "colorSetsGroupQuery": "title:\"Esri Colors\" AND owner:esri_en",
            "customBaseUrl": "localhost",
            "defaultBasemap": {
                "baseMapLayers": [
                    {
                        "url": "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer",
                        "resourceInfo": {
                            "currentVersion": 10.01,
                            "copyrightText": "Sources: Esri, DeLorme, NAVTEQ, TomTom, Intermap, AND, USGS, NRCAN, Kadaster NL, and the GIS User Community",
                            "spatialReference": {
                                "wkid": 102100
                            },
                            "singleFusedMapCache": True,
                            "tileInfo": {
                                "rows": 256,
                                "cols": 256,
                                "dpi": 96,
                                "format": "JPEG",
                                "compressionQuality": 90,
                                "origin": {
                                    "x": -20037508.342787,
                                    "y": 20037508.342787
                                },
                                "spatialReference": {
                                    "wkid": 102100
                                },
                                "lods": [
                                    {
                                        "level": 0,
                                        "resolution": 156543.033928,
                                        "scale": 591657527.591555
                                    },
                                    {
                                        "level": 1,
                                        "resolution": 78271.5169639999,
                                        "scale": 295828763.795777
                                    },
                                    {
                                        "level": 2,
                                        "resolution": 39135.7584820001,
                                        "scale": 147914381.897889
                                    },
                                    {
                                        "level": 3,
                                        "resolution": 19567.8792409999,
                                        "scale": 73957190.948944
                                    },
                                    {
                                        "level": 4,
                                        "resolution": 9783.93962049996,
                                        "scale": 36978595.474472
                                    },
                                    {
                                        "level": 5,
                                        "resolution": 4891.96981024998,
                                        "scale": 18489297.737236
                                    },
                                    {
                                        "level": 6,
                                        "resolution": 2445.98490512499,
                                        "scale": 9244648.868618
                                    },
                                    {
                                        "level": 7,
                                        "resolution": 1222.99245256249,
                                        "scale": 4622324.434309
                                    },
                                    {
                                        "level": 8,
                                        "resolution": 611.49622628138,
                                        "scale": 2311162.217155
                                    },
                                    {
                                        "level": 9,
                                        "resolution": 305.748113140558,
                                        "scale": 1155581.108577
                                    },
                                    {
                                        "level": 10,
                                        "resolution": 152.874056570411,
                                        "scale": 577790.554289
                                    },
                                    {
                                        "level": 11,
                                        "resolution": 76.4370282850732,
                                        "scale": 288895.277144
                                    },
                                    {
                                        "level": 12,
                                        "resolution": 38.2185141425366,
                                        "scale": 144447.638572
                                    },
                                    {
                                        "level": 13,
                                        "resolution": 19.1092570712683,
                                        "scale": 72223.819286
                                    },
                                    {
                                        "level": 14,
                                        "resolution": 9.55462853563415,
                                        "scale": 36111.909643
                                    },
                                    {
                                        "level": 15,
                                        "resolution": 4.77731426794937,
                                        "scale": 18055.954822
                                    },
                                    {
                                        "level": 16,
                                        "resolution": 2.38865713397468,
                                        "scale": 9027.977411
                                    },
                                    {
                                        "level": 17,
                                        "resolution": 1.19432856685505,
                                        "scale": 4513.988705
                                    },
                                    {
                                        "level": 18,
                                        "resolution": 0.597164283559817,
                                        "scale": 2256.994353
                                    },
                                    {
                                        "level": 19,
                                        "resolution": 0.298582141647617,
                                        "scale": 1128.497176
                                    }
                                ]
                            },
                            "fullExtent": {
                                "xmin": -20037507.0671618,
                                "ymin": -19971868.8804086,
                                "xmax": 20037507.0671618,
                                "ymax": 19971868.8804086,
                                "spatialReference": {
                                    "wkid": 102100
                                }
                            },
                            "supportedImageFormatTypes": "PNG24,PNG,JPG,DIB,TIFF,EMF,PS,PDF,GIF,SVG,SVGZ,AI,BMP",
                            "capabilities": "Map,Query,Data"
                        }
                    }
                ],
                "title": "Topographic"
            },
            "defaultExtent": {
                "xmin": -15000000,
                "ymin": 2700000,
                "xmax": -6200000,
                "ymax": 6500000,
                "spatialReference": {
                    "wkid": 102100
                }
            },
            "description": None,
            "featuredGroups": [
                {
                    "owner": "Federal_User_Community",
                    "title": "National Maps for USA"
                },
                {
                    "owner": "esri",
                    "title": "Esri Maps and Data"
                },
                {
                    "owner": "esri",
                    "title": "Community Basemaps"
                },
                {
                    "owner": "esri",
                    "title": "Landsat Community"
                },
                {
                    "owner": "esri_en",
                    "title": "Web Application Templates"
                },
                {
                    "owner": "ArcGISTeamLocalGov",
                    "title": "ArcGIS for Local Government"
                }
            ],
            "featuredItemsGroupQuery": "title:\"Featured Maps and Apps for United States\" AND owner:Esri_cy_US",
            "galleryTemplatesGroupQuery": "title:\"Gallery Templates\" AND owner:esri_en",
            "helpBase": "http://doc.arcgis.com/en/arcgis-online/",
            "helpMap": {
                "v": "1.0",
                "m": {
                    "120000503": "administer/view-status.htm",
                    "120000905": "administer/configure-open-data.htm",
                    "120000897": "administer/configure-roles.htm",
                    "120000468": "create-maps/configure-pop-ups.htm",
                    "120000473": "create-maps/configure-time.htm",
                    "120000470": "create-maps/change-symbols.htm",
                    "120000464": "create-maps/make-your-first-map.htm",
                    "120000467": "create-maps/add-layers.htm#FILE",
                    "120000902": "share-maps/publish-features.htm",
                    "120000900": "share-maps/review-addresses.htm",
                    "120000923": "share-maps/share-maps.htm",
                    "120000455": "share-maps/share-items.htm",
                    "120000454": "share-maps/add-items.htm",
                    "120000456": "share-maps/supported-items.htm",
                    "120000899": "use-maps/take-maps-offline.htm",
                    "120000516": "reference/troubleshoot.htm#WEB_STORAGE",
                    "120000815": "reference/about-cityengine-web-viewer.htm",
                    "120000814": "reference/faq.htm",
                    "120000817": "reference/troubleshoot-cityengine-web-viewer.htm",
                    "120000816": "reference/use-cityengine-web-viewer.htm",
                    "120000461": "reference/videos.htm",
                    "120000463": "reference/show-desktop-content.htm",
                    "120000465": "reference/search.htm",
                    "120000466": "reference/troubleshoot-account.htm",
                    "120000469": "reference/shapefiles.htm",
                    "120000592": "reference/manage-trial.htm",
                    "120000471": "reference/kml.htm",
                    "120000597": "reference/arcgis-server-services.htm",
                    "120000460": "index.html"
                }
            },
            "helperServices": {
                "geocode": [
                    {
                        "url": "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer",
                        "northLat": "Ymax",
                        "southLat": "Ymin",
                        "eastLon": "Xmax",
                        "westLon": "Xmin"
                    }
                ],
                "route": {
                    "url": "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World"
                },
                "geometry": {
                    "url": "https://utility.arcgisonline.com/arcgis/rest/services/Geometry/GeometryServer"
                },
                "printTask": {
                    "url": "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task"
                },
                "closestFacility": {
                    "url": "https://route.arcgis.com/arcgis/rest/services/World/ClosestFacility/NAServer/ClosestFacility_World"
                },
                "asyncClosestFacility": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/ClosestFacility/GPServer/FindClosestFacilities"
                },
                "traffic": {
                    "url": "https://traffic.arcgis.com/arcgis/rest/services/World/Traffic/MapServer"
                },
                "serviceArea": {
                    "url": "https://route.arcgis.com/arcgis/rest/services/World/ServiceAreas/NAServer/ServiceArea_World"
                },
                "asyncServiceArea": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/ServiceAreas/GPServer/GenerateServiceAreas"
                },
                "syncVRP": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/VehicleRoutingProblemSync/GPServer/EditVehicleRoutingProblem"
                },
                "asyncVRP": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/VehicleRoutingProblem/GPServer/SolveVehicleRoutingProblem"
                },
                "asyncLocationAllocation": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/LocationAllocation/GPServer"
                },
                "elevation": {
                    "url": "https://elevation.arcgis.com/arcgis/rest/services/Tools/Elevation/GPServer"
                },
                "hydrology": {
                    "url": "https://hydro.arcgis.com/arcgis/rest/services/Tools/Hydrology/GPServer"
                },
                "elevationSync": {
                    "url": "https://elevation.arcgis.com/arcgis/rest/services/Tools/ElevationSync/GPServer"
                },
                "asyncRoute": {
                    "url": "https://logistics.arcgis.com/arcgis/rest/services/World/Route/GPServer"
                },
                "geoenrichment": {
                    "url": "https://geoenrich.arcgis.com/arcgis/rest/services/World/GeoenrichmentServer"
                }
            },
            "homePageFeaturedContent": "title:\"Featured Maps\" AND owner:Esri_cy_US",
            "homePageFeaturedContentCount": 12,
            "httpPort": 3000,
            "httpsPort": 555,
            "ipCntryCode": "US",
            "isPortal": True,
            "layerTemplatesGroupQuery": "title:\"Esri Layer Templates\" AND owner:esri_en",
            "name": None,
            "portalHostname": "localhost:555",
            "portalMode": "multitenant",
            "portalName": "ArcGIS Online",
            "portalThumbnail": None,
            "rotatorPanels": [
                {
                    "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-1.jpg);display:block;' title='Create and Collaborate on Maps and Apps'><div class='contentWidth'><h1>Create and Collaborate on Maps and Apps</h1><p>ArcGIS Online is a cloud-based, collaborative content management system for maps, apps, data, and other geographic information.</p><a target='_blank' class='extralarge button green' href='/about/'>Learn More &raquo;</a></div></div></div>"
                },
                {
                    "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-2.jpg);display:block;' title='Your Maps, Your Way'><div class='contentWidth'><h1>Your Maps, Your Way</h1><p>Create, store, and manage your own maps, apps, and data with a personal ArcGIS Online account.</p><a target='_blank' class='extralarge button blue' href='/about/features.html'>Learn More &raquo;</a></div></div></div>"
                },
                {
                    "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-3.jpg);display:block;' title='The Geospatial Platform for Your Organization'> <div class='contentWidth'> <h1>The Geospatial Platform for Your Organization</h1><p>Host your organization's geographic information in Esri's cloud with an ArcGIS Online subscription.</p><a target='_blank' class='extralarge button green' href='/about/features.html#your-data-in-the-cloud'>Learn More &raquo;</a></div></div></div>"
                },
                {
                    "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-4.jpg);display:block;' title='Intelligent Web Maps'><div class='contentWidth'><h1>Intelligent Web Maps</h1><p>Turn your data into information by creating content-rich, beautiful maps that tell your story.</p><a class='extralarge button yellow' href='webmap/viewer.html?useExisting=1'>Get Started &raquo;</a></div></div></div>"
                },
                {
                    "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-5.jpg);display:block;' title='Any Map, Anywhere'><div class='contentWidth'><h1>Any Map, Anywhere</h1><p>Whether in the board room, at your desk, or in in the field, access the same map on all your devices.</p><a href='http://itunes.apple.com/us/app/arcgis/id379687930'><img src='CDN_SERVER/images/App_Store_Badge_en.png' alt='Download on the App Store'/></a>&nbsp;&nbsp;&nbsp;<a href='http://play.google.com/store/apps/details?id=com.esri.android.client'><img src='http://www.android.com/images/brand/android_app_on_play_logo_small.png' alt='Android app on Google Play' /></a><br/><br/><a href='http://www.windowsphone.com/en-US/apps/7cb003be-990a-e011-9264-00237de2db9e'><img src='CDN_SERVER/images/Download-en-Small.png' alt='Download for Windows Phone'/>&nbsp;&nbsp;&nbsp;<a href='http://www.amazon.com/gp/product/B007OWF3BI/ref=mas_pm_ArcGIS'><img class='badge esriLeadingMargin2' src='CDN_SERVER/images/amazon.png' alt='Available at Amazon Appstore for Android' /></a></a></div></div></div>"
                },
                {
                    "innerHTML": "<div><div class='item whiteTxt' style='background-image:url(CDN_SERVER/images/slide-6.jpg);display:block;' title='Develop Browser and Mobile Apps'><div class='contentWidth'><h1>Develop Browser and Mobile Apps</h1><p>Build mapping applications with powerful APIs that work with your data.</p><a target='_blank' class='extralarge button green' href='http://developers.arcgis.com'>Learn More &raquo;</a></div></div></div>"
                }
            ],
            "staticImagesUrl": "https://localhost:555/images",
            "stylesGroupQuery": "title:\"Esri Styles\" AND owner:esri_en",
            "supportsHostedServices": True,
            "supportsOAuth": True,
            "symbolSetsGroupQuery": "title:\"Esri Symbols\" AND owner:esri_en",
            "templatesGroupQuery": "title:\"Web Application Templates\" AND owner:esri_en",
            "thumbnail": None,
            "supportsOAuth": False,
        }
    if request.GET.get('callback'):
        return JsonPResponse(portal_json, callback=request.GET.get('callback'))
    else:
        return JsonResponse(portal_json, content_type="application/json")
