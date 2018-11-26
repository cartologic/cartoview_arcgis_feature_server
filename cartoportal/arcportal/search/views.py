__author__ = 'Ahmed Nour Eldeen'

from django.views.decorators.csrf import csrf_exempt
from ..json_response_utils import JsonResponse, JsonPResponse, ModelToJson
from ..models import Item
import json

from ..utils import parse_query
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@csrf_exempt
def search(request):
    query = request.REQUEST["q"]
    query_tokens = parse_query(query)
    filters = {'type': 'Web Map'}
    if query_tokens[0][0] == 'owner':
        filters['owner__username'] = query_tokens[0][2].strip("\"")
    elif query_tokens[0][0] in ['id', 'group']:
        filters[query_tokens[0][0]] = query_tokens[0][2].strip("\"")
    results = Item.objects.filter(**filters)

    sort_field = request.REQUEST.get('sortField')
    allowed_fileds = ['title', 'uploaded', 'type', 'owner',  'modified']
    if sort_field is not None and sort_field in allowed_fileds:
        if sort_field == 'uploaded':
            sort_field = 'created'
        #title, uploaded, type, owner, modified, avgRating, numRatings, numComments, and numViews.
        sort_order = request.REQUEST.get('sortOrder')
        if sort_order == 'desc':
            sort_field = "-" + sort_field
        results = results.order_by(sort_field)
    # paging
    total = results.count()
    items_per_page = int(request.REQUEST.get('num', 10))
    start = int(request.REQUEST.get('start', 1)) - 1
    results = results[start : start + items_per_page]

    results_json = json.loads(ModelToJson().serialize(results))
    for item in results_json:
        item["owner"] = request.user.username
    search_json = {
    "nextStart": start + items_per_page + 1 if start + items_per_page + 1 < total else -1,
    "results": results_json,
    "start": start + 1,
    "num": items_per_page,
    "query": query,
    "total": total
    }

    return JsonResponse(content=search_json)