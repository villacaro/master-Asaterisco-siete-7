# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.getmail_views import GetMail, GetMails, ReadMail, SendMail

urlpatterns = patterns(
    '',
    url(
        regex=r'^getmail/$',
        view=GetMail.as_view(),
        name='ws_mail_getmail_url'
    ),
    url(
        regex=r'^getmails/$',
        view=GetMails.as_view(),
        name='ws_mail_getmails_url'
    ),
    url(
        regex=r'^readmail/$',
        view=ReadMail.as_view(),
        name='ws_mail_readmail_url'
    ),
    url(
        regex=r'^sendmail/$',
        view=SendMail.as_view(),
        name='ws_mail_sendmail_url'
    ),
)
