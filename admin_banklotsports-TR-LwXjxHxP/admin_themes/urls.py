import os

from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^themes/static/banklot/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(getattr(settings, 'PROJECT_PATH', None), 'themes/static/banklot'),
    })
)
