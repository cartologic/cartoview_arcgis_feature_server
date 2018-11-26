__author__ = 'Ahmed Nour Eldeen'

from django.conf.urls import patterns, url
import rest_views
from .. import *

rest_url_patterns = patterns('',
     url(r'^self$', rest_views.community, name=COMMUNITY_URL_NAME),
     url(r'^groups$', rest_views.groups, name=COMMUNITY_GROUPS_URL_NAME),
     url(r'^users/(?P<username>[^/]+)$', rest_views.community_users, name=COMMUNITY_USERS_URL_NAME),
 )