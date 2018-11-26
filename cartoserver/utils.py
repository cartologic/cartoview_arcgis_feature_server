__author__ = 'kamal'
import json
import decimal
from django.db.models.base import ModelState

def get_context(context):
    from . import *
    context = context or {}
    for key, value in locals().items():
        if isinstance(value, basestring):
            context[key] = value
    return context


class DynamicObject(object):
    def __init__(self, d={}):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [DynamicObject(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, DynamicObject(b) if isinstance(b, dict) else b)

    # __getattr__ is called if the object doesn't have the attribute as member
    # this to avoid "object has no attribute" error and make the object acts like javascript
    def __getattr__(self, name):
        return None

    def json(self):
        return json.dumps(self, cls=DynamicObjectJSONEncoder, separators=(',', ':'))


class DynamicObjectJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DynamicObject):
            return obj.__dict__
        if hasattr(obj, 'isoformat'): # handle Date types
           return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
           return float(obj)
        elif isinstance(obj, ModelState):
           return None
        return json.JSONEncoder.default(self, obj)
