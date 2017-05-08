from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# from .layers_providers import GeonodeLayersProvider
from .forms import FeatureLayerEditForm
from django.contrib.auth.decorators import login_required
from . import *

def get_context(context):
    from . import *
    context = context or {}
    for key, value in locals().items():
        if isinstance(value, basestring):
            context[key] = value
    return context


# layers_provider = GeonodeLayersProvider()
from .cartoserver.views import get_layers, get_layer_for_metadata_edit

def layer_list(request):
    context_dict = get_context({
        "items": get_layers(request)
    })
    return render_to_response(LAYER_LIST_TPL, RequestContext(request, context_dict))

@login_required
def layer_edit(request, layer_name):
    layer = get_layer_for_metadata_edit(request, layer_name)
    saved = False
    if request.method == "POST":
        form = FeatureLayerEditForm(request.POST, instance=layer)
        if form.is_valid():
            form.save()
            saved = True
    else:
        form = FeatureLayerEditForm(instance=layer)
    context_dict = get_context({
        "form": form,
        "saved": saved
    })
    return render_to_response(LAYER_EDIT_TPL, RequestContext(request, context_dict))
