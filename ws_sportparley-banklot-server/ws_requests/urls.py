# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.getdata_views import GetData
from .views.getfiles_views import GetFiles

urlpatterns = patterns(
    '',
    url(
        regex=r'^getdata/$',
        view=GetData.as_view(),
        name='ws_requests_getdata_url'
    ),
    url(
        regex=r'^getfiles/$',
        view=GetFiles.as_view(),
        name='ws_requests_getfiles_url'
    ),
)
