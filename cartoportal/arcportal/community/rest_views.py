__author__ = 'Ahmed Nour Eldeen'

from ..utils import parse_query
from django.views.decorators.csrf import csrf_exempt
import time
from ..json_response_utils import JsonResponse, ModelToJson
from ..token_manager.models import Token
from ..token_manager import views as token_manager_views
from django.contrib.auth import get_user_model
User = get_user_model()
import json

from models import Group as GroupModel


@csrf_exempt
def community(request):
    token_obj = Token.objects.get(token=request.REQUEST['token'])
    response_json = {}
    if token_manager_views.is_valid_token(token_obj.token):
        response_json = get_user_json(token_obj.user)
    return JsonResponse(content=response_json)


def community_users(request, username):
    response_json = {}
    if token_manager_views.is_valid_token(request.GET['token']):
        user = User.objects.get(username=username)
        response_json = get_user_json(user)
    return JsonResponse(content=response_json)


def groups(request):
    groups_json = {
        "query": request.GET['q'],
        "total": 0,
        "start": 1,
        "num": 0,
        "nextStart": -1,
        "results": []
    }

    tokens = parse_query(request.GET['q'])
    groups_list = GroupModel.objects.filter(title=tokens[0][2].strip('"'))
    groups_json["num"] = groups_json["total"] = groups_list.count()
    groups_json["results"] = json.loads(ModelToJson().serialize(groups_list))
    return JsonResponse(content=groups_json)


def get_user_json(user):
    return {
        "username": user.username,
        "fullName": user.get_full_name(),
        "preferredView": "Web",
        "description": "",
        "email": user.email,
        "access": "public",
        # "storageUsage": 0,
        # "storageQuota": 0,
        "orgId": "%s" % user.id,
        "role": user.groups.first().name,  # TODO:roles should be mapped to user groups
        # "tags": [
        #     "<GIS Analyst>",
        #     "<City of Redlands>"
        # ],
        # "culture": "en",
        # "region": "US",
        # "thumbnail": "<myProfile.jpg>",
        "created": time.mktime(user.date_joined.timetuple()) * 1000,
        "modified": time.mktime(user.date_joined.timetuple()) * 1000,
        "groups": []
    }



