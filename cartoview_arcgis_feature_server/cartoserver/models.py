from django.contrib.gis.db import models
from django.contrib.contenttypes.models import ContentType
from .utils import DynamicObject
from django.utils.text import capfirst
from django.utils import six
from .constants import *
import json
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
import os
import sys
from django.utils.datastructures import SortedDict
from django.contrib.gis.db import models
from django.db import connections, DEFAULT_DB_ALIAS, transaction
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
# add libs folder to path
from django.utils.safestring import mark_safe
from .fields import ColorField
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage

class DatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Datastore(DatedModel):
    engine = 'django.contrib.gis.db.backends.postgis'
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100, default='', blank=True)
    password = models.CharField(max_length=100, default='', blank=True)
    host = models.CharField(max_length=100, default='loacalhost')
    port = models.IntegerField()
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = (('name', 'user', 'host', 'port'),)

    @property
    def connection_config(self):
        return dict(
            ENGINE=self.engine,
            NAME=self.name,
            USER=self.user,
            PASSWORD=self.password,
            HOST=self.host,
            PORT=self.port,
            IS_DEFAULT=self.is_default
        )

    def get_connection_name(self):
        return str('dynamic_%d' % self.pk)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_default:
            try:
                temp = Datastore.objects.get(is_default=True)
                if self != temp:
                    temp.is_default = False
                    temp.save()
            except Datastore.DoesNotExist:
                pass
        if Datastore.objects.count() == 0:
            self.is_default = True
        super(Datastore, self).save(force_insert, force_update, using, update_fields)
        update_geo_table()

    @staticmethod
    def get_by_connection_name(connection_name):
        try:
            pk = int(connection_name.split("_")[1])
            return Datastore.objects.get(pk=pk)
        except:
            return None

    @staticmethod
    def update_database_connections():
        for item in Datastore.objects.all():
            alias = item.get_connection_name()
            if not alias in connections.databases:
                connections.databases[alias] = item.connection_config


class GeoTable(DatedModel):
    table_name = models.CharField(null=True, blank=True, max_length=100)
    title = models.CharField(null=True, blank=True, max_length=100)
    description = models.TextField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s', )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s', null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="Check to make the data available for other users")
    datastore = models.ForeignKey(Datastore, related_name='%(app_label)s_%(class)s', null=True)

    def __init__(self, *args, **kwargs):
        self._srid = None
        self._geometry_type = None
        self._geometry_field_name = None
        self._fields_defs = []

        super(GeoTable, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def delete(self, using=None):
        table_name = self.table_name
        content_type = self.content_type
        super(GeoTable, self).delete(using=using)
        content_type.delete()
        sql = "DROP TABLE %s;" % table_name
        from .postgis import execute
        execute(sql, 'cartoserver')

    def _init_table_properties(self):
        for f in self.datasource._meta.fields:
            if issubclass(f.__class__, models.GeometryField):
                self._srid = f.srid
                self._geometry_type = f.geom_type
                self._geometry_field_name = f.attname
            else:
                alias = six.text_type(capfirst(f.verbose_name))
                field_def = dict(
                    name=f.attname,
                    alias=alias,
                    # editable=f.editable if f.attname != self.id_field_name else False,
                    nullable=f.null,
                    type=get_esri_type(f),
                    length=getattr(f, 'max_length', None)
                )
                self._fields_defs.append(field_def)

    @property
    def datasource(self):
        return self.content_type.model_class()

    @property
    def geometry_field_name(self):
        if self._geometry_field_name is None:
            self._init_table_properties()
        return self._geometry_field_name

    @property
    def geometry_type(self):
        if self._geometry_type is None:
            self._init_table_properties()
        return self._geometry_type

    @property
    def num_features(self):
        return self.datasource.objects.all().count()

    @property
    def srid(self):
        if self._srid is None:
            self._init_table_properties()
        return self._srid

    @property
    def layers(self):
        return FeatureLayer.objects.filter(content_type=self.content_type)


def get_esri_type(django_field):
    """
    @param django_field:
    @return:
    """
    for type_map in DJANGO_FIELDS_TYPES_TO_ESRI:
        if isinstance(django_field, type_map[0]):
            return type_map[1]
    return "esriFieldTypeString"


class FeatureLayer(DatedModel):
    name = models.CharField(max_length=200)
    content_type = models.ForeignKey(ContentType, related_name='%(app_label)s_%(class)s', verbose_name='Data Source',
                                     help_text="Please choose the datasource for your layer")
    service_name = models.CharField(max_length=200, editable=False, unique=True)
    description = models.TextField(blank=True)
    copyright_text = models.TextField(verbose_name="Copyright Text", blank=True)
    max_records = models.IntegerField(default=1000, verbose_name='Maximum Number of Records Returned',
                                      help_text="The maximum number of results that can be returned at once from query, identify and find operations.")
    included_fields_names = models.CharField(max_length=1000, null=True, blank=True, default="*",
                                             verbose_name="Included Fields",
                                             help_text="""The datasource fields that will be included in the generated layer fields.
                    this must be comma separated string.<br/>Example: field_1,field_2<br/>* means all fields.""")
    display_field_name = models.CharField(max_length=100, blank=True, null=True,
                                          help_text="The name of the display field. it must be one of the fields in the included fields")
    drawing_info = models.TextField(null=True, blank=True, verbose_name="Drawing Info", help_text="""A JSON renderer object as returned by the ArcGIS REST API.
    You can find more info <a target='_blank' href='http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#//02r30000019t000000'>here</a>""")
    popup = models.TextField(null=True, blank=True)
    initial_query = models.TextField(blank=True, null=True,
                                     help_text="Specify the filter that is initially applied to data.")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s', null=True, blank=True)
    has_attachments = models.BooleanField(default=True)
    enable_geometry_simplify = models.BooleanField(default=True, help_text="""by set this as True, the returned geometry
     in query requested will be simplified to reduce the number of coordinates which lead to reduce the response size.""")
    tolerance_factor = models.FloatField(default=0, help_text="""When geometry simplify is enabled,
    the simplify tolerance will be this factor multiplied by the minimum edge length in the resulted data bounding box.
    <br/>While simplifing, Points are removed if the distance with the tentative simplified line is smaller than the tolerance.
    <br/>value must be from 0 to 1""")

    class Meta:
        verbose_name = "Feature Service"
        verbose_name_plural = "Feature Services"

    def __init__(self, *args, **kwargs):
        self._geometry_field_name = None
        self._srid = None
        self._geometry_type = None
        self._fields_names = []
        self._fields_defs = []
        self._field_aliases = {}

        super(FeatureLayer, self).__init__(*args, **kwargs)

    @property
    def datasource(self):
        return self.content_type.model_class()

    @property
    def initial_queryset(self):
        """
        @return: a queryset which contain all features
        """
        if self.initial_query is not None and self.initial_query != '':
            try:
                return self.datasource.objects.extra(where=[self.initial_query])
            except:
                pass
        return self.datasource.objects.all()

    @property
    def id_field(self):
        return self.datasource._meta.pk

    @property
    def id_field_name(self):
        return self.datasource._meta.pk.name

    def _init_layer_properties(self):
        for f in self.datasource._meta.fields:
            if issubclass(f.__class__, models.GeometryField):
                self._geometry_field_name = f.attname
                self._srid = f.srid
                self._geometry_type = GEODJANGO_GEOMETRY_TYPES_TO_ESRI[f.geom_type]
            else:
                if self.included_fields_names == "*" or f.attname in self.included_fields_names:
                    self._fields_names.append(f.attname)
                if f.attname in self._fields_names:
                    alias = six.text_type(capfirst(f.verbose_name))
                    field_def = dict(
                        name=f.attname,
                        alias=alias,
                        editable=f.editable if f.attname != self.id_field_name else False,
                        nullable=f.null,
                        type=get_esri_type(f),
                        length=getattr(f, 'max_length', 256)
                    )
                    if field_def["length"] is None:
                        field_def["length"] = 256
                    # TODO handle choices
                    # print getattr(f, 'choices', None)
                    self._fields_defs.append(field_def)
                    self._field_aliases[f.attname] = alias

    @property
    def geometry_field_name(self):
        if not self._geometry_field_name:
            self._init_layer_properties()
        return self._geometry_field_name

    @property
    def srid(self):
        if not self._srid:
            self._init_layer_properties()
        return self._srid

    @property
    def geometry_type(self):
        if not self._geometry_type:
            self._init_layer_properties()
        return self._geometry_type

    @property
    def fields_defs(self):
        if not self._fields_defs:
            self._init_layer_properties()
        return self._fields_defs

    @property
    def field_aliases(self):
        if not self._field_aliases:
            self._init_layer_properties()
        return self._field_aliases

    @property
    def fields_names(self):
        if not self._fields_names:
            self._init_layer_properties()
        return self._fields_names

    @property
    def num_features(self):
        return self.datasource.objects.all().count()

    def get_layer_info(self):
        """
        @return: info object
        """
        d = {}
        d.update(LAYER_INFO_DEFAULTS)
        info = DynamicObject(d)
        # info.extent = self.extent
        info.fields = self.fields_defs
        info.geometryType = self.geometry_type
        info.name = self.name
        info.description = self.description
        info.copyrightText = self.copyright_text
        info.maxRecordCount = self.max_records
        info.objectIdField = self.id_field_name
        info.displayField = self.display_field_name
        info.hasAttachments = self.has_attachments
        try:
            if self.drawing_info is not None:
                info.drawingInfo = DynamicObject(json.loads(self.drawing_info))
                # print info.drawingInfo
        except:
            pass
        bbox = self.initial_queryset.extent()
        srid = 102100 if self.srid == 900913 else self.srid
        info.extent = DynamicObject(dict(
            xmin=bbox[0],
            ymin=bbox[1],
            xmax=bbox[2],
            ymax=bbox[3],
            spatialReference=dict(wkid=srid, latestWkid=srid)
        ))
        return info

    def get_service_info(self):
        layer_info = self.get_layer_info()
        info = DynamicObject(SERVICE_INFO_DEFAULTS)

        info.serviceDescription = self.description
        info.description = self.description
        info.copyrightText = self.copyright_text
        info.maxRecordCount = self.max_records
        info.layers.append(DynamicObject(dict(
            id=0,
            name=layer_info.name
        )))
        info.spatialReference = layer_info.extent.spatialReference
        info.initialExtent = info.fullExtent = layer_info.extent
        return info

    @property
    def meta_page_url(self):
        return reverse(LAYER_INFO_URL_NAME, args=[self.service_name])

    def __unicode__(self):
        return self.name

    def publish(self, request):
        # add default values on add
        if self.id is None or self.service_name == '':
            # service name
            counter = 0
            name = slugify(self.name)
            service_name = name
            while 1:
                try:
                    FeatureLayer.objects.get(service_name=service_name)
                    counter += 1
                    service_name = "%s-%d" % (name, counter)
                except:
                    break
            self.service_name = service_name
            self.drawing_info = DRAWING_INFO_DEFAULTS[self.geometry_type]
        self.save()

    @property
    def geo_table(self):
        try:
            return GeoTable.objects.get(content_type=self.content_type)
        except:
            return None


current_folder = os.path.dirname(__file__)
upload_storage = FileSystemStorage(location=current_folder, base_url='/attachment')
class Attachment(DatedModel):
    def attachment_upload(instance, filename):
        return 'attachments/%s/%s/%s' % (instance.feature_layer.pk, instance.feature_id, filename)

    feature_layer = models.ForeignKey(FeatureLayer)
    feature_id = models.CharField(max_length=300)
    attachment = models.FileField(upload_to=attachment_upload, storage=upload_storage)
    name = models.CharField(max_length=300)
    content_type = models.CharField(max_length=200)


class TileService(DatedModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, editable=False)
    description = models.TextField(blank=True)
    copyright_text = models.TextField(verbose_name="Copyright Text", blank=True)
    background_color = ColorField(null=True, blank=True,
                                  help_text='HTML color code for the background-color of the generated tiles (for instance #000000), Empty value means transparent background ')

    class Meta:
        verbose_name = "Tile Service"
        verbose_name_plural = "Tile Services"

    def __init__(self, *args, **kwargs):
        super(TileService, self).__init__(*args, **kwargs)
        self._mapfile = None
        if self.pk is not None:  # and not os.path.exists(self.mapfile): #TODO uncomment to cash the file
            self.update_mapfile()

    @property
    def meta_page_url(self):
        return "%stiles/%s/tiles/{z}/{x}/{y}.png" % (reverse(MANAGER_HOME_URL_NAME), self.slug,)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # try:
        #     from django.contrib.gis.utils import add_srs_entry
        #     add_srs_entry(self.srid)
        # except:
        #     pass
        super(TileService, self).save(force_insert, force_update, using, update_fields)
        if self.pk is not None:
            self.update_mapfile()

    def update_mapfile(self):
        xml = render_to_string(APP_NAME + '/tiles/style.xml', {'service': self})
        f = open(self.mapfile, 'w+')
        f.write(xml)
        f.close()

    @property
    def mapfile(self):
        if self._mapfile is None:
            current_folder = os.path.dirname(__file__)
            self._mapfile = os.path.abspath(os.path.join(current_folder, 'tiles', 'styles_xml', str(self.pk) + ".xml"))
        return self._mapfile

    def srid(self):
        return 900913

    def proj4text(self):
        try:
            connection_name = self.layers.first().datasource.objects._db
        except:
            datastore = Datastore.objects.get(is_default=True)
            connection_name = datastore.get_connection_name()
        sql = "SELECT proj4text FROM spatial_ref_sys where srid=%d;" % self.srid()
        result = Connector(connection_name).get_result(sql)
        proj4text = result[0]['proj4text']
        return proj4text
        # return "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs";
        # connection_name = DEFAULT_DB_ALIAS
        # try:
        #     datastore = Datastore.objects.get(is_default=True)
        #     connection_name = datastore.get_connection_name()
        # except:
        #     pass
        # SpatialRefSys = connections[connection_name].ops.spatial_ref_sys()
        # sr = SpatialRefSys.objects.get(srid=self.srid)
        # return sr.proj4text

    def center(self):
        return "0,0,2"

    def extent(self):
        return "-180,-85.05112877980659,180,85.05112877980659"

    def max_extent(self):
        return "-20037508.34,-20037508.34,20037508.34,20037508.34"

    def minzoom(self):
        return 0

    def maxzoom(self):
        return 22

    # def background_color(self):
    #     return "#b8dee6"

    def __unicode__(self):
        return self.name

    @property
    def service_url(self):
        return "%stiles/%s/tiles/{z}/{x}/{y}.png" % (reverse(MANAGER_HOME_URL_NAME), self.slug,)


class TilesLayer(DatedModel):
    name = models.CharField(max_length=200)
    content_type = models.ForeignKey(ContentType, verbose_name='Data Source', related_name=APP_NAME + "_layers",
                                     help_text="Please choose the datasource for your layer")
    service = models.ForeignKey(TileService, related_name="layers")
    style = models.TextField(blank=True, null=True)
    filter = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        ordering = ['order']

    def __init__(self, *args, **kwargs):
        self._geometry_field_name = None
        self._srid = None
        self._geometry_type = None
        self._fields_names = []
        self._fields_defs = []
        self._field_aliases = {}

        super(TilesLayer, self).__init__(*args, **kwargs)

    # def delete(self, using=None):
    #     service = self.service
    #     super(Layer, self).delete()
    #     if service.layers.count() == 0:
    #         service.delete()

    def slug(self):
        return slugify(self.name)

    @property
    def datasource(self):
        return self.content_type.model_class()

    def table_name(self):
        table_name = self.datasource._meta.db_table
        if self.filter is not None and self.filter != "":
            table_name = mark_safe("(select * from %s where %s) as temp_table" % (table_name, self.filter))
        return table_name

    def extent(self):
        extent = self.datasource.objects.all().extent()
        return ",".join(map(str, extent))

    def db(self):
        return settings.DATABASES[self.datasource.objects.db]

    @property
    def id_field(self):
        return self.datasource._meta.pk

    @property
    def id_field_name(self):
        return self.datasource._meta.pk.name

    def proj4text(self):
        connection_name = self.datasource.objects._db
        sql = "SELECT proj4text FROM spatial_ref_sys where srid=%d;" % self.srid
        result = Connector(connection_name).get_result(sql)
        proj4text = result[0]['proj4text']
        return proj4text
        # "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs"
        # connection_name = DEFAULT_DB_ALIAS
        # try:
        #     datastore = Datastore.objects.get(is_default=True)
        #     connection_name = datastore.get_connection_name()
        # except:
        #     pass
        # SpatialRefSys = connections[connection_name].ops.spatial_ref_sys()
        # sr = SpatialRefSys.objects.get(srid=self.srid)
        # return sr.proj4text

    def _init_layer_properties(self):
        for f in self.datasource._meta.fields:
            if issubclass(f.__class__, models.GeometryField):
                self._geometry_field_name = f.attname
                self._srid = f.srid
                self._geometry_type = f.geom_type

    @property
    def geometry_field_name(self):
        if not self._geometry_field_name:
            self._init_layer_properties()
        return self._geometry_field_name

    @property
    def srid(self):
        if not self._srid:
            self._init_layer_properties()
        return self._srid

    @property
    def geometry_type(self):
        if not self._geometry_type:
            self._init_layer_properties()
        return self._geometry_type

    def __unicode__(self):
        return self.name


class GeoManager(models.GeoManager):
    def __init__(self, db):
        super(GeoManager, self).__init__()
        self._db = db


class BaseModel(models.Model):
    _db = 'default'

    class Meta:
        abstract = True  # this must be abstract

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(BaseModel, self).save(force_insert=force_insert, force_update=force_update, using=self._db,
                                    update_fields=update_fields)


models_cls = __import__('django.contrib.gis.db.models', globals(), locals(), 'models')
geometry_types = {
    'MULTIPOLYGON': 'MultiPolygonField',
    'MULTIPOINT': 'MultiPointField',
    'MULTILINESTRING': 'MultiLineStringField',
    'LINESTRING': 'LineStringField',
    'POLYGON': 'PolygonField',
    'POINT': 'PointField',
    'GEOMETRYCOLLECTION': 'GeometryCollectionField'
}


class Connector(object):
    model_name_index = 0
    def __init__(self, db='default'):
        self.db = db
        self.connection = connections[self.db]
        self.cursor = self.connection.cursor()

    def get_result(self, sql):
        self.cursor.execute(sql)
        desc = self.cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in self.cursor.fetchall()
            ]

    def get_geo_tables(self):
        return self.get_result("SELECT * FROM geometry_columns WHERE f_table_schema='public'")

    def get_table_fields(self, table_name):
        return self.get_result(
            "select * from INFORMATION_SCHEMA.COLUMNS where table_schema = 'public'  and table_name = '" + table_name + "'")

    def get_field_type(self, connection, table_name, row):
        """
        Given the database connection, the table name, and the cursor row
        description, this routine will return the given field type name, as
        well as any additional keyword parameters and notes for the field.
        """
        field_params = SortedDict()
        field_notes = []

        try:
            if row[1] == 1700:  # numric
                field_type = "FloatField"
            else:
                field_type = connection.introspection.get_field_type(row[1], row)
        except KeyError:
            field_type = 'TextField'
            field_notes.append('This field type is a guess.')

        # This is a hook for data_types_reverse to return a tuple of
        # (field_type, field_params_dict).
        if type(field_type) is tuple:
            field_type, new_params = field_type
            field_params.update(new_params)

        # Add max_length for all CharFields.
        if field_type == 'CharField' and row[3]:
            max_length = int(row[3])
            if max_length == -1:
                field_type = 'TextField'
            else:
                field_params['max_length'] = max_length

        if field_type == 'DecimalField':
            if row[4] is None or row[5] is None:
                field_notes.append(
                    'max_digits and decimal_places have been guessed, as this '
                    'database handles decimal fields as float')
                field_params['max_digits'] = row[4] if row[4] is not None else 10
                field_params['decimal_places'] = row[5] if row[5] is not None else 5
            else:
                field_params['max_digits'] = row[4]
                field_params['decimal_places'] = row[5]

        return field_type, field_params, field_notes

    def create_model(self, table):

        """
        Create specified model
        """
        table_name = str(table["f_table_name"])
        print 'cartoserver: creating model for %s...' % table_name
        try:
            indexes = self.connection.introspection.get_indexes(self.cursor, table_name)
        except NotImplementedError:
            indexes = {}

        class Meta:
            db_table = table_name
            managed = False

        model_attrs = {
            '__module__': __name__,  # set module name to current module name
            '_db': self.db,
            'Meta': Meta,
            'objects': GeoManager(self.db)
        }
        for i, row in enumerate(self.connection.introspection.get_table_description(self.cursor, table_name)):
            field_type, field_params, field_notes = self.get_field_type(self.connection, table_name, row)
            column_name = row[0]
            # field_params['field_name'] = column_name
            # field_params['field_type'] = field_type
            field_params['db_column'] = column_name
            # Add primary_key and unique, if necessary.
            if column_name in indexes:

                if indexes[column_name]['primary_key']:
                    # print indexes[column_name]
                    field_params['primary_key'] = True
                    # I assumed that the primary key is auto increment TODO: check for this
                    field_type = 'AutoField'
                elif indexes[column_name]['unique']:
                    field_params['unique'] = True
                else:
                    field_params['null'] = field_params['blank'] = row[6]

            if field_type == 'GeometryField':
                field_type = geometry_types[str(table['type']).upper()]
                field_params['srid'] = table['srid']
            field_type_cls = getattr(models_cls, field_type)
            from .postgis import get_model_field_name
            field_name = get_model_field_name(column_name)
            model_attrs.update({field_name: field_type_cls(**field_params)})
        
        self.model_name_index += 1
        model_name = "%s_%d" % (self.db, self.model_name_index)
        
        model = type(model_name, (BaseModel,), model_attrs)
        try:
            content_type, created = ContentType.objects.get_or_create(app_label=APP_NAME, name=model_name, model=model_name)
            if getattr(settings, "USE_MANAGED_GEO_SERVICES", False):
                datastore = Datastore.get_by_connection_name(self.db)
                geotable, created = GeoTable.objects.get_or_create(datastore=datastore, table_name=table_name,
                                                                   content_type=content_type)
                if created:
                    geotable.title = geotable.table_name
                    geotable.save()
                    # table_name=name, title=title, description=description, content_type=content_type,
                    #         is_public=is_public, owner=request.user, datastore=datastore
            return content_type
        except Exception as ex:
            print ex.args
            return None

    def create_models(self, table_name=None):
        geo_tables_content_types = {}
        ret_content_type = None
        for table in self.get_geo_tables():
            content_type = self.create_model(table)
            if content_type is not None:
                geo_tables_content_types[str(table["f_table_name"])] = content_type
                if table_name is not None and str(table["f_table_name"]) == table_name.lower():
                    ret_content_type = content_type
            else:
                print 'cannot create model for table %s from %s database' % (str(table["f_table_name"]), self.db)
        Connector.geo_content_types[self.db] = geo_tables_content_types
        return ret_content_type

    geo_content_types = {}

    @staticmethod
    def update_models():
        Connector.geo_content_types = {}
        for db in connections.databases:
            try:
                Connector(db).create_models()
            except:
                print "cannot generate geo models for %s database" % db


# load all databases
def update_geo_table():
    try:
        Datastore.update_database_connections()
        Connector.update_models()
    except:
        pass


update_geo_table()
