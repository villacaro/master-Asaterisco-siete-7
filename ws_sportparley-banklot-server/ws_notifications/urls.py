# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.keepalive_views import KeepAlive
from .views.notifications_views import Notifications, NotificationsCadena, NotificationsLost

urlpatterns = patterns(
    '',
    url(
        regex=r'^notifications/$',
        view=Notifications.as_view(),
        name='ws_notifications_notifications_url'
    ),
    url(
        regex=r'^notifications/lost/$',
        view=NotificationsLost.as_view(),
        name='ws_notifications_notifications_lost_url'
    ),
    url(
        regex=r'^notifications/cadena/$',
        view=NotificationsCadena.as_view(),
        name='ws_notifications_cadena_notifications_url'
    ),
    url(
        regex=r'^keepalive/$',
        view=KeepAlive.as_view(),
        name='ws_notifications_keepalive_url'
    ),
)
