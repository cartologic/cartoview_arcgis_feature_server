from cartoserver.layers_providers import Provider
from cartoserver.models import FeatureLayer
from guardian.shortcuts import get_objects_for_user


class GeonodeLayersProvider(Provider):
    def __init__(self):
        super(GeonodeLayersProvider, self).__init__()
        self.name = "GeonodeLayersProvider"

    def _get_permitted_queryset(self, request, permission):
        permitted_ids = get_objects_for_user(request.user, permission).values('id')
        queryset = FeatureLayer.objects.filter(geonode_layermapping__geonode_layer__id__in=permitted_ids)
        return queryset

    def get_layers(self, request):
        # check if there is no layers load layers from geonode.
        # this is useful if the cartoview app was installed after creating geonode layers
        if FeatureLayer.objects.count() == 0:
            from .models import map_all_layers
            map_all_layers()
        return self._get_permitted_queryset(request, 'base.view_resourcebase')

    def get_layer(self, name, request):
        queryset = self._get_permitted_queryset(request, 'base.view_resourcebase')
        return queryset.get(service_name=name)

    def get_layer_for_metadata_edit(self, name, request):
        queryset = self._get_permitted_queryset(request, 'base.change_resourcebase_metadata')
        return queryset.get(service_name=name)

    def get_layer_for_data_edit(self, name, request):
        queryset = self._get_permitted_queryset(request, 'layers.change_layer_data')
        return queryset.get(service_name=name)