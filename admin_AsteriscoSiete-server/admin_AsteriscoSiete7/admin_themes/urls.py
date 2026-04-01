import os

from django.conf import settings
from django.urls import include, re_path
from django.views.static import serve

urlpatterns = [
re_path(r'^themes/static/asterisco7/(?P<path>.*)$', serve, {
        'document_root': os.path.join(getattr(settings, 'PROJECT_PATH', None), 'themes/static/asterisco7'),
    })
]
