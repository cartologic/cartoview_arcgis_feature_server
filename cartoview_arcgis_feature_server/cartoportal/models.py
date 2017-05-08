from django.db import models
from geonode.layers.models import Layer
from geonode.maps.models import Map as GeonodeMap
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from arcportal.models import Item, ItemData
import json
from django.contrib.gis.geos.polygon import Polygon
from . import *
from django.template.defaultfilters import slugify
from django.conf import settings
from geonode.maps.models import MapLayer
from cartoview_arcgis_feature_server.cartoserver.models import FeatureLayer


class Map(models.Model):
    geonode_map = models.ForeignKey(GeonodeMap, related_name='portal_%(class)s')
    portal_item = models.ForeignKey(Item, null=True)
    edited = models.BooleanField(default=False)

    def publish(self):
        if self.portal_item:
            item_obj = self.portal_item
            item_data_obj = ItemData.objects.get(item=item_obj)
        else:
            item_obj = Item()
            item_data_obj = ItemData()

        # save portal item
        item_obj.owner = self.geonode_map.owner
        item_obj.name = self.geonode_map.title.replace(" ", "_")
        item_obj.title = self.geonode_map.title
        item_obj.url = None
        item_obj.type = "Web Map"
        item_obj.type_keywords = ",".join(["ArcGIS Online", "Explorer Web Map", "Map", "Online Map", "Web Map"])
        item_obj.description = self.geonode_map.title
        item_obj.tags = ",".join(['map', ])  # todo: get tags from geonode
        item_obj.snippet = 'snippet'  # todo
        item_obj.thumbnail = self.geonode_map.thumbnail_url
        m = self.geonode_map
        bbox = [m.bbox_x0, m.bbox_y0, m.bbox_x1, m.bbox_y1]
        item_obj.extent = Polygon.from_bbox(bbox)
        item_obj.save()
        # save item data
        item_data_json = json.loads(render_to_string(ITEM_DATA_JSON_TPL, {}))
        op_layers = []
        site_url = settings.SITEURL
        if site_url.endswith("/"):
            site_url = site_url[:-1]
        wms_url = settings.OGC_SERVER["default"]["PUBLIC_LOCATION"]
        if wms_url.endswith("/"):
            wms_url += "wms"
        else:
            wms_url += "/wms"
        wms_layers = []
        #                [{
        #     "name": layergroup_name,
        #     "title": layergroup_name
        #
        # }]

        for layer_obj in self.geonode_map.layer_set.all().exclude(group="background"):
            featurelayer = FeatureLayer.objects.get(geonode_layer__typename=layer_obj.name)
            fields = []
            for f in featurelayer.fields_defs:
                fields.append({
                    "fieldName": f["name"],
                    "label": f["alias"],
                    "isEditable": f["editable"],
                    "tooltip": "",
                    "visible": True,
                    "format": None,
                    "stringFieldOption": "textbox"  # TODO chanege according to field type
                })
            layer_params_obj = json.loads(layer_obj.layer_params)
            title = layer_params_obj.get("title", layer_obj.layer_title)
            op_layers.append({
                "id": "layer_%d" % layer_obj.id,
                "layerType": "ArcGISFeatureLayer",
                "url": site_url + featurelayer.meta_page_url,
                "visibility": True,
                "opacity": 0,
                "mode": 1,
                "title": title,
                "popupInfo": {
                    "title": title,
                    "fieldInfos": fields,
                    "description": None,
                    "showAttachments": True,
                    "mediaInfos": []
                }
            })
            wms_layers.append({
                "name": layer_obj.name,
                "title": title

            })

        op_layers.insert(0, {
            "id": "wms",
            "title": "WMS",
            "url": wms_url,
            "visibility": True,
            "visibleLayers": [layer['name'] for layer in wms_layers],
            "opacity": 1,
            "type": "WMS",
            "layerType": "WMS",
            "version": "1.1.1",
            "mapUrl": wms_url,
            "layers": wms_layers,
            "spatialReferences": [3857, 2154, 23030, 23031, 23032, 27561, 27562, 27563, 27564, 27571, 27572, 27573,
                                  27574, 3035, 3942, 3948, 4171, 4258, 4326, 900913],
            "extent": [
                [float(self.geonode_map.bbox_x0), float(self.geonode_map.bbox_y0)],
                [float(self.geonode_map.bbox_x1), float(self.geonode_map.bbox_y1)]
            ],
            "copyright": ""
        })
        item_data_json["operationalLayers"] = op_layers
        item_data_obj.item = item_obj
        item_data_obj.text = json.dumps(item_data_json)
        item_data_obj.save()
        # save map
        self.portal_item = item_obj
        self.edited = False
        self.save()


@receiver(post_delete, sender=GeonodeMap)
def post_delete_geonode_map(sender, instance, *args, **kwargs):
    try:
        instance.portal_map.all().delete()
    except:
        pass

@receiver(post_delete, sender=Map)
def post_delete_map(sender, instance, *args, **kwargs):
    try:
        instance.portal_item.delete()
    except:
        pass


def map_map(geonode_map, created=True):

    m, m_created = Map.objects.get_or_create(geonode_map=geonode_map)
    m.save()
    if not created and not m.edited:
        m.publish()


@receiver(post_save, sender=GeonodeMap)
def post_save_map(sender, instance, created, *args, **kwargs):
    map_map(instance, created)

def map_all():
    maps = GeonodeMap.objects.all()
    for m in maps:
        map_map(m, False)
