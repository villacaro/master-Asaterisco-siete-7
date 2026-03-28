# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.auth_views import Auth
from .views.conn_views import Connection

urlpatterns = patterns(
    '',
    url(
        regex=r'^connection/$',
        view=Connection.as_view(),
        name='ws_auth_connection_url'
    ),
    url(
        regex=r'^auth/$',
        view=Auth.as_view(),
        name='ws_auth_auth_url'
    ),
)
