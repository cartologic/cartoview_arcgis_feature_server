__author__ = 'Ahmed Nour Eldeen'
from .. import *
import os
from django.conf.urls import patterns, url, static
import views
import rest_views


url_patterns = patterns('',
    url(r'^newItem/$', views.new_item, name=CONTENT_NEW_ITEM_URL_NAME),
    url(r'^editItem/(?P<item_id>[^/]+)/$', views.edit_item, name=CONTENT_EDIT_ITEM_URL_NAME)
)


current_folder, filename = os.path.split(os.path.abspath(__file__))
rest_url_patterns = patterns('',
    url(r'^users/(?P<username>[^/]+)$', rest_views.user_items, name=USER_ITEMS_URL_NAME),
    url(r'^items/(?P<item_id>[^/]+)$', rest_views.items, name=ITEMS_URL_NAME),
    url(r'^items/(?P<item_id>[^/]+)/data$', rest_views.item_data, name=ITEM_DATA_URL_NAME),
    url(r'^items/(?P<item_id>[^/]+)/info/thumbnail/(?P<file_name>[^/]+)$', rest_views.item_thumbnail, name=ITEM_DATA_THUMB_URL_NAME),
)


