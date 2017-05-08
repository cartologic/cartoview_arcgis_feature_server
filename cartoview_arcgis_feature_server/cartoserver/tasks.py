from .utils import DynamicObject
from .query import GeoDjangoQuery
# from .layers_providers import layers_provider
from celery import shared_task, current_task



@shared_task
def query_json_task(user_id, service_name, query_params):
    print "start task"
    query_params = DynamicObject(query_params)
    layer = layers_provider.get_layer(service_name, user_id)
    # TODO validate query params before calling GeoDjangoQuery.query
    qs = GeoDjangoQuery.query(layer, query_params)
    return  qs.json()
