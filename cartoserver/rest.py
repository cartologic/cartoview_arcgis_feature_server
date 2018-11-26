
from tastypie.authorization import Authorization
from django.db.models import Q
from tastypie.authentication import  BasicAuthentication
from django.conf.urls import url
from .models import *
from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from django.contrib.gis.geos import Polygon

class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(Q(is_public=True) | Q(owner=bundle.request.user))

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.owner == bundle.request.user or bundle.obj.is_public

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.owner == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.owner == bundle.request.user:
                allowed.append(obj)

        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.owner == bundle.request.user


# this class implementation is from https://github.com/amezcua/TastyPie-DjangoCookie-Auth/blob/master/DjangoCookieAuth.py
class DjangoCookieBasicAuthentication(BasicAuthentication):
    '''
     If the user is already authenticated by a django session it will
     allow the request (useful for ajax calls) . If it is not, defaults
     to basic authentication, which other clients could use.
    '''

    def __init__(self, *args, **kwargs):
        super(DjangoCookieBasicAuthentication, self).__init__(*args, **kwargs)

    def is_authenticated(self, request, **kwargs):
        from django.contrib.sessions.models import Session
        if 'sessionid' in request.COOKIES:
            s = Session.objects.get(pk=request.COOKIES['sessionid'])
            if '_auth_user_id' in s.get_decoded():
                u = User.objects.get(id=s.get_decoded()['_auth_user_id'])
                request.user = u
                return True
        return super(DjangoCookieBasicAuthentication, self).is_authenticated(request, **kwargs)


# class GeoTableResource(ModelResource):
#     num_features = fields.IntegerField(attribute='num_features', readonly=True)
#     srid = fields.IntegerField(attribute='srid', readonly=True)
#     geometry_type = fields.CharField(attribute='geometry_type', readonly=True)
#     content_type_id = fields.IntegerField(attribute="content_type_id", readonly=True, null=True)
#     # owner = fields.ForeignKey(UserResource, 'owner',full=True, null=True, blank=True, readonly=True)
#     is_mine = fields.BooleanField()
#     datastore = fields.CharField(readonly=True, null = True)
#     # layers = fields.ToManyField('FeatureLayerResource', 'layers', full=True, readonly=True, null=True, blank=True)
#
#     class Meta:
#         queryset = GeoTable.objects.all()
#         # can_edit = True
#         authorization = UserObjectsOnlyAuthorization()
#         authentication = DjangoCookieBasicAuthentication()
#         # filtering = {
#         #     'is_mine': ALL
#         # }
#
#     def dehydrate_is_mine(self, bundle):
#         return bundle.obj.owner == bundle.request.user
#
#     def dehydrate_datastore(self, bundle):
#         return bundle.obj.datastore.name
#
#     def hydrate(self, bundle):
#         if not bundle.obj.id:
#             bundle.obj.owner = bundle.request.user
#         return bundle
#
#     def build_filters(self, filters=None):
#         if filters is None:
#             filters = {}
#         if ('is_mine' in filters):
#             orm_filters = {'is_mine': filters['is_mine'] == 'true'}
#
#             filters.pop('is_mine')
#         else:
#             orm_filters = super(GeoTableResource, self).build_filters(filters)
#
#         return orm_filters
#
#     def apply_filters(self, request, applicable_filters):
#         custom = None
#         if 'is_mine' in applicable_filters:
#             is_mine = applicable_filters.pop('is_mine')
#             if is_mine:
#                 custom = Q(owner=request.user)
#
#         semi_filtered = super(GeoTableResource, self).apply_filters(request, applicable_filters)
#
#         return semi_filtered.filter(custom) if custom else semi_filtered
#
#     def prepend_urls(self):
#         urls = super(GeoTableResource, self).prepend_urls()
#         return urls + [
#             url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/download%s$" % (self._meta.resource_name, trailing_slash()),
#                 self.wrap_view('download_detail'), name="api_download_detail"),
#         ]
#
#     def download_detail(self, request, **kwargs):
#         pk = kwargs.pop('pk', None)
#         geotable = self._meta.queryset.get(pk=pk)
#
#         from shapes.views import ShpResponder
#         qs = geotable.content_type.model_class().objects.all()
#         # proj = form.cleaned_data['projection']
#         # query = form.cleaned_data['query']
#         # if query:
#         #     where = query.replace("%", "%%")
#         #     qs = qs.extra(where=[where])
#         # bbox = form.cleaned_data['bbox']
#         # if bbox:
#         #     bbox_arr = map(float, bbox.split(","))
#         #     geom = Polygon.from_bbox(bbox_arr)
#         #     filter_kwargs = {}
#         #     key = obj.geometry_field_name + "__intersects"
#         #     filter_kwargs[key] = geom
#         #     qs = qs.filter(**filter_kwargs)
#         shp_response = ShpResponder(qs)  # , proj_transform=proj)
#         shp_response.file_name = geotable.title  # + ("" if proj is None else "_" + str(proj))
#         return shp_response()


class FeatureLayerResource(ModelResource):
    # geo_table = fields.ForeignKey(GeoTableResource, 'geo_table', full=True, readonly=True, null=True, blank=True)
    service_name = fields.CharField(attribute='service_name', readonly=True)
    geometry_type = fields.CharField(attribute='geometry_type', readonly=True)
    meta_page_url = fields.CharField(attribute='meta_page_url', readonly=True)
    srid = fields.IntegerField(attribute='srid', readonly=True)
    num_features = fields.IntegerField(attribute='num_features', readonly=True)

    class Meta:
        queryset = FeatureLayer.objects.all()
        can_edit = False
        authorization = DjangoAuthorization()
        # filtering = {
        #     'provider': ALL_WITH_RELATIONS,
        #     'geo_table': ALL_WITH_RELATIONS
        # }

    def dehydrate_meta_page_url(self, bundle):
        return bundle.request.build_absolute_uri(bundle.obj.meta_page_url)

    # def build_filters(self, filters=None):
    #     if filters is None:
    #         filters = {}
    #     if ('geo_table' in filters):
    #         geo_table_id = filters['geo_table']
    #         geo_table = GeoTable.objects.get(id=geo_table_id)
    #         qset = Q(content_type=geo_table.content_type)
    #         orm_filters = {'custom': qset}
    #     else:
    #         orm_filters = super(FeatureLayerResource, self).build_filters(filters)
    #
    #     return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(FeatureLayerResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered

    # def hydrate(self, bundle):
    #     if not bundle.obj.id:
    #         bundle.obj.owner = bundle.request.user
    #     geotable_id = bundle.data.get('geotable')
    #     if geotable_id:
    #         geotable = GeoTable.objects.get(pk=geotable_id)
    #         del bundle.data['geotable']
    #         bundle.obj.content_type = geotable.content_type
    #     return bundle

    def save(self, bundle, skip_errors=False):
        bundle = super(FeatureLayerResource, self).save(bundle, skip_errors)
        bundle.obj.publish(bundle.request)
        return bundle


# class DatastoreResource(ModelResource):
#     class Meta:
#         queryset = Datastore.objects.all()
#         can_edit = False
#         authorization = DjangoAuthorization()



# class TilesLayerResource(ModelResource):
#     content_type_id = fields.IntegerField(attribute="content_type_id", null=True)
#     service = fields.ForeignKey("%s.rest.TilesServiceResource" % APP_NAME, 'service', null=True)
#     class Meta:
#         queryset = TilesLayer.objects.all()
#         authorization = DjangoAuthorization()
#
#     def hydrate(self, bundle):
#
#         return bundle

# class TilesServiceResource(ModelResource):
#     service_url = fields.CharField( readonly=True)
#     layers = fields.ToManyField(TilesLayerResource, 'layers', full=True, null=True)
#     extent = fields.CharField(readonly=True,null=True)
#     class Meta:
#         queryset = TileService.objects.all()
#         authorization = DjangoAuthorization()
#
#     def dehydrate_service_url(self, bundle):
#         return "%stiles/%s/tiles/{z}/{x}/{y}.png" % (bundle.request.build_absolute_uri(reverse(MANAGER_HOME_URL_NAME)), bundle.obj.slug,)
#
#
#     def dehydrate_extent(self, bundle):
#         # todo get extent from all layers or from the xml file
#         try:
#             layer = bundle.obj.layers.first()
#             extent = map(float, layer.datasource.objects.all().extent())
#             print extent
#             poly = Polygon.from_bbox(extent)
#             #do the transformation in the database not. a hack to avoid transformation using gdal
#             #todo fix this issue to use gdal
#             connection_name = layer.datasource.objects._db
#             sql ="SELECT ST_AsText(ST_Transform(ST_GeomFromText('%s',%d),4326)) As geom;" % (poly.wkt, layer.srid)
#             from .models import Connector
#             wkt = Connector(connection_name).get_result(sql)[0]['geom']
#             from django.contrib.gis.geos import GEOSGeometry
#             poly = GEOSGeometry(wkt) # WKT
#             # poly.srid = layer.srid
#             # poly.transform(4326)
#             return map(float, poly.extent)
#
#         except:
#             return None
#
#     def hydrate(self, bundle):
#         for layer in bundle.obj.layers.all():
#             layer.service = bundle.obj
#         return bundle
#
#     def save(self, bundle, skip_errors=False):
#         bundle = super(TilesServiceResource, self).save(bundle, skip_errors)
#         bundle.obj.save()
#         return bundle
#
#     def obj_create(self, bundle, **kwargs):
#
#         bundle.obj = self._meta.object_class()
#
#         for key, value in kwargs.items():
#             setattr(bundle.obj, key, value)
#         layers = bundle.data.pop('layers')
#         bundle = self.full_hydrate(bundle)
#         bundle = self.save(bundle)
#         for layer in layers:
#             layer['service'] = bundle.obj
#             TilesLayer(**layer).save()
#         from django.utils.text import slugify
#         bundle.obj.slug = slugify(bundle.obj.name)
#         bundle.obj.save()
#         return bundle