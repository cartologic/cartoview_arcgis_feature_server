from django.db import models
from geonode.layers.models import Layer
from geonode.maps.models import Map as GeonodeMap
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from cartoserver.models import update_geo_table, Connector
from cartoserver.models import FeatureLayer
from cartoserver.constants import DRAWING_INFO_DEFAULTS
from django.template.defaultfilters import slugify

DYNAMIC_DATASTORE = 'datastore'


# class LayerMapping(models.Model):
#     geonode_layer = models.ForeignKey(Layer, related_name='featurelayer_%(class)s')
#     cartoserver_featurelayer = models.ForeignKey(FeatureLayer, related_name='geonode_%(class)s')
#
#
# def update_featre_layer(geonode_layer, featurelayer):
#     content_type = Connector.geo_content_types[DYNAMIC_DATASTORE][geonode_layer.name]
#     featurelayer.name = geonode_layer.title
#
#     # service name
#     counter = 0
#     name = slugify(geonode_layer.title)
#     service_name = name
#     qs = FeatureLayer.objects
#     if featurelayer.pk:
#         qs = qs.exclude(pk=featurelayer.pk)
#     while 1:
#         if qs.filter(service_name=service_name).count() > 0:
#             counter += 1
#             service_name = "%s-%d" % (name, counter)
#         else:
#             break
#     featurelayer.service_name = service_name
#     featurelayer.content_type = content_type
#     featurelayer.description = geonode_layer.abstract
#     if featurelayer.drawing_info == '' or featurelayer.drawing_info is None:
#         featurelayer.drawing_info = DRAWING_INFO_DEFAULTS[featurelayer.geometry_type]
#     featurelayer.save()
#
#
# def map_layer(layer):
#     try:
#         layer_mapping = LayerMapping.objects.get(geonode_layer=layer)
#         update_featre_layer(layer, layer_mapping.cartoserver_featurelayer)
#     except LayerMapping.DoesNotExist:
#         featurelayer = FeatureLayer()
#         update_featre_layer(layer, featurelayer)
#         layer_mapping = LayerMapping(geonode_layer=layer, cartoserver_featurelayer=featurelayer)
#         layer_mapping.save()
#
#
# @receiver(post_save, sender=Layer)
# def post_save_layer(sender, instance, created, *args, **kwargs):
#     # add try block to neglect layers that has the following
#     # 1. the layer uses database view not table TODO: handle this issue
#     try:
#         if created:
#             update_geo_table()
#         map_layer(instance)
#     except:
#         print "cannot map layer %s" % instance.title
#
#
# @receiver(post_delete, sender=LayerMapping)
# def post_delete_layermapping(sender, instance, *args, **kwargs):
#     instance.cartoserver_featurelayer.delete()
#
#
# def map_all_layers():
#     mapped_layers_ids = LayerMapping.objects.all().values_list('geonode_layer_id')
#     not_published = Layer.objects.exclude(pk__in=mapped_layers_ids)
#     update_geo_table()
#     print not_published
#     for layer in not_published:
#         try:
#             map_layer(layer)
#         except:
#             pass
