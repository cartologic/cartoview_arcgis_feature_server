from django import template
from guardian.shortcuts import get_objects_for_user, get_perms

from ..models import Map
from .. import *
from ..views import get_context


register = template.Library()

@register.inclusion_tag(MAP_LIST_ACTIONS_TPL, takes_context=True)
def map_list_actions(context):
    request = context['request']
    map = context["item"]
    permitted_ids = get_objects_for_user(request.user, 'base.change_resourcebase_metadata').values('id')
    queryset = Map.objects.filter(geonode_map__id__in=permitted_ids)
    try:
        queryset.get(id=map.id)
        can_edit = True
    except:
        can_edit = False

    return get_context({
        'item': map,
        'can_edit': can_edit,
    })
