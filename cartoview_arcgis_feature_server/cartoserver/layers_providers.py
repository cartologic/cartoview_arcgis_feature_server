from .models import Connector
from .models import FeatureLayer, GeoTable
from django.conf import settings


class Provider(object):
    def __init__(self):
        self.name = "LayerProvider"

    def get_layers(self, request):
        raise NotImplemented

    def get_layer(self, name, request):
        raise NotImplemented

    def refresh(self):
        raise NotImplemented

    def get_layer_for_metadata_edit(self, name, request):
        return self.get_layer(name, request)

    def get_layer_for_data_edit(self, name, request):
        return self.get_layer(name, request)

class BasicProvider(Provider):
    _layers_dict = None
    _layers = None

    def __init__(self):
        super(BasicProvider, self).__init__()
        self.name = "BasicLayerProvider"

    def _init_layers(self):
        BasicProvider._layers_dict = dict()
        BasicProvider._layers = []
        for db in Connector.geo_content_types:
            for model_name in Connector.geo_content_types[db]:
                content_type = Connector.geo_content_types[db][model_name]
                layer = FeatureLayer()
                layer.name = layer.service_name = content_type.name
                layer.content_type = content_type
                BasicProvider._layers.append(layer)
                BasicProvider._layers_dict[layer.name] = layer

    def get_layers(self, request):
        if BasicProvider._layers is None:
            self._init_layers()
        return BasicProvider._layers

    def get_layer(self, name, request):
        if BasicProvider._layers is None:
            self._init_layers()
        return BasicProvider._layers_dict[name]

    def refresh(self):
        self._init_layers()


class ManagedServicesProvider(Provider):
    def __init__(self):
        super(ManagedServicesProvider, self).__init__()
        self.name = "ManagedServicesProvider"

    def get_layers(self, request):
        return FeatureLayer.objects.all()

    def get_layer(self, name, request):
        return FeatureLayer.objects.get(service_name=name)


if hasattr(settings, 'GEO_SERVICES_LAYERS_PROVIDER'):
    parts = settings.GEO_SERVICES_LAYERS_PROVIDER.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    layers_provider = m()
elif getattr(settings, 'USE_MANAGED_GEO_SERVICES', False):
    layers_provider = ManagedServicesProvider()
else:
    layers_provider = BasicProvider()
