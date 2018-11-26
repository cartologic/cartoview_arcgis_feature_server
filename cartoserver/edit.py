__author__ = 'kamal'

from .utils import DynamicObject
import json
from django.contrib.gis.db import models
from django.db.models import Q
from django.contrib.gis.geos import Polygon, Point, MultiPoint, LineString
from .query import GeoDjangoQuery

class GeoDjangoEdit:
    @staticmethod
    def apply_edits(layer, post_data):
        result = {}
        adds = post_data.get('adds', None)
        if adds:
            result['addResults'] = GeoDjangoEdit.add(layer, json.loads(adds))

        updates = post_data.get('updates', None)
        if updates:
            result['updateResults'] = GeoDjangoEdit.edit(layer,json.loads(updates))

        deletes = post_data.get('deletes', None)
        if deletes:
            try:
                deletes = deletes.split(',')
            except:
                deletes = [deletes]
            result['deleteResults'] = GeoDjangoEdit.delete(layer, deletes)

        return DynamicObject(result)

    @staticmethod
    def add_features(layer, post_data):
        result = {}
        adds = post_data.get('features', None)
        result['addResults'] = GeoDjangoEdit.add(layer,json.loads(adds))
        return DynamicObject(result)

    @staticmethod
    def update_features(layer, post_data):
        result = {}
        updates = post_data.get('features', None)
        result['updateResults'] = GeoDjangoEdit.edit(layer,json.loads(updates))
        return DynamicObject(result)

    @staticmethod
    def delete_features(layer, post_data):
        result = {}
        deletes = post_data.get('objectIds', None)
        if deletes:
            try:
                deletes = deletes.split(',')
            except:
                deletes = [deletes]
            result['deleteResults'] = GeoDjangoEdit.delete(layer, deletes)
        return DynamicObject(result)

    @staticmethod
    def add(layer, adds):
        result = []
        for feature_data in adds:
            geom = GeoDjangoEdit._get_geometry(layer.geometry_type, DynamicObject(feature_data))
            if geom:
                feature_data['attributes'][layer.geometry_field_name]= geom
            feature = layer.datasource.objects.create(**feature_data['attributes'])
            feature.save()
            result.append(dict(
                objectId=feature.pk,
                # globalId=None,
                success=True
            ))
        return result


    @staticmethod
    def edit(layer, updates):
        result = []
        for feature_data in updates:
            objectId = feature_data['attributes'][layer.id_field_name]
            feature = layer.datasource.objects.get(pk=objectId)
            for key, value in feature_data['attributes'].items():
                setattr(feature, key, value)
            geom = GeoDjangoEdit._get_geometry(layer.geometry_type, DynamicObject(feature_data))
            if geom:
                setattr(feature,layer.geometry_field_name, geom)
            feature.save()
            result.append(dict(
                objectId=objectId,
                # globalId=None,
                success=True
            ))
        return result

    @staticmethod
    def delete(layer, deletes):
        filters = dict()
        filters[layer.id_field_name + "__in"] = deletes
        qs = layer.datasource.objects.filter(**filters)
        qs.delete()
        return [{'objectId': object_id, 'success': True} for object_id in deletes]


    @staticmethod
    def _get_geometry(geom_type, feature):
        print geom_type
        geom_obj = feature.geometry
        if geom_obj is None:
            return None

        geom = None
        if geom_type == 'esriGeometryPoint':
            geom = Point(geom_obj.x, geom_obj.y)
        elif geom_type == "esriGeometryPolyline":
            geom = LineString(geom_obj.paths[0])
        elif geom_type == "esriGeometryPolygon":
            geom = Polygon(geom_obj.rings[0])
        # TODO:Support these types
        # elif geom_type == "esriGeometryMultipoint":
        # elif geom_type == "esriGeometryPolyline":
        # elif geom_type == "esriGeometryPolygon":

        # set the projection on the geometry
        if geom and geom_obj.spatialReference and geom_obj.spatialReference.wkid:
            geom.srid = int(geom_obj.spatialReference.wkid)
            if geom.srid == 102100:
                geom.srid = 900913
        return geom


