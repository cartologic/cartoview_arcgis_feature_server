__author__ = 'kamal'

from .utils import DynamicObject
import json
from django.contrib.gis.db import models
from django.db.models import Q
from django.contrib.gis.geos import Polygon, Point, MultiPoint, LineString

DEFAULT_GEOMETRY_TYPE = 'esriGeometryEnvelope'
SPATIAL_RELATION_MAPPING = dict(
    esriSpatialRelIntersects="__intersects",
    # hack now to be supported
    esriSpatialRelContains="__intersects"
)
DEFAULT_SPATIAL_REL = 'esriSpatialRelIntersects'


class GeoDjangoGeometrySerializer(object):
    @staticmethod
    def simplify(layer, geom, qs, query_geom):

        if query_geom is not None:
            bbox = query_geom.extent
        else:
            bbox = qs.extent()

        tolerance = min(abs(bbox[0]-bbox[2]), abs(bbox[1]-bbox[3])) * layer.tolerance_factor
        return geom.simplify(tolerance, True)

    @staticmethod
    def esriGeometryPoint(geometry, layer, qs, query_geom):
        return {
            'x': geometry.coords[0],
            'y': geometry.coords[1],
        }

    @staticmethod
    def esriGeometryPolyline(geometry, layer, qs, query_geom):
        if layer.enable_geometry_simplify:
            geometry = GeoDjangoGeometrySerializer.simplify(layer, geometry, qs, query_geom)
        paths = [geometry.coords] if geometry.geom_type == 'LineString' else geometry.coords
        return {'paths': paths}

    @staticmethod
    def esriGeometryPolygon(geometry, layer, qs, query_geom):
        try:
            if layer.enable_geometry_simplify:
                geometry = GeoDjangoGeometrySerializer.simplify(layer, geometry, qs, query_geom)
            rings = geometry.coords[0] if geometry.geom_type == 'MultiPolygon' else geometry.coords
            return {'rings': rings}
        except:
            return None

    @staticmethod
    def esriGeometryMultipoint(geometry, layer, qs, query_geom):
        if layer.enable_geometry_simplify:
            geometry = GeoDjangoGeometrySerializer.simplify(layer, geometry, qs, query_geom)
        return {'points': geometry.coords}




class GeoDjangoQuery:

    @staticmethod
    def query(layer, query_obj):
        qs = layer.initial_queryset
        # check for objectIds query
        if query_obj.objectids:
            ids = query_obj.objectids.split(",")
            filters = dict()
            filters[layer.id_field_name + "__in"] = ids
            qs = qs.filter(**filters)
        #
        if query_obj.where and query_obj.where != '':
            # escape % because querySet.extra expected
            # the "where" argument as a formatting string and replace params in it
            where = query_obj.where.replace("%", "%%")
            qs = qs.extra(where=[where])
        # add spatial query to filters
        query_obj.geom = GeoDjangoQuery._get_query_geometry(query_obj)
        qs = GeoDjangoQuery._build_spatial_query(layer, query_obj, qs)


        if query_obj.returncountonly:
            result = GeoDjangoQuery._get_count(qs)
        elif query_obj.returnidsonly == True:
            result = GeoDjangoQuery._get_ids(layer,qs)
        else:
            qs = qs[0:layer.max_records]
            outSR = int(query_obj.outsr or layer.srid)
            if outSR != layer.srid and query_obj.returngeometry:
                qs = qs.transform(outSR if outSR != 102100 else 900913)
            outFields = query_obj.outfields or layer.id_field_name or layer.display_field_name
            if outFields == "*":
                outFields = layer.fields_names
            else:
                outFields = outFields.split(",")
            result = GeoDjangoQuery._get_list(layer, qs, query_obj.geom, outFields, query_obj.returngeometry, outSR)
        return result

    @staticmethod
    def _build_spatial_query(layer, query_obj, qs):
        """
        apply spatial query if the query parameters includes geometry parameter
        @param query_obj: the request parameters sent from the client
        @param qs: a django query set to apply the spatial query on it
        @return: a django query set after applying the spatial query if found in the request
        """
        if query_obj.geom:
            query_obj.spatialrel = query_obj.spatialrel or DEFAULT_SPATIAL_REL
            filter_kwargs = {}
            key = layer.geometry_field_name + SPATIAL_RELATION_MAPPING[query_obj.spatialrel]
            filter_kwargs[key] = query_obj.geom
            qs = qs.filter(**filter_kwargs)
        return qs

    # TODO move this method to query parser
    @staticmethod
    def _get_query_geometry(query_obj):
        if query_obj.geometry == None or query_obj.geometry == '':
            return None

        geom = None
        query_obj.geometrytype = query_obj.geometrytype or DEFAULT_GEOMETRY_TYPE
        if query_obj.geometrytype == 'esriGeometryPoint':
            try:
                xy = map(float, query_obj.geometry.split(","))
            except:
                xy = DynamicObject(json.loads(query_obj.geometry))
                xy = [xy.x, xy.y]
            geom = Point(*xy)
        elif query_obj.geometrytype == 'esriGeometryPolygon':
            poly = DynamicObject(json.loads(query_obj.geometry))
            geom = Polygon(*poly.rings)
        elif query_obj.geometrytype == 'esriGeometryPolyline':
            line = DynamicObject(json.loads(query_obj.geometry))
            geom = LineString(*line.paths)
        elif query_obj.geometrytype == 'esriGeometryEnvelope':
            try:
                bbox = map(float, query_obj.geometry.split(","))
            except:
                bbox = DynamicObject(json.loads(query_obj.geometry))
                bbox = [bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax]
            geom = Polygon.from_bbox(bbox)

        # set the projection on the geometry
        if geom and query_obj.insr:
            geom.srid = int(query_obj.insr)
            if geom.srid == 102100:
                geom.srid = 900913
        return geom


    @staticmethod
    def _get_count(query_set):
        return DynamicObject(dict(count=query_set.count()))

    @staticmethod
    def _get_ids(layer, query_set):
        ids = []
        for item in query_set:
            ids.append(getattr(item, layer.id_field_name))
        result_data = DynamicObject(dict(
            objectIdFieldName=layer.id_field_name
        ))
        result_data.objectIds = ids
        return result_data

    @staticmethod
    def _get_list(layer, query_set, query_geom, out_fields, returnGeometry, outSR):
        """
        serialize the django query set into arcGIS JSON format.
        @param layer: FeatureLayer
        @param query_set: the final query set that will be included in the result
        @param out_fields: a list of fields names that will be included in the result
        @param returnGeometry: true to add geometry to result
        @param outSR: just to include in the result
        @return: DynamicObject
        """
        features = []
        for item in query_set:
            feature = {}
            if returnGeometry:
                geometry = None
                geom = getattr(item, layer.geometry_field_name)
                if geom:
                    geometry_fn = getattr(GeoDjangoGeometrySerializer, layer.geometry_type)
                    geometry = geometry_fn(geom, layer, query_set, query_geom)
                feature['geometry'] = geometry
            attributes = {}
            for p in out_fields: #GeoDjangoQuery.fields_names:
                attributes[p] = getattr(item, p)
            feature['attributes'] = attributes
            features.append(feature)
        result_data = dict(displayFieldName=layer.display_field_name)
        if len(features) > 0:
            fields_defs = []
            aliases = {}
            for f in layer.fields_defs:
                if f['name'] in out_fields:
                    fields_defs.append(f)
                    aliases[f['name']] = f['alias']
            result_data.update(dict(
                fields=fields_defs,
                fieldAliases=aliases,
                objectIdFieldName=layer.id_field_name
            ))
            if returnGeometry:
                result_data.update(dict(
                    geometryType=layer.geometry_type,
                    spatialReference=dict(wkid=outSR, latestWkid=outSR),
                ))
        result_data = DynamicObject(result_data)
        result_data.features = features
        return result_data
