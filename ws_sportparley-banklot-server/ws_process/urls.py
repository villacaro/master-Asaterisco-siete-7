# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.process_bet_views import Bet
from .views.process_change_password_views import ChangePassword
from .views.process_checking_last_bet_views import CheckingLastBet

urlpatterns = patterns(
    '',
    url(
        regex=r'^bet/$',
        view=Bet.as_view(),
        name='ws_process_bet_url'
    ),

    url(
        regex=r'^bet/checking-last/$',
        view=CheckingLastBet.as_view(),
        name='ws_process_change_password_url'
    ),

    url(
        regex=r'^change-password/$',
        view=ChangePassword.as_view(),
        name='ws_process_change_password_url'
    ),
)
