from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.exceptions import NotFound
from tastypie.resources import Resource
from .models import Datastore

class DatastoreResource(Resource):
    # fields must map to the attributes in the Datastore class
    id = fields.IntegerField(attribute = 'id', null=True)
    NAME = fields.CharField(attribute = 'NAME')
    USER = fields.CharField(attribute = 'USER')
    PASSWORD = fields.CharField(attribute = 'PASSWORD')
    HOST = fields.CharField(attribute = 'HOST')
    PORT = fields.CharField(attribute = 'PORT')
    IS_DEFAULT = fields.BooleanField(attribute = 'IS_DEFAULT', default=False)

    class Meta:
        #resource_name = 'post'
        object_class = Datastore
        authentication = Authentication()
        authorization = Authorization()

    # def prepend_urls(self):
    #     return [
    #         url(r"^(?P<resource_name>%s)/default%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('default_datastore'), name="default_datastore"),
    #     ]

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object (typically a ``Model`` instance),
        it returns the extra kwargs needed to generate a detail URI.

        By default, it uses the model's ``pk`` in order to create the URI.
        """
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj.obj, self._meta.detail_uri_name)
        else:
            kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj, self._meta.detail_uri_name)

        return kwargs

    def get_object_list(self, request):
        # inner get of object list... this is where you'll need to
        # fetch the data from what ever data source
        Datastore.load()
        return Datastore.data.values()

    def obj_get_list(self, request = None, **kwargs):
        # outer get of object list... this calls get_object_list and
        # could be a point at which additional filtering may be applied
        return self.get_object_list(request)

    def obj_get(self, request = None, **kwargs):
        # get one object from data source
        pk = int(kwargs['pk'])
        Datastore.load()
        try:
            return Datastore.data[pk]
        except KeyError:
            raise NotFound("Object not found") 
    
    def obj_create(self, bundle, request = None, **kwargs):
        # create a new row
        bundle.obj = Datastore()
        
        # full_hydrate does the heavy lifting mapping the
        # POST-ed payload key/values to object attribute/values
        bundle = self.full_hydrate(bundle)
        
        # we add it to our in-memory data dict for fun
        Datastore.load()
        item = Datastore.add(bundle.obj)
        Datastore.save()
        return bundle
    
    def obj_update(self, bundle, request = None, **kwargs):
        # update an existing row
        pk = int(kwargs['pk'])
        try:
            bundle.obj = Datastore.data[pk]
        except KeyError:
            raise NotFound("Object not found")
        
        # let full_hydrate do its work
        bundle = self.full_hydrate(bundle)
        Datastore.update(bundle.obj)
        Datastore.save()
        return bundle

    def obj_delete(self, bundle, **kwargs):
        pk = int(kwargs.pop("pk"))
        try:
            bundle.obj = Datastore.data[pk]
        except KeyError:
            raise NotFound("A model instance matching the provided arguments could not be found.")

        # self.authorized_delete_detail(self.get_object_list(bundle.request), bundle)
        Datastore.delete(pk)
        Datastore.save()





