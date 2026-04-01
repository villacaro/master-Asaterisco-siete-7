# -*- coding: utf-8 -*-

import datetime
import threading as thread

from admin_banklotsports.settings import ACTIVATE_HISTORY, FORMAT_STR_DATE_3, REDIS_DB
from admin_historic.models import SessionsDetail, UsersProcesses
from admin_principal.security import Security
from crequest.middleware import CrequestMiddleware
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models

DEFAULT_TIME_CACHE_HISTORIC = 120


def register(*args):
    """
    Registra un modelo para su auditoria en la interaccion con la db
    """
    if not ACTIVATE_HISTORY:
        """
        en caso de estar desactivada
        la auditoria no se registran los modelos en la instancia actual
        """
        return

    for model in args:
        if model is not None:
            model.audit_save = True
            models.signals.pre_save.connect(audit_pre_save, sender=model)
            models.signals.post_save.connect(audit_post_save, sender=model)
            models.signals.pre_delete.connect(audit_pre_delete, sender=model)
            models.signals.post_delete.connect(audit_post_delete, sender=model)

            m2ms = model._meta.many_to_many
            for m2m in m2ms:
                sender_m2m = getattr(model, m2m.name).through
                models.signals.m2m_changed.connect(audit_m2m_change, sender=sender_m2m)

            """
            Se agrega una funcion a la clase que sirve para obtener el url del historico
            """

            def get_url_historic(self):
                return reverse(
                    'admin_historic_app_model_ref',
                    kwargs={
                        'app': self._meta.app_label,
                        'model': self.__class__.__name__.lower(),
                        'ref': self.pk
                    }
                )

            def get_ref_historic(self):
                return '{0}.{1}.{2}'.format(
                    self._meta.app_label,
                    self.__class__.__name__.lower(),
                    self.pk
                )

            model.get_url_historic = get_url_historic
            model.get_ref_historic = get_ref_historic


def get_key_for_instance(instance, cache_prefix='django_historic'):
    """
    Devuelve un key generado para manipular la instancia en la cache
    """
    return '%s_%s_%s' % (cache_prefix, instance.__class__.__name__, instance.pk)


def serialize_model(instance, update_fields=None, propiedades=['fields', 'foreign', 'm2m'], process='update'):
    """
    Serializa el modelo en un json,
    teniendo en cuenta todos los distintos
    tipos de atributos, guardandolos en variables
    distintas para diferenciarlos
    """
    messaje = {}
    messaje['fields'] = {}
    messaje['foreign'] = {}
    messaje['m2m'] = {}

    for attr in instance._meta.fields:
        valor = getattr(instance, attr.name, None)

        audit_exclude = getattr(instance, 'audit_exclude', ()) + ('created_at',)

        if attr.primary_key:
            """
            Si es la clave primaria no la guarda
            o si es la fecha del login anterior en usuaios
            """
            continue

        elif attr.name in audit_exclude:
            """
            Validación de atributos excluidos
            """
            continue

        if update_fields and attr.name not in update_fields:
            continue

        if valor is not None and (isinstance(attr, models.ForeignKey) or isinstance(attr, models.OneToOneField)):
            """
            Si es un campo de tipo foraneo lo audita de cierta manera
            particular, obteniendo su pk y un cadena de texto del objeto q lo
            representa.
            """
            messaje['foreign'][attr.name] = {}
            messaje['foreign'][attr.name]['{0}'.format(valor.pk)] = '{0}'.format(valor)
        else:
            if valor is None and process != 'update':
                continue
            messaje['fields'][attr.name] = '{0}'.format(humanize_value(valor))

    if 'm2m' in propiedades:
        for attr in instance._meta.many_to_many:
            if attr.name not in audit_exclude:
                valor = getattr(instance, attr.name, None)
                messaje['m2m'][attr.name] = {}
                for val in valor.all():
                    messaje['m2m'][attr.name][val.pk] = '{0}'.format(val)

    return messaje


def humanize_value(value):
    if value is None:
        value = ''
    elif isinstance(value, bool):
        if value is True:
            value = 'Sí'
        else:
            value = 'No'
    elif isinstance(value, datetime.datetime):
        value = value.strftime(FORMAT_STR_DATE_3)
    return value


def audit_pre_save(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.pk:

        if kwargs.get('update_fields'):
            querry = sender.objects.only(*kwargs['update_fields'])
        else:
            querry = sender.objects

        try:
            object_old = serialize_model(
                querry.get(pk=instance.pk),
                kwargs.get('update_fields'),
            )
            cache.set(get_key_for_instance(instance), object_old, DEFAULT_TIME_CACHE_HISTORIC)
        except Exception:
            pass


def audit_post_save(sender, **kwargs):
    if kwargs.get('instance').audit_save:
        if kwargs['created']:
            save_audit(kwargs, 'create')
        else:
            """
            como es una actualizacion se indica que deben
            gestionarse las atributos propios de la clase
            """
            save_audit(kwargs, 'update', ['fields', 'foreign', ])
    else:
        kwargs.get('instance').audit_save = True


def audit_pre_delete(sender, **kwargs):
    if kwargs.get('instance').audit_save:
        save_audit(kwargs, 'delete')


def audit_post_delete(sender, **kwargs):
    pass


def audit_m2m_change(sender, **kwargs):
    """
    audit m2m changes if the settings DJANGO_SIMPLE_AUDIT_M2M_FIELDS is set to True
    """
    if kwargs.get('instance').audit_save is False:
        kwargs.get('instance').audit_save = True
        return

    action = kwargs.get('action')
    if action:
        if kwargs['action'] == 'pre_add':
            pass
        elif kwargs['action'] == 'post_add':
            """
            aqui solo de indica verificar los campos m2m
            """
            save_audit(kwargs, 'update', ['m2m', ])
        elif kwargs['action'] == 'pre_remove':
            pass
        elif kwargs['action'] == 'post_remove':
            """
            aqui solo de indica verificar los campos m2m
            """
            save_audit(kwargs, 'update', ['m2m', ])
        elif kwargs['action'] == 'pre_clear':
            save_audit(kwargs, 'update', ['m2m', ])
        elif kwargs['action'] == 'post_clear':
            pass


def save_audit(kwargs={}, process=None, propiedades=[]):

    instance = kwargs['instance']

    def get_user_process(instance, process):
        """
        Obtiene el proceso de usuario invocado en cada accion respectiva
        """

        model = instance.__class__.__name__
        codename = 'model_' + model.lower() + '_' + process
        try:
            process = UsersProcesses.get_userprocess_by_codename(codename=codename)
        except UsersProcesses.DoesNotExist:
            label = {
                'create': 'Creación de ',
                'update': 'Actualización de ',
                'delete': 'Eliminación de '
            }
            if isinstance(instance._meta.verbose_name_plural, str):
                verbose = instance._meta.verbose_name_plural
            else:
                verbose = model

            try:
                process = UsersProcesses.objects.get_or_create(
                    name=label[process] + verbose,
                    codename=codename,
                    content_type=instance._meta.app_label,
                    process_suc=UsersProcesses.get_userprocess_by_codename(
                        codename='process_login'
                    ),
                )[0]
            except Exception:
                """
                Aqui podria ir una llamada recursiva a la mia funcion pero
                es mejor evitar problemas recursivos, y tratarla de obtener
                de una vez
                """
                process = UsersProcesses.get_userprocess_by_codename(codename=codename)
        return process

    request = CrequestMiddleware.get_request()
    url_process = ''
    session = None
    if request:
        url_process = request.path
        security = Security()
        try:
            session = security.get_session(request).pk
        except Exception:
            pass
    else:
        session = REDIS_DB.get('{0}'.format(thread.get_ident()))

    json_update = {
        'model': instance._meta.app_label + '.' + instance.__class__.__name__,
        'url': url_process,
        'attr': {
            'fields': {},
            'foreign': {},
            'm2m': {}
        },
        'process': process,
    }

    is_save = False
    if process == 'update':
        """
        la cache no hay necesida de eliminarla, ya que se invalida
        de manera automatica al pasar 120 segundos
        """
        old = cache.get(get_key_for_instance(instance))

        if old is not None:
            new = serialize_model(instance, kwargs.get('update_fields'), propiedades)
            cache.set(get_key_for_instance(instance), new, DEFAULT_TIME_CACHE_HISTORIC)

            """
            Buscando cambios en los fields
            Buscando cambios en los foreign
            Buscando cambios en los m2m
            """
            for propiedad in propiedades:
                for key in old[propiedad].keys():
                    if old[propiedad].get(key) != new[propiedad].get(key):
                        json_update['attr'][propiedad][key] = [
                            old[propiedad].get(key),
                            new[propiedad].get(key)
                        ]
                        if is_save is False:
                            is_save = True
        else:
            """
            si ocurre algun error guarda el objeto actual completo
            """
            # json_update['attr'] = new
            # json_update['process'] = 'create'
            # is_save = True
            pass

    elif process == 'create':
        json_update['attr'] = serialize_model(instance, kwargs.get('update_fields'), propiedades, process)
        is_save = True
    elif process == 'delete':
        json_update['attr'] = serialize_model(instance, kwargs.get('update_fields'), propiedades, process)
        is_save = True

    if is_save:
        json_update['object'] = '{0}'.format(instance)

        if hasattr(instance, 'get_ref_related_historic'):
            ref_related = instance.get_ref_related_historic()
        else:
            ref_related = None

        SessionsDetail.objects.create(
            session_id=session,
            userprocess=get_user_process(instance, process),
            json=json_update,
            ref=instance.get_ref_historic(),
            ref_related=ref_related
        )
