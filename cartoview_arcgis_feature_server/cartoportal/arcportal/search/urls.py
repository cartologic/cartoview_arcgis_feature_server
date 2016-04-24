__author__ = 'Ahmed Nour Eldeen'
from .. import *
from django.conf.urls import patterns, url
import views


url_patterns = patterns('',
    url(r'^$', views.search, name=SEARCH_URL_NAME)
)