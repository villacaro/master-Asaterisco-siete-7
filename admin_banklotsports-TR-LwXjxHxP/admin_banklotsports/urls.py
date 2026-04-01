# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Urls del admin de django
    url(r'^' + settings.ADMIN_URL[1:], include(admin.site.urls)),

    # urls de las app desarrolladas

    url(r'^', include('admin_comercializacion.urls')),
    url(r'^', include('admin_finanzas.urls')),
    url(r'^', include('admin_historic.urls')),
    url(r'^', include('admin_juego.urls')),
    url(r'^', include('admin_logros.urls')),
    url(r'^', include('admin_mail.urls')),
    url(r'^', include('admin_permisologia.urls')),
    url(r'^', include('admin_profiles.urls')),
    url(r'^', include('admin_principal.urls')),
    url(r'^', include('admin_reportes.urls')),
    url(r'^', include('admin_resultados.urls')),
    url(r'^', include('admin_soporte.urls')),
    url(r'^', include('admin_themes.urls')),
    url(r'^', include('admin_users.urls')),
    url(r'^', include('api.urls')),
    # urls de los archivos media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
