# -*- coding: utf-8 -*-

import json
import logging

from admin_asterisco7 import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils.functional import Promise
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

try:
    from django.utils.encoding import force_str as force_str  # Django < 1.5
except ImportError as e:
    from django.utils.encoding import force_str  # Django 1.5 / python3
logger = logging.getLogger(__name__)


class LazyEncoder(DjangoJSONEncoder):
    """Encodes django's lazy i18n strings
    """

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super(LazyEncoder, self).default(obj)


class JSONResponseMixin(object):
    is_clean = False

    def render_to_response(self, context):
        """ Returns a JSON response containing 'context' as payload
        """
        return self.get_json_response(context)

    def get_json_response(self, content, **httpresponse_kwargs):
        """ Construct an `HttpResponse` object.
        """
        response = HttpResponse(content,
                                content_type='application/json',
                                **httpresponse_kwargs)
        add_never_cache_headers(response)
        return response

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.request = request
        response = None

        try:
            func_val = self.get_context_data(**kwargs)
            if not self.is_clean:
                assert isinstance(func_val, dict)
                response = dict(func_val)
                if 'result' not in response:
                    response['result'] = 'ok'
            else:
                response = func_val
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        except Exception as e:
            if not request.is_ajax():
                raise

            logger.error('JSON view error: %s' % request.path, exc_info=True)

            # Come what may, we're returning JSON.
            if hasattr(e, 'message'):
                msg = e.message
                msg += str(e)
            else:
                msg = _('Internal error') + ': ' + str(e)
            response = {'result': 'error',
                        'sError': msg,
                        'text': msg}
        keys = []
        for key in response:
            try:
                json.dumps(response[key], cls=LazyEncoder)
            except Exception:
                keys.append(key)
        for key in keys:
            response.pop(key)

        if settings.DEBUG_TOOLBAR and not request.is_ajax():
            return HttpResponse('<html lang="es"><head></head><body><div>{0}</div></body></html>'.format(
                response
            )
            )
        else:
            dump = json.dumps(response, cls=LazyEncoder)
            return self.render_to_response(dump)


class JSONResponseView(JSONResponseMixin, TemplateView):
    pass
