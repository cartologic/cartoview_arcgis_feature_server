__author__ = 'Ahmed Nour Eldeen'

from django.conf.urls import patterns, url
import views


url_patterns = patterns('',
    # url(r'^rest/tokens$', views.tokens, name="arcportal_rest_tokens"),
    url(r'^generateToken$', views.generate_token, name="arcportal_generate_token"),
    url(r'^generateToken/$', views.generate_token, name="generate_token"),
)