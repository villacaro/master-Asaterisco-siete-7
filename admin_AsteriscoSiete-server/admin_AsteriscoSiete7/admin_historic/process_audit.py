import ast
import datetime
import json as JSON

from admin_asterisco7.settings import FORMAT_STR_DATE_3
from admin_comercializacion.models import FactorRiesgo
from admin_historic.models import SessionsDetail
from admin_juego.models import Sorteo, SorteoDetalle, apuesta, ModalidadJuego
from admin_permisologia.models import PermissionsSalesRestrictions
from admin_resultados.models import AnotacionesDetail, Resultados
from django.apps import apps as django_apps
from django.db.models import Q


class AdminJuegoProcess(object):

    def process_encuentros(self, objecto):
        model = Sorteo
        json = {}
        json['object'] = {}
        json['object']['fields'] = []
        json['object']['fields_related'] = {}
        json['process'] = objecto.json.get('process')

        if objecto.json.get('process') == 'create':
            # Generic Part
            json['object']['fields'] = get_fields_basic_create(
                model, objecto.json['attr'])

            # Custom Part
            ref_relateds = SessionsDetail.objects.filter(
                ref_related=objecto.ref,
                ref__startswith='admin_juego.encuentrosdetail',
                updated_at__range=[objecto.updated_at,
                                   objecto.updated_at + datetime.timedelta(seconds=5)]
            ).order_by('updated_at')

            equipos = {}
            for refr in ref_relateds:
                nombre = list(
                    refr.json['attr']['foreign']['equipos_temporadas'].values()
                )[0]

                equipos[nombre] = {}
                equipos[nombre]["Home/Visitante"] = django_apps.get_model(
                    'admin_juego',
                    'encuentrosdetail'
                ).str_indice[refr.json['attr']['fields']['indice']]

                if refr.json['attr']['foreign'].get('jugador'):
                    equipos[nombre]["NumeroSorteo"] = '{0}({1})'.format(
                        list(
                            refr.json['attr']['foreign']['jugador'].values()
                        )[0],
                        refr.json['attr']['fields']['referencia'],
                    )

            json['object']['fields_related']['ModalidadJuego'] = equipos

        elif objecto.json.get('process') == 'update':
            # Generic Part
            json['object']['fields'] = get_fields_basic_update(
                model, objecto.json['attr']
            )

            # Custom Part
            ref_relateds = SessionsDetail.objects.filter(
                ref_related=objecto.ref,
                ref__startswith='admin_juego.encuentrosdetail',
                updated_at__range=[objecto.updated_at,
                                   objecto.updated_at + datetime.timedelta(seconds=5)]
            ).order_by('updated_at')

            equipos = {}
            model = SorteoDetalle

            for refr in ref_relateds:
                fields = get_fields_basic_update(model, refr.json['attr'])
                if fields:
                    nombre = SorteoDetalle.objects.get(
                        pk=refr.json['object']
                    )

                    fields[0]['Home/Visitante'][0] = django_apps.get_model(
                        'admin_juego',
                        'encuentrosdetail'
                    ).str_indice[fields[0]['Home/Visitante'][0]]

                    fields[0]['Home/Visitante'][1] = django_apps.get_model(
                        'admin_juego',
                        'encuentrosdetail'
                    ).str_indice[fields[0]['Home/Visitante'][1]]

                    equipos[str(nombre.equipos_temporadas)] = fields

            if equipos:
                json['object']['fields_related']['ModalidadJuego'] = equipos

            if objecto.json['attr']['fields'].get('updated_at_logros'):

                ref_relateds = SessionsDetail.objects.filter(
                    ref_related=objecto.ref,
                    updated_at__range=[
                        datetime.datetime.strptime(
                            objecto.json['attr']['fields']['updated_at_logros'][0], FORMAT_STR_DATE_3
                        ) + datetime.timedelta(seconds=1),
                        datetime.datetime.strptime(
                            objecto.json['attr']['fields']['updated_at_logros'][1], FORMAT_STR_DATE_3
                        ) + datetime.timedelta(seconds=1),
                    ]
                ).filter(
                    Q(ref__startswith='admin_juego.jugadas') |
                    Q(ref__startswith='admin_juego.encuentrosmodalidades'),
                )

                logros = {}
                model = apuesta

                for refr in ref_relateds.order_by('updated_at'):
                    if refr.json['process'] == 'update':
                        if refr.ref.startswith('admin_juego.jugadas'):
                            model = apuesta
                        else:
                            model = SorteoModalidades
                        fields = get_fields_basic_update(
                            model, refr.json['attr'])
                        if fields:
                            logros[refr.json['object']] = fields

                if logros:
                    json['object']['fields_related']['Logros'] = logros

        return json


class AdminResultadoProcess(object):

    def process_resultados(self, objecto):
        model = Resultados
        json = {}
        json['object'] = {}
        json['object']['fields'] = []
        json['object']['fields_related'] = {}
        json['process'] = objecto.json.get('process')

        if objecto.json.get('process') == 'create':
            # Generic Part
            json['object']['fields'] = get_fields_basic_create(
                model, objecto.json['attr'])

        elif objecto.json.get('process') == 'update':
            # Generic Part
            json['object']['fields'] = get_fields_basic_update(
                model, objecto.json['attr'])

            # Custom Part
            ref_relateds = SessionsDetail.objects.filter(
                ref_related=objecto.ref,
                ref__startswith='admin_resultados.anotacionesdetail',
                updated_at__range=[objecto.updated_at,
                                   objecto.updated_at + datetime.timedelta(seconds=30)]
            )

            resultados = {}
            model = AnotacionesDetail

            for refr in ref_relateds:
                if refr.json['process'] == 'update':
                    fields = get_fields_basic_update(model, refr.json['attr'])
                    if fields:
                        resultados[refr.json['object']] = fields

            # Custom Part
            ref_relateds = list(SessionsDetail.objects.filter(
                ref_related=objecto.ref,
                ref__startswith='admin_resultados.resultadosrestric',
                updated_at__range=[objecto.updated_at,
                                   objecto.updated_at + datetime.timedelta(seconds=30)]
            ))
            if ref_relateds:
                resultados['Exclusiónes'] = []
                for refr in ref_relateds:
                    if refr.json['process'] == 'delete':
                        resultados['Exclusiónes'].append(
                            {refr.json['object']: ['Agregada', 'Eliminada']}
                        )
                    else:
                        resultados['Exclusiónes'].append(
                            {refr.json['object']: ['', 'Agregada'], }
                        )

            if resultados:
                json['object']['fields_related']['Resultados'] = resultados
            else:
                json['object']['fields_related']['Resultados'] = {
                    'Se reprocesaron resultados': ''
                }

        return json


class AdminComercializacionProcess(object):

    def process_factorriesgo(self, objecto):
        model = FactorRiesgo

        json = {}
        json['object'] = {}
        json['object']['fields'] = []
        json['object']['fields_related'] = {}
        json['process'] = objecto.json.get('process')

        fields = []
        attr = objecto.json['attr']
        attr['fields'].pop('updated_at', None)
        for field in attr['fields']:
            json_interno = {}
            if field == 'factores':
                value = []
                if objecto.json.get('process') == 'create':
                    value.append(self.humanize_factor_riesgo(attr['fields'][field]))
                else:
                    for dic in attr['fields'][field]:
                        value.append(self.humanize_factor_riesgo(dic))
            else:
                value = attr['fields'][field]
            json_interno[get_verbose_name_to_field(model, field)] = value
            fields.append(json_interno)
        json['object']['fields'] = fields

        return json

    def process_permissionssalesrestrictions(self, objecto):
        model = PermissionsSalesRestrictions

        json = {}
        json['object'] = {}
        json['object']['fields'] = []
        json['object']['fields_related'] = {}
        json['process'] = objecto.json.get('process')

        if objecto.json.get('process') == 'create':
            # Generic Part
            json['object']['fields'] = get_fields_basic_create(
                model, objecto.json['attr'])

        elif objecto.json.get('process') == 'update':
            # Generic Part
            fields = []
            attr = objecto.json['attr']
            attr['fields'].pop('updated_at', None)
            for field in attr['fields']:
                json_interno = {}
                if field == 'restrictions':
                    value = []
                    for dic in attr['fields'][field]:
                        value.append(
                            self.humanize_permissionssalesrestrictions(dic))
                else:
                    value = attr['fields'][field]
                json_interno[get_verbose_name_to_field(model, field)] = value
                fields.append(json_interno)
            json['object']['fields'] = fields

        return json

    def humanize_factor_riesgo(self, arrays):
        strs = '<table class="table">'
        if arrays:
            arrays = arrays.replace('Decimal(', '')
            arrays = arrays.replace(')', '')
            arrays = ast.literal_eval(arrays)
            for i, array in enumerate(arrays):
                strs += '<tr><td>Rango {0}: [{1},{2}] Factor {3}: {4}</td></tr>'.format(
                    i + 1, array[0], array[1], i + 1, array[2]
                )
        strs += '</table>'
        return strs

    def humanize_permissionssalesrestrictions(self, dic):
        dic = dic.replace('\'', '\"').replace(' ', '')
        dic = JSON.loads(dic)
        strs = '<table class="table">'
        for key in dic.keys():
            modalidad = ModalidadJuego.objects.get(pk=key)
            values = ''
            for value in dic[key]:
                modalidad = ModalidadJuego.objects.get(pk=value)
                values += '({0}) '.format(modalidad.modalidad)

            strs += '<tr><td>{0}: {1}</td></tr>'.format(
                modalidad.modalidad, values)
        strs += '</table>'
        return strs


class ProcessModelGeneric(object):

    def process(self, objecto):
        model = django_apps.get_model(objecto.get_app(), objecto.get_model())

        json = {}
        json['object'] = {}
        json['object']['fields'] = []
        json['object']['fields_related'] = {}
        json['process'] = objecto.json.get('process')

        if objecto.json.get('process') == 'create':
            # Generic Part
            json['object']['fields'] = get_fields_basic_create(
                model, objecto.json['attr'])

        elif objecto.json.get('process') == 'update':
            # Generic Part
            json['object']['fields'] = get_fields_basic_update(
                model, objecto.json['attr'])

        return json


def get_fields_basic_create(model, attr):
    """
    Humaniza los campos relacionados al proceso de creacion
    """
    fields = []
    attr['fields'].pop('updated_at', None)
    attr['fields'].pop('created_at', None)
    for field in attr['fields']:
        json_interno = {}
        json_interno[get_verbose_name_to_field(model, field)] = attr[
            'fields'][field]
        fields.append(json_interno)

    attr['foreign'].pop('updated_at', None)
    attr['foreign'].pop('created_at', None)
    for field in attr['foreign']:
        json_interno = {}
        json_interno[
            get_verbose_name_to_field(
                model, field)] = list(
            attr['foreign'][field].values())[0]
        fields.append(json_interno)
    return fields


def get_fields_basic_update(model, attr):
    """
    Humaniza los campos relacionados al proceso de actualizacion
    """
    fields = []
    attr['fields'].pop('updated_at', None)
    for field in attr['fields']:
        json_interno = {}
        json_interno[get_verbose_name_to_field(model, field)] = attr[
            'fields'][field]
        fields.append(json_interno)

    attr['foreign'].pop('updated_at', None)
    for field in attr['foreign']:
        json_interno = {}
        json_interno[get_verbose_name_to_field(model, field)] = [
            list(attr['foreign'][field][0].values())[0],
            list(attr['foreign'][field][1].values())[0]
        ]
        fields.append(json_interno)

    for field in attr['m2m']:
        json_interno = {}
        json_interno[get_verbose_name_to_field(model, field)] = [
            humanize_list(list(attr['m2m'][field][0].values())),
            humanize_list(list(attr['m2m'][field][1].values()))
        ]
        fields.append(json_interno)
    return fields


def humanize_list(lista):
    st = ''
    for l in lista:
        st += '({0}) '.format(l)
    return st


def get_verbose_name_to_field(model, field_name):
    try:
        return model._meta.get_field(
            field_name
        ).verbose_name.replace('(*)', '')
    except Exception:
        return field_name
