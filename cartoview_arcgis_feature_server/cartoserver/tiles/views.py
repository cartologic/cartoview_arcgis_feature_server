from .. import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from ..models import *
import TileStache





def tiles(request, service_slug, z, x, y, extension):
    """
    Proxy to tilestache
    {X} - coordinate column.
    {Y} - coordinate row.
    {B} - bounding box.
    {Z} - zoom level.
    {S} - host.
    """
    service = TileService.objects.get(slug=service_slug)
    config = {
        "cache": {"name": "Test"},
        "layers": {}
    }
    config["layers"][service_slug]={
        "provider": {
            'name': 'mapnik',
            "mapfile": service.mapfile
        }
    }
    config = TileStache.Config.buildConfiguration(config)
    path_info = "%s/%s/%s/%s.%s" % (service_slug, z, x, y, extension)
    coord, extension = TileStache.splitPathInfo(path_info)[1:]
    mimetype, content = TileStache.getTile(config.layers[service_slug], coord, extension)
    return HttpResponse(content, mimetype=mimetype)


def xml_view(request, service_slug):
    service = TileService.objects.get(slug=service_slug)
    return render(request, APP_NAME + '/tiles/style.xml', {'service': service})

from django.contrib.gis.geos import Polygon
def preview_service(request, service_slug):
    service = TileService.objects.get(slug=service_slug)
    layer = service.layers.first()
    extent = map(float, layer.datasource.objects.all().extent())
    poly = Polygon.from_bbox(extent)
    poly.srid = layer.srid
    poly.transform(4326)
    context = {
        "service": service,
        "extent": ",".join(map(str, poly.extent)),
        "layer_url": "%stiles/%s/tiles/{z}/{x}/{y}.png" % (request.build_absolute_uri(reverse(MANAGER_HOME_URL_NAME)) , service.slug,)
    }
    return render(request, APP_NAME + '/map.html', context)