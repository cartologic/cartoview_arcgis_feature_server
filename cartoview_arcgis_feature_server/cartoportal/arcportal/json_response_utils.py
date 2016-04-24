__author__ = 'Ahmed Nour Eldeen'

import json
from django.http import HttpResponse
from django.core.serializers.json import Serializer
from django.utils.encoding import smart_text, is_protected_type
import datetime,time
from django.contrib.gis.geos.polygon import Polygon




class JsonResponse(HttpResponse):
    """
        JSON response
    """
    def __init__(self, content, mimetype=None, status=None, content_type='application/json', cors=True):
        super(JsonResponse, self).__init__(
            content=content if type(content) is str else json.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )

        if cors:
            # enable cross-domain requests
            self["Access-Control-Allow-Origin"] = "*"


class JsonPResponse(HttpResponse):
    """
        JSONP response
    """
    def __init__(self, content, mimetype=None, status=None, content_type='text/javascript', callback='callback'):
        response = "%s(%s)" % (callback, content if type(content) is str else json.dumps(content))
        super(JsonPResponse, self).__init__(
            content=response,
            mimetype=mimetype,
            status=status,
            content_type=content_type,
        )


class ModelToJson(Serializer):

    def get_dump_object(self, obj):
        json_obj = {obj._meta.pk.name: smart_text(obj._get_pk_val(), strings_only=True)}
        json_obj.update(self._current)
        return json_obj

    def handle_field(self, obj, field):
        value = field._get_val_from_obj(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        field_json_name = underscore_to_camelcase(field.name)
        if isinstance(value, datetime.datetime):
            # convert to milliseconds
            self._current[field_json_name] = time.mktime(value.timetuple())*1000
        elif is_protected_type(value):
            self._current[field_json_name] = value
        elif isinstance(value, list):
            self._current[field_json_name] = value
        elif isinstance(value, Polygon):
            self._current[field_json_name] = [[value.extent[0], value.extent[1]], [value.extent[2], value.extent[3]]]
        else:
            self._current[field_json_name] = field.value_to_string(obj)


def underscore_to_camelcase(word):
    words = word.split('_')
    return ''.join((x.capitalize() if x != words[0] else x) for x in words)
