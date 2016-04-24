__author__ = 'Ahmed Nour Eldeen'

from ..json_response_utils import JsonResponse, JsonPResponse, ModelToJson
from models import *
import json
from django.db import models
from django.http import HttpResponse

from PIL import Image
import os
import datetime,time
import os
current_folder = os.path.dirname(__file__)

def items(request, item_id):
    item_obj = Item.objects.get(id=item_id)
    item_json_obj = json.load(open(os.path.join(current_folder,'json','item.json')))
    item_json_obj.update(json.loads(ModelToJson().serialize([item_obj]))[0])

    # item_json_obj = json.loads('{"id":"6f6d3730772143769bd5632539fd6e08","owner":"kamal01","created":1446451748000,"modified":1446474237000,"guid":null,"name":null,"title":"NYC","type":"Web Map","typeKeywords":["ArcGIS Online","Data Editing","Explorer Web Map","Map","Online Map","Web Map"],"description":null,"tags":["nyc"],"snippet":"NYC","thumbnail":"thumbnail/ago_downloaded.png","documentation":null,"extent":[[-74.3383,40.5193],[-73.6173,40.8925]],"spatialReference":null,"accessInformation":null,"licenseInfo":null,"culture":"en-us","properties":null,"url":null,"access":"public","size":4364,"appCategories":[],"industries":[],"languages":[],"largeThumbnail":null,"banner":null,"screenshots":[],"listed":false,"commentsEnabled":true,"numComments":0,"numRatings":0,"avgRating":0,"numViews":90}')
    # item_json_obj["id"] = item_id
    item_json_obj["owner"] = item_obj.owner.username


    if 'callback' in request.REQUEST:
        return JsonPResponse(content=item_json_obj, callback=request.REQUEST["callback"])
    else:
        return JsonResponse(content=item_json_obj)

def get_time(value):
    return time.mktime(value.timetuple())*1000

def get_extent(value):
    return [[value.extent[0], value.extent[1]], [value.extent[2], value.extent[3]]]
def user_items(request, username):
    items_obj = Item.objects.filter(owner__username=username)
    items_json = []
    count = items_obj.count()
    for item in items_obj:
        items_json.append(
            dict(id=str(item.id), owner=item.owner.username, created=get_time(item.created),
                 modified=get_time(item.created), guid=None,
                 name=None, title=item.title, type="Web Map", typeKeywords=[
                    "Online Map", "ArcGIS Online", "Collector",
                    "Data Editing",
                    "Explorer Web Map",
                    "Map",
                    "Offline",
                    "Online Map",
                    "Web Map"
                ], description=item.description, tags=item.tags.split(","), snippet=item.snippet,
                 thumbnail=str(item.thumbnail), documentation=None, extent=get_extent(item.extent), spatialReference=None,
                 accessInformation=None, licenseInfo=None, culture="en-us", properties=None, url=None, access="org",
                 size=4159, appCategories=[], industries=[], languages=[], largeThumbnail=None, banner=None,
                 screenshots=[], listed=None, ownerFolder=None, protected=False, numComments=0, numRatings=0,
                 avgRating=0, numViews=1))
    res_json = {
        "username": username,
        "total": count,
        "start": 1,
        "num": count,
        "nextStart": -1,
        "currentFolder": None,
        "folders":[],
        "items": items_json
    }
    if 'callback' in request.REQUEST:
        return JsonPResponse(content=res_json, callback=request.REQUEST["callback"])
    else:
        return JsonResponse(content=res_json)


def item_data(request, item_id):
    data_json_obj = {}
    try:
        data_json_obj = json.loads(ItemData.objects.get(item_id=item_id).text)
    except models.ObjectDoesNotExist:
        pass
    if 'callback' in request.REQUEST:
        return JsonPResponse(content=data_json_obj, callback=request.REQUEST["callback"])
    else:
        return JsonResponse(content=data_json_obj)



current_folder, filename = os.path.split(os.path.abspath(__file__))
content_media_folder = os.path.abspath(os.path.join(current_folder, 'media'))


def item_thumbnail(request, item_id, file_name):
    thumbnail = Image.open(os.path.join(content_media_folder, 'WebMapThumbnail.png'))
    response = HttpResponse(mimetype='image/png')
    thumbnail.save(response, 'png')
    return response