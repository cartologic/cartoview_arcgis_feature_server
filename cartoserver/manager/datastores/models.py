__author__ = 'kamal'
#
# 'spatialite': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'kuwait_locations.sqlite'),
#     },
import os
import json
from django.db import connections
from django.conf import settings
from django.db.utils import DEFAULT_DB_ALIAS

current_folder = os.path.dirname(__file__)
datastors_file_path = os.path.join(current_folder, 'datastores.json')
default_datastore_file_path = os.path.join(current_folder, 'default_datastore.json')


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Datastore):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Datastore(object):
    data = {}
    id_count = 0

    def __init__(self, d={}):
        self.ENGINE = 'django.contrib.gis.db.backends.postgis'
        self.NAME = ''
        self.USER = ''
        self.PASSWORD = ''
        self.HOST = 'localhost'
        self.PORT = ''
        self.IS_DEFAULT = False
        # TODO check for valid attributes only
        for a, b in d.items():
            setattr(self, a, b)

    def get_connection_name(self):
        return str("dynamic_stores_" + self.NAME)

    @staticmethod
    def load():
        Datastore.id_count = 0
        Datastore.data = {}
        with open(datastors_file_path) as data_file:
            data = json.load(data_file)
        for item in data:
            Datastore.add(item, True)

    @staticmethod
    def add(item, init=False):
        Datastore.id_count += 1
        if not isinstance(item, Datastore):
            item = Datastore(item)
        item.id = item.pk = Datastore.id_count
        Datastore.data[item.id] = item
        if not init and item.IS_DEFAULT:
            Datastore.set_default(item)

        return item

    @staticmethod
    def update(item):
        # update existing row in data dict
        Datastore.data[item.pk] = item
        if item.IS_DEFAULT:
            Datastore.set_default(item)

    @staticmethod
    def set_default(default_item):
        for item in Datastore.data.values():
            item.IS_DEFAULT = default_item.pk == item.pk

    @staticmethod
    def delete(pk):
        del Datastore.data[pk]

    @staticmethod
    def update_database_connections():
        for item in Datastore.data.values():
            alias = item.get_connection_name()
            if not alias in connections.databases:
                connections.databases[alias] = item.__dict__

    @staticmethod
    def get_default_connection():
        if getattr(settings, 'USE_MANAGED_GEO_SERVICES', False):
            for item in Datastore.data.values():
                if item.IS_DEFAULT:
                    return item.get_connection_name()
        if getattr(settings, 'GEOSERVICES_REST_STORE', None) is not None:
            return settings.GEOSERVICES_REST_STORE
        return DEFAULT_DB_ALIAS

    @staticmethod
    def save():
        with open(datastors_file_path, 'w') as outfile:
            json.dump(Datastore.data.values(), outfile, cls=JSONEncoder)
            outfile.close()
        Datastore.update_database_connections()
