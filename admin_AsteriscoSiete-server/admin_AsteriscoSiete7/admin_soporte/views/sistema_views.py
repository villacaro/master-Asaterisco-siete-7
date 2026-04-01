# -*- coding: utf-8 -*-

from admin_asterisco7.settings import REDIS_DB
from admin_lib.util_views import MyViewBase
from admin_soporte.forms import SistemForm
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView

MESSAGES_INDICE = ['DESHABILITADA', 'HABILITADA']

MESSAGES = {
    'cache_clear': 'Cache reiniciada con éxito!',
    'bet_taquilla': 'Ventas en taquilla {0} con éxito!',
    'pay_taquilla': 'Pago de tickets en taquilla {0} con éxito!',
    'connection_taquilla': 'Conexiónes en taquilla {0} con éxito!',
    'connection_panel': 'Conexión en panel {0} con éxito!',
}

KEYS_CODENAME = {
    'bet_taquilla': 'WS_MAINTENANCE_BET',
    'pay_taquilla': 'WS_MAINTENANCE_PAY',
    'connection_taquilla': 'WS_MAINTENANCE_GLOBAL',
    'connection_panel': 'PANEL_MAINTENANCE_GLOBAL',
}

KEYS_ARRAY = ['bet_taquilla', 'pay_taquilla', 'connection_taquilla', 'connection_panel']


class OptionsSystem(MyViewBase, FormView):
    form_class = SistemForm
    template_name = 'admin_soporte/sistema/opciones/index.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs

    def post(self, request, *args, **kwargs):
        process = self.request.POST.get('_process', None)
        if process == 'cache_clear':
            cache.clear()
            messages.info(self.request, MESSAGES.get('cache_clear'))
            return HttpResponseRedirect(reverse('admin_soporte_sistema_opciones'))

        change_check = None
        for key in self.request.POST:
            if key in KEYS_ARRAY:
                change_check = key
                break

        key_cod = KEYS_CODENAME[change_check]
        if self.get_profile().codename != 'userprofile_master':
            key_redis = '{0}-{1}'.format(key_cod, self.object_comercializadora.id)
        else:
            key_redis = '{0}'.format(key_cod)

        value = REDIS_DB.get(key_redis)
        if value:
            value = 1 - int(value)
            REDIS_DB.set(key_redis, value)
        else:
            value = 0
            REDIS_DB.set(key_redis, 0)

        messages.info(self.request, MESSAGES.get(change_check).format(MESSAGES_INDICE[value]))
        return HttpResponseRedirect(reverse('admin_soporte_sistema_opciones'))
