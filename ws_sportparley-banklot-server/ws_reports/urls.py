# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views.analysis_cash_box_views import AnalysisCashBox
from .views.analysis_daily_views import AnalysisDaily
from .views.analysis_periodic_views import AnalysisPeriodic
from .views.ticket_cancel_views import TicketCancel
from .views.ticket_details_views import TicketDetails
from .views.ticket_forward_views import TicketForward
from .views.ticket_last_ticket_views import LastTicket
from .views.ticket_pay_views import TicketPay
from .views.tickets_list_views import TicketsList
from .views.tickets_winners_views import TicketsWinners

urlpatterns = patterns(
    '',
    url(
        regex=r'^ticket/forward/$',
        view=TicketForward.as_view(),
        name='ws_reports_ticket_forward_url'
    ),
    url(
        regex=r'^ticket/details/$',
        view=TicketDetails.as_view(),
        name='ws_reports_ticket_details_url'
    ),
    url(
        regex=r'^ticket/cancel/$',
        view=TicketCancel.as_view(),
        name='ws_reports_ticket_cancel_url'
    ),
    url(
        regex=r'^ticket/pay/$',
        view=TicketPay.as_view(),
        name='ws_reports_ticket_pay_url'
    ),
    url(
        regex=r'^tickets/winners/$',
        view=TicketsWinners.as_view(),
        name='ws_reports_ticket_winners_url'
    ),
    url(
        regex=r'^tickets/list/$',
        view=TicketsList.as_view(),
        name='ws_reports_ticket_list_url'
    ),
    url(
        regex=r'^ticket/last-ticket/$',
        view=LastTicket.as_view(),
        name='ws_reports_ticket_last_ticket'
    ),
    url(
        regex=r'^analysis/daily/$',
        view=AnalysisDaily.as_view(),
        name='ws_reports_analysis_daily_url'
    ),
    url(
        regex=r'^analysis/periodic/$',
        view=AnalysisPeriodic.as_view(),
        name='ws_reports_analysis_periodic_url'
    ),
    url(
        regex=r'^analysis/cash-box/$',
        view=AnalysisCashBox.as_view(),
        name='ws_reports_analysis_cash_box_url'
    ),
)
