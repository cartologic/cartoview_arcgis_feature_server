from django import template
from .. import *
from ..views import get_context
from ..cartoserver.views import get_layer_for_metadata_edit


register = template.Library()


@register.inclusion_tag(LAYER_LIST_ACTIONS_TPL, takes_context=True)
def layer_list_actions(context):
    request = context['request']
    layer = context["item"]
    try:
        get_layer_for_metadata_edit(request, layer.service_name)
        can_edit = True
    except:
        can_edit = False

    return get_context({
        'layer': layer,
        'can_edit': can_edit,
    })