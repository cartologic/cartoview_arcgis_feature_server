from django.conf.urls import url

import views

from .. import *

url_patterns = [
    url(r'^$', views.search, name=SEARCH_URL_NAME)
]
