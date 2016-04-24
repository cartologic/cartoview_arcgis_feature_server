from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from . import *
from .models import Map, LayerMapping
from arcportal.models import Item, ItemData
import json
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import get_objects_for_user
from django.views.decorators.http import require_POST


def get_context(context):
    from . import *
    context = context or {}
    for key, value in locals().items():
        if isinstance(value, basestring):
            context[key] = value
    return context


def map_list(request):
    permitted_ids = get_objects_for_user(request.user, 'base.view_resourcebase').values('id')
    items = Map.objects.filter(geonode_map__id__in=permitted_ids)
    context_dict = get_context({
        "items": items,
        "portal_base_url": request.build_absolute_uri(reverse("arcportal_home"))[:-1]
    })
    return render_to_response(MAP_LIST_TPL, RequestContext(request, context_dict))


@login_required
def map_edit(request, map_id):
    permitted_ids = get_objects_for_user(request.user, 'base.change_resourcebase_metadata').values('id')
    map_obj = Map.objects.get(geonode_map__id__in=permitted_ids, pk=map_id)
    json_obj = json.loads(ItemData.objects.get(item=map_obj.portal_item).text)
    context_dict = get_context(dict(config_json=json.dumps(json_obj, indent=4), map_obj=map_obj))
    return render_to_response(MAP_EDIT_TPL, RequestContext(request, context_dict))


# def get_nested_attr(obj,attr,default=None):
#     attrs = attr.split(".")
@require_POST
@login_required
def map_publish(request, map_id):
    permitted_ids = get_objects_for_user(request.user, 'base.change_resourcebase_metadata').values('id')
    map_obj = Map.objects.get(geonode_map__id__in=permitted_ids, pk=map_id)
    map_obj.publish()
    return HttpResponseRedirect(reverse(MAP_EDIT_URL_NAME, args=(map_id,)))


def map_config_save(request, map_id):
    if request.method == 'POST':
        permitted_ids = get_objects_for_user(request.user, 'base.change_resourcebase_metadata').values('id')
        map_obj = Map.objects.get(geonode_map__id__in=permitted_ids, pk=map_id)
        item_data_obj = ItemData.objects.get(item=map_obj.portal_item)
        item_data_obj.text = request.POST['config-json']
        item_data_obj.save()
        map_obj.edited = True
        map_obj.save()
    return HttpResponseRedirect(reverse(MAP_EDIT_URL_NAME, args=(map_id,)))


def map_config_reset(request, map_id):
    return map_publish(request, map_id)
