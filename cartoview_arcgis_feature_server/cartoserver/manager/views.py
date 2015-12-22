from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from ..models import FeatureLayer, GeoTable
from ..utils import get_context, DynamicObject
from ..constants import *
from ..views import response_to_json
from ..postgis import file2pgtable, get_model_field_name
from ..models import Datastore, Connector


@login_required
def home(request):
    # GeoTable.objects.all().delete()
    context = get_context({
        "items": GeoTable.objects.all()
    })
    return render(request, MANAGER_HOME_TPL, context)


@login_required
def add_geotable(request):
    # GeoTable.objects.all().delete()
    context = get_context({
        "items": GeoTable.objects.all()
    })
    return render(request, MANAGER_GEOTABLES_ADD_TPL, context)


def angular_template(request, template):
    context = get_context({})
    return render(request, ANGULAR_TEMPLATE_BASE + template, context)


from django.conf import settings
import os
import datetime
import zipfile

SHP_UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, 'ShapeFiles')


def write_file(file_path, file_data):
    destination = open(file_path, 'wb+')
    for chunk in file_data.chunks():
        destination.write(chunk)
    destination.close()


class ShapefileNotFoundException(Exception):
    pass


def extract_file(folder_name, file_path):
    shapefile = None
    zfile = zipfile.ZipFile(file_path)
    for info in zfile.infolist():
        if info.filename.startswith('__MACOSX/'):
            continue
        if info.filename.endswith('/'):
            continue
            # try: # Don't try to create a directory if exists
            #     os.mkdir(os.path.join(folder_name, info.filename))
            # except:
            #     pass
        if info.filename.endswith('shp'):
            shapefile = info.filename
        data = zfile.read(info.filename)
        shp_part = '%s%s%s' % (folder_name, os.path.sep, info.filename)
        fout = open(shp_part, "wb")
        fout.write(data)
        fout.close()
    if shapefile is None:
        raise ShapefileNotFoundException()
    return '%s%s%s' % (folder_name, os.path.sep, shapefile)


from django.db import connections, DEFAULT_DB_ALIAS


## get srid from proj4 (using spatial_ref_sys table in database)
def get_srid(proj4):
    SpatialRefSys = connections[DEFAULT_DB_ALIAS].ops.spatial_ref_sys()
    return SpatialRefSys.objects.get(proj4text=proj4).srid


def get_shapefile_info(shapefile_path):
    from django.contrib.gis import gdal
    ds = gdal.DataSource(shapefile_path)
    layer = ds[0]
    fields = []
    for i in range(0, len(layer.fields)):
        fields.append(dict(
            name=layer.fields[i],
            type=layer.field_types[i].__name__,
            width=layer.field_widths[i],
            precision=layer.field_precisions[i]
        ))
    srid = None
    if layer.srs is not None:
        if layer.srs.srid is None:
            try:
                srid = get_srid(layer.srs.proj4)
            except:
                pass
        else:
            srid = layer.srs.srid

    return DynamicObject(dict(
        name=layer.name,
        # num_features=layer.num_feat,
        type=layer.geom_type.name,
        # fields=fields,
        # extent=layer.extent.tuple,
        srid=srid
    ))


@csrf_exempt
def upload(request):
    if not os.path.exists(SHP_UPLOAD_DIR):
        os.makedirs(SHP_UPLOAD_DIR)
    file_data = request.FILES['shapefile']
    # contruct the full filepath and filename
    folder_name = os.path.normpath(os.path.join(SHP_UPLOAD_DIR, os.path.splitext(file_data.name)[0]))
    if os.path.exists(folder_name):
        append = datetime.datetime.now().strftime('%Y-%m-%dT%H_%M_%S')
        folder_name = '%s_%s' % (folder_name, append)
        os.makedirs(folder_name)
    else:
        os.makedirs(folder_name)

    file_path = os.path.normpath(os.path.join(folder_name, file_data.name))
    write_file(file_path, file_data)
    json_response = DynamicObject()
    try:
        shapefile_path = extract_file(folder_name, file_path)
        json_response.success = True

    except ShapefileNotFoundException:
        json_response.success = False
        json_response.error_msg = "The uploaded zip file doesn't include any shapefile!"
    except:
        json_response.success = False
        json_response.error_msg = "Unable to extract the zip file!"

    if json_response.success:
        json_response.shapefileInfo = get_shapefile_info(shapefile_path)
        json_response.shapefileInfo.path = shapefile_path.split(SHP_UPLOAD_DIR + os.path.sep)[1]

    context = get_context(dict(
        json=json_response
    ))
    return response_to_json(request, context)


from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Polygon, LineString, Point, MultiLineString, MultiPolygon


def get_point(geom):
    return Point(geom.x, geom.y)


def get_multipoint(geom):
    rings = []
    for ring in geom.tuple:
        # ensure that the ring is closed
        rings.append(ring + (ring[0],))
    return Polygon(*rings)


def get_line(geom):
    return LineString(geom.coords)


# TODO test MultiLine
def get_multiline(geom):
    if geom.geom_type.name == "Linestring":
        return MultiLineString(get_line(geom))
    lines = []
    for line in geom.tuple:
        lines.append(LineString(line))
    return MultiLineString(*lines)


def get_polygon(geom):
    rings = []
    for ring in geom.tuple:
        # ensure that the ring is closed
        rings.append(ring + (ring[0],))
    return Polygon(*rings)


def get_multipolygon(geom):
    if geom.geom_type.name == "Polygon":
        return MultiPolygon(get_polygon(geom))
    polys = []
    for poly in geom.tuple:
        rings = []
        for ring in poly:
            # ensure that the ring is closed
            rings.append(ring + (ring[0],))
        polys.append(Polygon(*rings))
    return MultiPolygon(*polys)


get_geom_methods = dict(
    POINT=get_point,
    MULTIPOINT=get_multipoint,
    LINESTRING=get_line,
    MULTILINESTRING=get_multiline,
    POLYGON=get_polygon,
    MULTIPOLYGON=get_multipolygon
)


def add_data(shapefile_path, geotable):
    datasource = DataSource(shapefile_path)
    layer = datasource[0]
    added_features = 0
    for feature in layer:
        try:
            data = {}
            geom = get_geom_methods[geotable.geometry_type](feature.geom)
            data[geotable.geometry_field_name] = geom
            for field in feature:
                field_name = get_model_field_name(field.name)
                data[field_name] = feature.get(field.name)
            geotable.datasource(**data).save()
            added_features += 1
        except:
            print added_features
    return layer.num_feat, added_features


def get_table_name(path, db):
    table_name = os.path.basename(path).split(".")[0]
    table_name = get_model_field_name(table_name)
    counter = 0
    name = table_name
    cursor = connections[db].cursor()
    table_names = connections[db].introspection.get_table_list(cursor)
    while name in table_names:
        counter += 1
        name = "%s_%d" % (table_name, counter)
    return name


@csrf_exempt
def save_new(request):
    json_response = DynamicObject()
    json_response.success = False
    # try:

    shapefile_path = os.path.join(SHP_UPLOAD_DIR, request.POST.get('path'))
    if os.path.isfile(shapefile_path):
        srid = int(request.POST.get('srid'))
        is_public = bool(request.POST.get('is_public'))
        # name = request.POST.get('name')
        datastore = None
        connection_name = DEFAULT_DB_ALIAS
        try:
            datastore = Datastore.objects.get(is_default=True)
            connection_name = datastore.get_connection_name()
        except:
            pass

        name = get_table_name(shapefile_path, connection_name)
        title = request.POST.get('title')
        description = request.POST.get('description')
        mapping = file2pgtable(shapefile_path, name, connection_name, srid)
        content_type = Connector(connection_name).create_models(name)
        geotable = GeoTable.objects.get(content_type=content_type)
        geotable.title = title
        geotable.description = description
        geotable.is_public = is_public
        geotable.owner = request.user
        geotable.datastore = datastore
        geotable.save()
        json_response.num_feat, json_response.added_features = add_data(shapefile_path, geotable)
        try:
            import shutil
            shutil.rmtree(os.path.dirname(shapefile_path))
        except:
            pass
        json_response.success = True
    else:
        json_response.error_msg = "Invalid shapefile path!"
    # except:
    #     json_response.msg = 'Cannot load table data'

    if json_response.success:
        return HttpResponseRedirect(
            "%srest/v1/geotable/%d/?format-json" % (reverse(MANAGER_HOME_URL_NAME), geotable.pk))
    else:
        context = get_context(dict(
            json=json_response
        ))
        return response_to_json(request, context)


@csrf_exempt
def publish(request):
    json_response = DynamicObject()
    json_response.success = False
    # try:

    geo_table_id = request.POST.get('geo_table')
    geotable = GeoTable.objects.get(pk=geo_table_id)

    counter = 0
    name = geotable.title
    while 1:
        try:
            FeatureLayer.objects.get(name=name)
            counter += 1
            name = "%s %d" % (geotable.title, counter)
        except:
            break

    layer = FeatureLayer(content_type=geotable.content_type, name=name, description=geotable.description,
                         add_to_catalog=True)
    # layer.save()
    layer.publish(request)
    json_response.success = True
    # except:
    #     json_response.msg = 'Cannot load table data'

    if json_response.success:
        return HttpResponseRedirect(
            "%s%s/featurelayer/%d/?format-json" % (reverse("cartoview2_rest_url"), APP_NAME, layer.pk))
    else:
        context = get_context(dict(
            json=json_response
        ))
        return response_to_json(request, context)
