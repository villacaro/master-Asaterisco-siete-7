# -*- coding: utf-8 -*-


def run(*args):
    """
         >> python manage.py runscript sync_consolidado --script-args=2281 2016-01-15

         --script-args:
            Id taquilla
            Fecha
    """
    if len(args) != 2:
        print('Debe indicar los parametros (id_taquilla y fecha): --script-args=2281 2016-01-15')
        return

    from admin_comercializacion.models import Taquillas
    from admin_datamart.models import Consolidado, Hecho5_ComisionesCadena
    from admin_datamart.task import ObtenerPorcentaje
    from django.utils.timezone import now

    fecha = now().strptime(args[1], '%Y-%m-%d')

    taquilla = Taquillas.objects.get(pk=args[0])
    agencia = taquilla.get_origen()
    distribuidor = agencia.get_origen()
    banca = distribuidor.get_origen()
    bloque = banca.get_origen()
    operadora = bloque.get_origen()

    resumen = Hecho5_ComisionesCadena.objects.get(
        tiempo__fecha=fecha,
        comercializacion=taquilla.get_dimension_arco_comercializadora(),
    )

    kwargs = {
        'id_lista': 0,
        'id_tipo_lista': 0,
        'id_prestador_servicio': 0,
        'id_comercializador': bloque.pk,
        'id_banca': banca.pk,
        'id_distribuidor': distribuidor.pk,
        'id_agencia': agencia.pk,
        'id_taquilla': taquilla.pk,
        'id_operador': operadora.pk,

        'nporcentaje_comision_com': ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=bloque,
            fecha=fecha
        ),
        'nporcentaje_participacion_com': ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=bloque,
            fecha=fecha
        ),
        'nporcentaje_regalia_com': ObtenerPorcentaje(
            codename='porcentaje_regalia',
            cadena=bloque,
            fecha=fecha
        ),
        'nporcentaje_comision_ban': ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=banca,
            fecha=fecha
        ),
        'nporcentaje_participacion_ban': ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=banca,
            fecha=fecha
        ),
        'nporcentaje_regalia_ban': ObtenerPorcentaje(
            codename='porcentaje_regalia',
            cadena=banca,
            fecha=fecha
        ),
        'nporcentaje_comision_dis': ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=distribuidor,
            fecha=fecha
        ),
        'nporcentaje_participacion_dis': ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=distribuidor,
            fecha=fecha
        ),
        'nporcentaje_regalia_dis': ObtenerPorcentaje(
            codename='porcentaje_regalia',
            cadena=distribuidor,
            fecha=fecha
        ),
        'nporcentaje_comision_agc': ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=agencia,
            fecha=fecha
        ),

        'mmonto_venta': resumen.venta,
        'mmonto_venta_externa': 0,
        'mmonto_venta_ganador': 0,
        'mmonto_premios': resumen.premio,

        'tserial_ifa': '',

        'id_perfil_pago_premios': 0,
    }

    kwargs['mmonto_comision_com'] = kwargs['mmonto_venta'] * kwargs['nporcentaje_comision_com']
    kwargs['mmonto_regalia_com'] = kwargs['mmonto_venta'] * kwargs['nporcentaje_regalia_com']
    kwargs['mmonto_comision_ban'] = kwargs['mmonto_venta'] * kwargs['nporcentaje_comision_ban']
    kwargs['mmonto_regalia_ban'] = kwargs['mmonto_venta'] * kwargs['nporcentaje_regalia_ban']
    kwargs['mmonto_comision_dis'] = kwargs['mmonto_venta'] * kwargs['nporcentaje_comision_dis']
    kwargs['mmonto_regalia_dis'] = kwargs['mmonto_venta'] * kwargs['nporcentaje_regalia_dis']
    kwargs['mmonto_comision_agc'] = kwargs['mmonto_venta'] * kwargs['nporcentaje_comision_agc']

    mmonto_regalia_agc = kwargs['mmonto_venta'] * ObtenerPorcentaje(
        codename='porcentaje_regalia',
        cadena=agencia,
        fecha=fecha
    )

    kwargs['msaldo_bruto_com'] = (
        kwargs['mmonto_venta'] - kwargs['mmonto_premios'] -
        kwargs['mmonto_comision_com'] - kwargs['mmonto_regalia_com']
    )

    kwargs['msaldo_bruto_ban'] = (
        kwargs['mmonto_venta'] - kwargs['mmonto_premios'] -
        kwargs['mmonto_comision_ban'] - kwargs['mmonto_regalia_ban']
    )

    kwargs['msaldo_bruto_dis'] = (
        kwargs['mmonto_venta'] - kwargs['mmonto_premios'] -
        kwargs['mmonto_comision_dis'] - kwargs['mmonto_regalia_dis']
    )

    saldo_bruto_ag = (
        kwargs['mmonto_venta'] - kwargs['mmonto_premios'] -
        kwargs['mmonto_comision_agc'] - mmonto_regalia_agc
    )

    kwargs['msaldo_dis'] = kwargs['msaldo_bruto_dis'] * kwargs['nporcentaje_participacion_dis']
    kwargs['msaldo_ban'] = kwargs['msaldo_bruto_ban'] * kwargs['nporcentaje_participacion_ban']
    kwargs['msaldo_com'] = kwargs['msaldo_bruto_com'] * kwargs['nporcentaje_participacion_com']

    kwargs['msaldo_oper'] = kwargs['msaldo_bruto_com'] - kwargs['msaldo_com'] + kwargs['mmonto_regalia_com']

    kwargs['msaldo_agc'] = saldo_bruto_ag * ObtenerPorcentaje(
        codename='porcentaje_participacion',
        cadena=agencia,
        fecha=fecha
    )

    kwargs['msaldo_oper_ban'] = (kwargs['msaldo_bruto_ban'] - kwargs['msaldo_ban']) + kwargs['mmonto_regalia_ban']
    kwargs['msaldo_oper_dis'] = (kwargs['msaldo_bruto_dis'] - kwargs['msaldo_dis']) + kwargs['mmonto_regalia_dis']
    kwargs['msaldo_oper_cm'] = (kwargs['msaldo_bruto_com'] - kwargs['msaldo_com']) + kwargs['mmonto_regalia_com']
    kwargs['msaldo_cm'] = kwargs['msaldo_bruto_com'] * kwargs['nporcentaje_participacion_com']

    kwargs['dfecha'] = fecha

    Consolidado.objects.update_or_create(
        id_sorteo=fecha.strftime('%Y%m%d'),
        defaults=kwargs
    )
