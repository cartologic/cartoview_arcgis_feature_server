from cartoview_arcgis_feature_server.cartoserver.query import GeoDjangoQuery
from . import *
from django.http import HttpResponse
from django.shortcuts import render
from .utils import get_context, DynamicObject
from .edit import GeoDjangoEdit
from .constants import *
import QueryParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.gzip import gzip_page
from .forms import AttachmentForm
from .models import Attachment
from guardian.shortcuts import get_objects_for_user
from .models import FeatureLayer
from geonode.layers.models import Layer


def _get_permitted_queryset(request, permission):
    permitted_ids = get_objects_for_user(request.user, permission).values('id')
    queryset = Layer.objects.filter(id__in=permitted_ids)
    return queryset

    # queryset = FeatureLayer.objects.filter(geonode_layer__id__in=permitted_ids)
    # return queryset


def get_layers(request):
    qs = _get_permitted_queryset(request, 'base.view_resourcebase')
    layers = []
    for geonode_layer in qs:
        layer = FeatureLayer.get_layer(geonode_layer)
        if layer is not None:
            layers.append(layer)
    return layers

def get_layer(request, service_name):
    queryset = _get_permitted_queryset(request, 'base.view_resourcebase')
    return FeatureLayer.get_layer(queryset.get(name=service_name))


def get_layer_for_metadata_edit(request, service_name):
    queryset = _get_permitted_queryset(request, 'base.change_resourcebase_metadata')
    return FeatureLayer.get_layer(queryset.get(name=service_name))


def get_layer_for_data_edit(request, service_name):
    queryset = _get_permitted_queryset(request, 'layers.change_layer_data')
    return FeatureLayer.get_layer(queryset.get(name=service_name))


def response_to_json(request, context=None, json_str=None):
    if context is not None:
        json_str = context['json'].json()
    content_type = "application/json"
    callback = request.GET.get('callback', None)
    if callback:
        content_type = "text/javascript"
        json_str = "%s(%s);" % (callback, json_str)
    response = HttpResponse(json_str, content_type=content_type)
    # enable cross-domain requests
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def response_to_html(request, context, template):
    return render(request, template, context)


def response_to_format(request, context, template):
    response_format = str(request.GET.get("f", request.POST.get("f", "HTML"))).upper()
    if response_format == "HTML":
        return response_to_html(request, context, template)
    return response_to_json(request, context)


@csrf_exempt
def folder_info(request, path=""):
    json_res = DynamicObject(FOLDER_INFO_DEFAULTS)
    for layer in get_layers(request):
        json_res.services.append(DynamicObject(dict(name=layer.service_name, type="FeatureServer")))
    context = get_context(dict(
        json=json_res
    ))
    return response_to_format(request, context, REST_ENDPOINT_FOLDER_TPL)


@csrf_exempt
def server_info(request):
    return folder_info(request)


@csrf_exempt
def service_info(request, service_name):
    layer = get_layer(request, service_name)
    context = get_context({
        'service_name': service_name,
        'json': layer.get_service_info()
    })
    return response_to_format(request, context, REST_ENDPOINT_SERVICE_TPL)


@csrf_exempt
def layer_info(request, service_name):
    layer = get_layer(request, service_name)
    context = get_context({
        'service_name': service_name,
        'json': layer.get_layer_info()
    })
    return response_to_format(request, context, REST_ENDPOINT_LAYER_TPL)



@csrf_exempt
@gzip_page
def layer_query(request, service_name):
    layer = get_layer(request, service_name)
    query_params = QueryParser.parse(request)
    # print (query_params.__dict__.keys())
    # TODO validate query params before calling GeoDjangoQuery.query
    qs = GeoDjangoQuery.query(layer, query_params)
    context = get_context(dict(
        json=qs,
        layer=layer
    ))
    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)
    # layer = get_layer(request, service_name)
    # context = get_context(dict(
    #     layer=layer
    # ))
    # response_format = str(request.GET.get("f", request.POST.get("f", "HTML"))).upper()
    # if response_format == "HTML":
    #
    #     return response_to_html(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)
    #
    # query_params = QueryParser.parse(request)
    # # params = dict(user_id=request.user.pk, service_name=service_name, query_params=query_params.__dict__)
    # # task = query_json_task.apply([request.user.pk, service_name, query_params.__dict__])
    # # task = query_json_task.delay(request.user.pk, service_name, query_params.__dict__)
    # return response_to_json(request, json_str="{}")


@login_required
@csrf_exempt
def layer_apply_edits(request, service_name):
    layer = get_layer_for_data_edit(request, service_name)
    edit_result = GeoDjangoEdit.apply_edits(layer, request.POST)
    context = get_context(dict(
        json=edit_result,
        layer=layer
    ))
    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)


@login_required
@csrf_exempt
def layer_add_features(request, service_name):
    layer = get_layer_for_data_edit(request, service_name)
    edit_result = GeoDjangoEdit.add_features(layer, request.POST)
    context = get_context(dict(
        json=edit_result,
        layer=layer
    ))
    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)


@login_required
@csrf_exempt
def layer_update_features(request, service_name):
    layer = get_layer_for_data_edit(request, service_name)
    edit_result = GeoDjangoEdit.update_features(layer, request.POST)
    context = get_context(dict(
        json=edit_result,
        layer=layer
    ))
    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)


@login_required
@csrf_exempt
def layer_delete_features(request, service_name):
    layer = get_layer_for_data_edit(request, service_name)
    edit_result = GeoDjangoEdit.delete_features(layer, request.POST)
    context = get_context(dict(
        json=edit_result,
        layer=layer
    ))
    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)


@csrf_exempt
def attachment_info(request, service_name, feature_id):
    attachments = Attachment.objects.filter(feature_id=feature_id, feature_layer__geonode_layer__name=service_name)
    infos = []
    for a in attachments:
        infos.append({
            "id": a.id,
            "parentGlobalId": feature_id,
            "name": a.name,
            "contentType": a.content_type,
            "size": a.attachment.size
        })
    context = get_context(dict(
        json=DynamicObject({"attachmentInfos": infos})
    ))
    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)


@require_POST
@login_required
@csrf_exempt
def add_attachment(request, service_name, feature_id):
    context = get_context({})
    layer = get_layer_for_data_edit(request, service_name)
    if layer.has_attachments:
        attach = Attachment(feature_layer=layer, feature_id=feature_id)
        form = AttachmentForm(request.POST, request.FILES, instance=attach)
        form.save(False)
        attach.name = attach.attachment.name
        attach.content_type = request.FILES["attachment"].content_type
        attach.save()

        context = get_context(dict(
            json=DynamicObject(dict(objectId=attach.pk, globalId=None, success=True)),
            layer=layer
        ))

    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)


def attachment(request, service_name, feature_id, attachment_id):
    a = Attachment.objects.get(pk=attachment_id, feature_id=feature_id, feature_layer__geonode_layer__name=service_name)
    return HttpResponse(a.attachment.file, mimetype=a.content_type)


@require_POST
@login_required
@csrf_exempt
def delete_attachment(request, service_name, feature_id):
    ids = request.POST.getlist("attachmentIds")
    deletes = []
    for pk in ids:
        a = Attachment.objects.get(pk=pk, feature_id=feature_id, feature_layer__geonode_layer__name=service_name)
        a.delete()
        deletes.append({"objectId": pk, "globalId": None, "success": True})
    context = get_context(dict(
        json=DynamicObject(dict(deleteAttachmentResults=deletes))
    ))
    return response_to_format(request, context, REST_ENDPOINT_LAYER_QUERY_TPL)
