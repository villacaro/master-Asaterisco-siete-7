import importlib
import threading as thread

from admin_asterisco7.settings import REDIS_DB
from admin_comercializacion.models import Preferences
from admin_finanzas.models import Comercializadora
from admin_lib.util_task import AsyncGestionOperationalError
try:
    from celery.registry import tasks
except ImportError:
    tasks = {}
from django.core.cache import cache


class AsyncProcessPreferencesDelete(AsyncGestionOperationalError):
    name = 'AsyncProcessPreferencesDelete'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        comercializadora = Comercializadora.objects.get(
            pk=kwargs.get('comercializadora')
        )
        self.cont = 0
        self.typepreferences = kwargs.get('typepreferences')

        self.delete_preferences(comercializadora)

        return ['{0} comercializadora(s) gestionada(s)'.format(self.cont)]

    def delete_preferences(self, comercializadora):
        childs = comercializadora.get_offspring()
        for child in childs:
            self.cont += 1

            for _id in self.typepreferences:
                key = 'preference_{0}_{1}'.format(
                    child.id,
                    _id
                )
                cache.delete(key)

            preferences_comer = Preferences.objects.filter(
                comercializacion_id=child.id,
                typepreference_id__in=self.typepreferences
            )
            for preference_comer in preferences_comer:
                preference_comer.delete()


tasks.register(AsyncProcessPreferencesDelete)


class AsyncProcessInvokeMethod(AsyncGestionOperationalError):
    name = 'AsyncProcessInvokeMethod'
    queue = 'default'

    def run_try(self, *args, **kwargs):

        module = importlib.import_module(kwargs.pop('module'))
        module_class = getattr(module, kwargs.pop('class'))
        module_method = getattr(module_class, kwargs.pop('method'))

        # Como este proceso es asyncrono verificamos si la session fue envidada
        # y procedemos a configurar la auditoria para que relacione esa session
        REDIS_DB.set(
            '{0}'.format(thread.get_ident()),
            kwargs.pop('session_id'),
            60 * 60
        )
        message = module_method(kwargs.pop('parametros'))
        # REDIS_DB.delete('{0}'.format(thread.get_ident()))

        return message

    def func_delay(func, kwargs, delay=True):
        kwargs['module'] = func.__module__
        kwargs['class'] = func.__qualname__.split('.')[0]
        kwargs['method'] = func.__qualname__.split('.')[1]
        if delay:
            AsyncProcessInvokeMethod.delay(
                *(),
                **kwargs
            )
        else:
            async_task = AsyncProcessInvokeMethod()
            async_task.run(
                *(),
                **kwargs
            )


tasks.register(AsyncProcessInvokeMethod)
