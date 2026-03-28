from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'ws_sportparley.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('ws_auth.urls')),
    url(r'^', include('ws_requests.urls')),
    url(r'^', include('ws_sport_requests.urls')),
    url(r'^', include('ws_notifications.urls')),
    url(r'^', include('ws_process.urls')),
    url(r'^', include('ws_reports.urls')),
    url(r'^', include('ws_mail.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
