# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.get_parley_data_views import GetParleyData, GetParleyDataByDeporte
from .views.get_parley_result_views import GetParleyResult, GetParleyResultTable

urlpatterns = patterns(
    '',
    url(
        regex=r'^getparleydata/$',
        view=GetParleyData.as_view(),
        name='ws_sport_requests_getparleydata_url'
    ),

    url(
        regex=r'^getparleydatabydeporte/$',
        view=GetParleyDataByDeporte.as_view(),
        name='ws_sport_requests_getparleydatabydeporte_url'
    ),

    url(
        regex=r'^getparleyresult/$',
        view=GetParleyResult.as_view(),
        name='ws_sport_requests_getparleyresult_url'
    ),

    url(
        regex=r'^getparleyresulttable/$',
        view=GetParleyResultTable.as_view(),
        name='ws_sport_requests_getparleyresulttable_url'
    ),
)
