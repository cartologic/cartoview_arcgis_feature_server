__author__ = 'Ahmed Nour Eldeen'

from ..json_response_utils import ModelToJson
from django.shortcuts import render, redirect
import json
from models import Item, ItemData
import datetime
from django.core.urlresolvers import reverse
from django.contrib.gis.geos.polygon import Polygon


def new_item(request):
    if request.method == 'POST':
        item_json_obj = json.loads(request.POST['map-json'])
        item_obj = Item()
        item_obj.owner = request.user
        item_obj.name = item_json_obj['name']
        item_obj.title = item_json_obj['title']
        item_obj.url = item_json_obj['url']
        item_obj.type = item_json_obj['type']
        item_obj.type_keywords = ",".join(item_json_obj['typeKeywords'])
        item_obj.description = item_json_obj['description']
        item_obj.tags = ",".join(item_json_obj['tags'])
        item_obj.snippet = item_json_obj['snippet']
        item_obj.thumbnail = item_json_obj['thumbnail']
        if item_json_obj['extent']:
            item_obj.extent = Polygon.from_bbox(item_json_obj['extent'][0]+item_json_obj['extent'][1])

        item_obj.created = datetime.datetime.today()
        item_obj.modified = datetime.datetime.today()

        item_obj.save()

        if 'text' in item_json_obj:
            item_data_obj = ItemData(item=item_obj, text=json.dumps(item_json_obj['text']))
            item_data_obj.save()
        return redirect(reverse('content.edit_item', args=[item_obj.id]))
    else:
        return render(request, 'content/edit_item.html')


def edit_item(request, item_id):
    item_obj = Item.objects.get(id=item_id)
    if request.method == 'POST':
        item_json_obj = json.loads(request.POST['map-json'])
        item_obj.owner = request.user
        item_obj.name = item_json_obj['name']
        item_obj.title = item_json_obj['title']
        item_obj.url = item_json_obj['url']
        item_obj.type = item_json_obj['type']
        item_obj.type_keywords = ",".join(item_json_obj['typeKeywords'])
        item_obj.description = item_json_obj['description']
        item_obj.tags = ",".join(item_json_obj['tags'])
        item_obj.snippet = item_json_obj['snippet']
        item_obj.thumbnail = item_json_obj['thumbnail']
        if item_json_obj['extent']:
            item_obj.extent = Polygon.from_bbox(item_json_obj['extent'][0]+item_json_obj['extent'][1])
        item_obj.modified = datetime.datetime.today()

        item_obj.save()

        if 'text' in item_json_obj:
            item_data_obj = ItemData(item=item_obj, text=json.dumps(item_json_obj['text']))
            item_data_obj.save()
    # TODO: handle array types in a better way.
    item_obj.type_keywords = item_obj.type_keywords.split(",")
    item_obj.tags = item_obj.tags.split(",")
    # TODO: handle single object instead of removing square brackets from the string.
    fields = ['name', 'title', 'url', 'type', 'type_keywords', 'description', 'tags', 'snippet', 'thumbnail', 'extent']
    item_json_obj = json.loads(ModelToJson().serialize([item_obj], indent=True, fields=fields).strip("[]\n"))
    try:
        item_json_obj['text'] = json.loads(ItemData.objects.get(item_id=item_id).text)
    except:
         pass
    return render(request, 'content/edit_item.html', {'item_obj': json.dumps(item_json_obj, indent=4)})
