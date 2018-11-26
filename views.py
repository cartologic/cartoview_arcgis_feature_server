from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from . import *
from .cartoserver.views import get_layer_for_metadata_edit, get_layers
# from .layers_providers import GeonodeLayersProvider
from .forms import FeatureLayerEditForm


def get_context(context):
    from . import *
    context = context or {}
    for key, value in locals().items():
        if isinstance(value, basestring):
            context[key] = value
    return context


# layers_provider = GeonodeLayersProvider()


def layer_list(request):
    context_dict = get_context({
        "items": get_layers(request)
    })
    return render(request, LAYER_LIST_TPL, context_dict)


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
    return render(request, LAYER_EDIT_TPL, context_dict)
