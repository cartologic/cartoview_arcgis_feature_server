from django import template
from .. import *
from ..views import get_context, layers_provider


register = template.Library()


@register.inclusion_tag(LAYER_LIST_ACTIONS_TPL, takes_context=True)
def layer_list_actions(context):
    request = context['request']
    layer = context["item"]
    try:
        layers_provider.get_layer_for_metadata_edit(layer.service_name,request)
        can_edit = True
    except:
        can_edit = False

    return get_context({
        'layer': layer,
        'can_edit': can_edit,
    })