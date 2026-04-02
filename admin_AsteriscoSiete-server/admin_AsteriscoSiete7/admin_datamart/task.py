# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal

from admin_apuestas.models import Tickets
from admin_asterisco7.settings import CACHES_CONF_TIME, FORMAT_STR_DATE_REPORTS, REDIS_DB
from admin_comercializacion.models import Agencias, Bancas, Bloques, Distribuidores, Porcentajes, Taquillas
from admin_datamart.models import (
    Consolidado, DimensionArcoComercializacion, DimensionComercializacion, DimensionJuegos, DimensionJuegosNew,
    DimensionTiempo, Hecho1_VentasCadenasJuegos, Hecho2_VentasCadenas, Hecho2_VentasCadenasLinea,
    Hecho5_ComisionesCadena, Hecho8_VentasMonitorLinea, Hecho9_VentasSaldosCadena,
)
from admin_finanzas.models import Comercializadora, Movimiento
from admin_lib.util_fechas import strFecha
from admin_lib.util_funtions import get_agencias_alquiler_by_frecuencia, get_decimal_is_not_none
from admin_lib.util_task import AsyncGestionOperationalError
try:
    from celery.registry import tasks
except ImportError:
    class _NoOpTaskRegistry:
        def register(self, *args, **kwargs):
            pass
    tasks = _NoOpTaskRegistry()
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import now


class InitDimensiones(object):
    """
    Inicializa las dimensiones
    """

    def get_dimension_tiempo(self, fecha):
        return DimensionTiempo.get_dimension_tiempo(fecha)

    def get_dimension_comercializacion(self, taquilla):
        dimension = cache.get(
            'get_dimension_comercializacion_{0}'.format(
                taquilla.pk))
        if not dimension:
            try:
                dimension = DimensionComercializacion.objects.get(
                    taquilla_id=taquilla.pk
                )
                # el campo taquilla_id esta indexado, esto mejora
                # su busqueda, en caso de no encontrarlo
                # si se procede a crearlo, la creacion seria una sola vez
            except DimensionComercializacion.DoesNotExist:
                dimension = DimensionComercializacion.objects.get_or_create(
                    taquilla_id=taquilla.pk,
                    agencia_id=taquilla.agencia_id,
                    distribuidor_id=taquilla.agencia.distribuidores_id,
                    banca_id=taquilla.agencia.distribuidores.banca_id,
                    bloque_id=taquilla.agencia.distribuidores.banca.bloque_id,
                    operadora_id=taquilla.agencia.distribuidores.banca.bloque.operadora_id
                )[0]
            cache.set(
                'get_dimension_comercializacion_{0}'.format(taquilla.pk),
                dimension,
                0,
            )
        return dimension

    def get_hecho2_ventas_cadenas(self, fecha, taquilla):
        return Hecho2_VentasCadenas.objects.get_or_create(
            tiempo=self.get_dimension_tiempo(fecha),
            comercializacion=self.get_dimension_comercializacion(taquilla)
        )[0]

    def get_hecho2_ventas_cadenas_linea(self, fecha, taquilla):
        return Hecho2_VentasCadenasLinea.objects.get_or_create(
            tiempo=self.get_dimension_tiempo(fecha),
            comercializacion=self.get_dimension_comercializacion(taquilla)
        )[0]

    def get_dimension_juegos(self, jugada):
        dimension = cache.get('get_dimension_juegos_{0}'.format(jugada.pk))
        if not dimension:
            dimension = DimensionJuegos.objects.get_or_create(
                pertenece=jugada.get_pertenece(),
                condicion_id=jugada.condicion_id,
                modalidad_id=jugada.condicion.modalidad_id,
                encuentros_modalidad_id=jugada.encuentros_modalidad_id,
                encuentro_id=jugada.encuentros_modalidad.encuentro_id,
                jornada_id=jugada.encuentros_modalidad.encuentro.jornada_id,
                temporada_id=jugada.encuentros_modalidad.encuentro.jornada.temporadas_id,
                torneo_id=jugada.encuentros_modalidad.encuentro.jornada.temporadas.torneo_id,
                deporte_id=jugada.encuentros_modalidad.encuentro
                .jornada.temporadas.torneo.deporte_id
            )[0]
            cache.set(
                'get_dimension_juegos_{0}'.format(jugada.pk),
                dimension,
                CACHES_CONF_TIME['registros_db']['workers']
            )
        return dimension

    def get_dimension_juegos_new(self, jugada):
        dimension = cache.get('get_dimension_juegos_new_{0}'.format(jugada.pk))
        if not dimension:
            dimension = DimensionJuegosNew.objects.get_or_create(
                jugador_id=jugada.detalle_encuentro.jugador_id if jugada.detalle_encuentro else None,
                grupojuego_id=jugada.encuentros_modalidad.encuentro.grupo_id,
                pertenece_id=jugada.get_pertenece_id(),
                equipo_id=jugada.detalle_encuentro.equipos_temporadas.equipo_id if jugada.detalle_encuentro else None,
                condicion_id=jugada.condicion_id,
                modalidad_id=jugada.condicion.modalidad_id,
                grupo_id=jugada.encuentros_modalidad.deporte_grupo.grupo_id,
                encuentros_modalidad_id=jugada.encuentros_modalidad_id,
                encuentro_id=jugada.encuentros_modalidad.encuentro_id,
                jornada_id=jugada.encuentros_modalidad.encuentro.jornada_id,
                temporada_id=jugada.encuentros_modalidad.encuentro.jornada.temporadas_id,
                torneo_id=jugada.encuentros_modalidad.encuentro.jornada.temporadas.torneo_id,
                deporte_id=jugada.encuentros_modalidad.encuentro
                .jornada.temporadas.torneo.deporte_id,
                sistema_id=jugada.encuentros_modalidad.encuentro.jornada.sistema_id,
            )[0]
            cache.set(
                'get_dimension_juegos_new_{0}'.format(jugada.pk),
                dimension,
                CACHES_CONF_TIME['registros_db']['workers']
            )
        return dimension

    def get_hecho8_ventas_monitor_linea(self, fecha, taquilla, jugada):
        return Hecho8_VentasMonitorLinea.objects.get_or_create(
            tiempo=self.get_dimension_tiempo(fecha),
            comercializacion=self.get_dimension_comercializacion(taquilla),
            juegos=self.get_dimension_juegos_new(jugada)
        )[0]

    def get_hecho9_ventas_saldo_cadena(self, fecha, comercializacion):
        return Hecho9_VentasSaldosCadena.objects.get_or_create(
            tiempo=self.get_dimension_tiempo(fecha),
            comercializacion=comercializacion,
        )[0]

    def get_hecho1_ventas_cadenas_juegos(self, fecha, taquilla, jugada):
        return Hecho1_VentasCadenasJuegos.objects.get_or_create(
            tiempo=self.get_dimension_tiempo(fecha),
            comercializacion=self.get_dimension_comercializacion(taquilla),
            juegos=self.get_dimension_juegos(jugada),
        )[0]

    def get_dimension_arco_comercializacion(
            self, taquilla=None, agencia=None,
            distribuidor=None, banca=None, bloque=None, operadora=None):
        return DimensionArcoComercializacion.objects.get_or_create(
            operadora_id=operadora,
            bloque_id=bloque,
            banca_id=banca,
            distribuidor_id=distribuidor,
            agencia_id=agencia,
            taquilla_id=taquilla
        )[0]


def ObtenerPorcentaje(codename, cadena, fecha):

    kwargs = {
        'tipo__codename': codename
    }
    kwargs[cadena.prefix_filter + '_id'] = cadena.pk
    porcentaje = Porcentajes.objects.filter(
        **kwargs
    )

    if porcentaje.count() == 0:
        porcentaje = Decimal(str('0.00'))
    elif porcentaje.count() == 1:
        porcentaje = porcentaje[0].porcentaje_ganancia
    else:
        porcentaje.filter(
            fecha_inicio__gte=fecha,
            fecha_fin__lte=fecha
        )
        if porcentaje.count() == 1:
            # Si el porcentaje tiene relacion con el padre
            if porcentaje[0].relacion:
                porcentaje = porcentaje[0].porcentaje_ganancia
            elif porcentaje[0].tipo.codename == "porcentaje_comision":
                porcentaje = Decimal(str('-1'))
        else:
            porcentaje = porcentaje.filter(
                fecha_fin=None
            )
            if porcentaje.count() == 1:
                if porcentaje[0].relacion:
                    porcentaje = porcentaje[0].porcentaje_ganancia
                elif porcentaje[0].tipo.codename == "porcentaje_comision":
                    porcentaje = Decimal(str('-1'))
            else:
                porcentaje = Decimal(str('0.00'))
    return porcentaje


class AsyncGestion_ProcessPorcentajesCadena(AsyncGestionOperationalError):
    name = 'AsyncGestion_ProcessPorcentajesCadena'
    queue = 'porcentajes_cadena'
    key = None

    # Expiracion de 1 hora
    key_expire = 3600

    def get_key(self, **kwargs):
        if self.key is None:
            self.key = 'key_delay_{0}_{1}_{2}'.format(
                kwargs.get('fecha'),
                kwargs.get('key'),
                kwargs.get(kwargs.get('key'))
            )
        return self.key

    def start_run(self, *args, **kwargs):

        procesar = REDIS_DB.get(self.get_key(**kwargs))
        if not procesar:
            procesar = 0
        else:
            procesar = int(procesar)

        if procesar < 2:
            procesar += 1
            REDIS_DB.set(self.get_key(**kwargs), procesar, self.key_expire)
            self.delay(*args, **kwargs)

    def run_try(self, *args, **kwargs):
        self.mensaje = []
        self.padlocks = {}

        self.dimensiones = InitDimensiones()
        self.fecha = now().strptime(kwargs.get('fecha'), FORMAT_STR_DATE_REPORTS)

        procesar = REDIS_DB.get(self.get_key(**kwargs))
        if not procesar:
            procesar = 1
        else:
            procesar = int(procesar)
        procesar -= 1
        REDIS_DB.set(self.get_key(**kwargs), procesar, self.key_expire)

        prefix_filter = None
        pk = None
        no_recursive = True

        if 'taquilla_id' in kwargs:
            taquilla_id = kwargs.pop('taquilla_id')
            try:
                taquilla = Taquillas.objects.only('pk', 'agencia').get(
                    pk=taquilla_id
                )
            except Taquillas.DoesNotExist:
                taquilla = Comercializadora.objects.get(taquilla_id=taquilla_id).get_object()

            self.procesar_taquilla(taquilla)

            kwargs['key'] = 'agencia_id'
            kwargs['agencia_id'] = taquilla.agencia_id
            self.start_run(*args, **kwargs)

        elif 'agencia_id' in kwargs:
            agencia_id = kwargs.pop('agencia_id')
            try:
                agencia = Agencias.objects.only('pk', 'distribuidores').get(
                    pk=agencia_id
                )
            except Agencias.DoesNotExist:
                agencia = Comercializadora.objects.get(agencia_id=agencia_id).get_object()

            self.procesar_agencia(agencia)

            kwargs['key'] = 'distribuidor_id'
            kwargs['distribuidor_id'] = agencia.distribuidores_id
            self.start_run(*args, **kwargs)

            prefix_filter = agencia.prefix_filter
            pk = agencia.get_comercializadora().pk

        elif 'distribuidor_id' in kwargs:
            distribuidor_id = kwargs.pop('distribuidor_id')
            try:
                distribuidor = Distribuidores.objects.only('pk', 'banca').get(
                    pk=distribuidor_id
                )
            except Distribuidores.DoesNotExist:
                distribuidor = Comercializadora.objects.get(distribuidor_id=distribuidor_id).get_object()
            self.procesar_distribuidor(distribuidor)

            kwargs['key'] = 'banca_id'
            kwargs['banca_id'] = distribuidor.banca_id
            self.start_run(*args, **kwargs)

            prefix_filter = distribuidor.prefix_filter
            pk = distribuidor.get_comercializadora().pk

        elif 'banca_id' in kwargs:
            banca_id = kwargs.pop('banca_id')
            try:
                banca = Bancas.objects.only('pk', 'bloque').get(
                    pk=banca_id
                )
            except Bancas.DoesNotExist:
                banca = Comercializadora.objects.get(banca_id=banca_id).get_object()

            self.procesar_banca(banca)

            kwargs['key'] = 'bloque_id'
            kwargs['bloque_id'] = banca.bloque_id
            self.start_run(*args, **kwargs)

            prefix_filter = banca.prefix_filter
            pk = banca.get_comercializadora().pk

        elif 'bloque_id' in kwargs:
            bloque_id = kwargs.pop('bloque_id')
            try:
                bloque = Bloques.objects.only('pk').get(
                    pk=bloque_id
                )
            except Bloques.DoesNotExist:
                bloque = Comercializadora.objects.get(bloque_id=bloque_id)

            self.procesar_bloque(bloque)

            prefix_filter = bloque.prefix_filter
            pk = bloque.get_comercializadora().pk
            no_recursive = False

        if prefix_filter and pk:
            self.check_finish(prefix_filter, pk, no_recursive)

        return self.mensaje

    def check_finish(self, prefix, pk, no_recursive=True):
        """
        solo si viene la bandera check_finish activa
        esta tarea se ejecuta en primer plano la tarea AsyncCheckComer_tickets
        para procesar hecho9 e importar saldos en resumen administrativo
        """
        tarea = AsyncCheckComer_tickets()
        tarea.delay(
            *(),
            **{
                'tipo': prefix,
                'id_comer': pk,
                'fecha': self.fecha.strftime(FORMAT_STR_DATE_REPORTS),
                'start_delay': True,
                'no_recursive': no_recursive,
            }
        )

    def open_padlock_up(self, _object):
        """
        Obtenemos la llave desde redis
        """
        key = '{0}_{1}_{2}'.format(
            'porcentajes_cadena',
            _object.prefix_filter,
            _object.pk)
        self.padlock_up = REDIS_DB.lock(key)

    def acquire_padlock_up(self):
        try:
            # esto hace que si hay un error, la clase origen intenta hacer un
            # release
            self.padlocks[self.padlock_up.name] = self.padlock_up
            self.padlock_up.acquire()
        except Exception:
            pass

    def release_padlock_up(self):
        try:
            del self.padlocks[self.padlock_up.name]
            self.padlock_up.release()
        except Exception:
            pass

    def open_padlock_down(self, _object):
        """
        Obtenemos la llave desde redis
        """
        key = '{0}_{1}_{2}'.format(
            'porcentajes_cadena',
            _object.prefix_filter,
            _object.pk)
        self.padlock_down = REDIS_DB.lock(key)

    def acquire_padlock_down(self):
        try:
            self.padlocks[self.padlock_down.name] = self.padlock_down
            self.padlock_down.acquire()
        except Exception:
            pass

    def release_padlock_down(self):
        try:
            del self.padlocks[self.padlock_down.name]
            self.padlock_down.release()
        except Exception:
            pass

    def procesar_taquilla(self, taquilla):

        # ===================================
        self.open_padlock_down(taquilla)
        self.acquire_padlock_down()

        self.open_padlock_up(taquilla.agencia)
        self.acquire_padlock_up()
        # ===================================

        # llenado del hecho 5
        self.val_dimension_tiempo = self.dimensiones.get_dimension_tiempo(
            self.fecha)
        val_dimension_comercializacion = taquilla.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        self.hecho2 = self.dimensiones.get_hecho2_ventas_cadenas(
            self.fecha, taquilla)

        hecho5.venta = self.hecho2.monto_total
        hecho5.premio = self.hecho2.monto_premios
        hecho5.saldo_bruto = hecho5.venta - hecho5.premio
        hecho5.saldo_oper = hecho5.saldo_bruto

        hecho5.save(
            update_fields=[
                'venta',
                'premio',
                'saldo_bruto',
                'saldo_oper'])

        # llenado del Consolidado
        agencia = taquilla.get_origen()
        distribuidor = agencia.get_origen()
        banca = distribuidor.get_origen()
        bloque = banca.get_origen()
        operadora = bloque.get_origen()

        kwargs = {
            'id_lista': 0,
            'id_tipo_lista': 0,
            'id_prestador_servicio': 0,
            'id_operador': operadora.pk,
            'id_comercializador': bloque.pk,
            'id_banca': banca.pk,
            'id_distribuidor': distribuidor.pk,
            'id_agencia': agencia.pk,

            'nporcentaje_comision_com': ObtenerPorcentaje(
                codename='porcentaje_comision',
                cadena=bloque,
                fecha=self.fecha
            ),
            'nporcentaje_participacion_com': ObtenerPorcentaje(
                codename='porcentaje_participacion',
                cadena=bloque,
                fecha=self.fecha
            ),
            'nporcentaje_regalia_com': ObtenerPorcentaje(
                codename='porcentaje_regalia',
                cadena=bloque,
                fecha=self.fecha
            ),
            'nporcentaje_comision_ban': ObtenerPorcentaje(
                codename='porcentaje_comision',
                cadena=banca,
                fecha=self.fecha
            ),
            'nporcentaje_participacion_ban': ObtenerPorcentaje(
                codename='porcentaje_participacion',
                cadena=banca,
                fecha=self.fecha
            ),
            'nporcentaje_regalia_ban': ObtenerPorcentaje(
                codename='porcentaje_regalia',
                cadena=banca,
                fecha=self.fecha
            ),
            'nporcentaje_comision_dis': ObtenerPorcentaje(
                codename='porcentaje_comision',
                cadena=distribuidor,
                fecha=self.fecha
            ),
            'nporcentaje_participacion_dis': ObtenerPorcentaje(
                codename='porcentaje_participacion',
                cadena=distribuidor,
                fecha=self.fecha
            ),
            'nporcentaje_regalia_dis': ObtenerPorcentaje(
                codename='porcentaje_regalia',
                cadena=distribuidor,
                fecha=self.fecha
            ),
            'nporcentaje_comision_agc': ObtenerPorcentaje(
                codename='porcentaje_comision',
                cadena=agencia,
                fecha=self.fecha
            ),

            'mmonto_venta': hecho5.venta,
            'mmonto_venta_externa': 0,
            'mmonto_venta_ganador': 0,
            'mmonto_premios': hecho5.premio,

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
            fecha=self.fecha
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

        porcentaje_agc = ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=agencia,
            fecha=self.fecha
        )

        if porcentaje_agc == 0:
            porcentaje_agc = 1

        kwargs['msaldo_agc'] = saldo_bruto_ag * porcentaje_agc

        kwargs['msaldo_oper_ban'] = (kwargs['msaldo_bruto_ban'] - kwargs['msaldo_ban']) + kwargs['mmonto_regalia_ban']
        kwargs['msaldo_oper_dis'] = (kwargs['msaldo_bruto_dis'] - kwargs['msaldo_dis']) + kwargs['mmonto_regalia_dis']
        kwargs['msaldo_oper_cm'] = (kwargs['msaldo_bruto_com'] - kwargs['msaldo_com']) + kwargs['mmonto_regalia_com']
        kwargs['msaldo_cm'] = kwargs['msaldo_bruto_com'] * kwargs['nporcentaje_participacion_com']

        kwargs['dfecha'] = self.fecha

        Consolidado.objects.update_or_create(
            id_sorteo=self.fecha.strftime('%Y%m%d'),
            id_taquilla=taquilla.pk,
            defaults=kwargs
        )

        # ===================================
        self.release_padlock_up()
        self.release_padlock_down()
        # ===================================

    def procesar_agencia(self, agencia):

        # ===================================
        self.open_padlock_down(agencia)
        self.acquire_padlock_down()

        self.open_padlock_up(agencia.distribuidores)
        self.acquire_padlock_up()
        # ===================================

        self.val_dimension_tiempo = self.dimensiones.get_dimension_tiempo(
            self.fecha)
        val_dimension_comercializacion = agencia.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__taquilla_id__isnull=False,
            comercializacion__agencia_id=agencia.pk,
            tiempo=self.val_dimension_tiempo
        )
        sum_down = hecho5.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('participacion'),
            Sum('regalia'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        hecho5.venta = sum_down['venta__sum']
        hecho5.premio = sum_down['premio__sum']

        hecho5.comision_down = sum_down['comision__sum']
        hecho5.participacion_down = sum_down['participacion__sum']
        hecho5.regalia_down = sum_down['regalia__sum']

        porc_comision = ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=agencia,
            fecha=self.fecha
        )
        # Cuando es un porcentaje negativo es por que no posee relación
        if porc_comision == Decimal(str('-1')):
            hecho5.comision = hecho5.comision_down
        else:
            hecho5.comision = hecho5.venta * porc_comision

        hecho5.regalia = hecho5.venta * ObtenerPorcentaje(
            codename='porcentaje_regalia',
            cadena=agencia,
            fecha=self.fecha
        )

        hecho5.saldo_bruto = hecho5.venta - \
            (hecho5.premio + hecho5.comision + hecho5.regalia)

        hecho5.participacion = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=agencia,
            fecha=self.fecha
        )

        hecho5.saldo_comer = hecho5.participacion
        hecho5.saldo_oper = hecho5.saldo_bruto - hecho5.saldo_comer + hecho5.regalia

        hecho5.queda_ref = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_queda',
            cadena=agencia,
            fecha=self.fecha
        )

        hecho5.save()

        # ===================================
        self.release_padlock_up()
        self.release_padlock_down()
        # ===================================

    def procesar_distribuidor(self, distribuidor):

        # ===================================
        self.open_padlock_down(distribuidor)
        self.acquire_padlock_down()

        self.open_padlock_up(distribuidor.banca)
        self.acquire_padlock_up()
        # ===================================

        self.val_dimension_tiempo = self.dimensiones.get_dimension_tiempo(
            self.fecha)
        val_dimension_comercializacion = distribuidor.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__agencia_id__isnull=False,
            comercializacion__distribuidor_id=distribuidor.pk,
            tiempo=self.val_dimension_tiempo
        )
        sum_down = hecho5.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('participacion'),
            Sum('regalia'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        hecho5.venta = sum_down['venta__sum']
        hecho5.premio = sum_down['premio__sum']

        hecho5.comision_down = sum_down['comision__sum']
        hecho5.participacion_down = sum_down['participacion__sum']
        hecho5.regalia_down = sum_down['regalia__sum']

        hecho5.regalia = hecho5.venta * ObtenerPorcentaje(
            codename='porcentaje_regalia',
            cadena=distribuidor,
            fecha=self.fecha
        )

        porc_comision = ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=distribuidor,
            fecha=self.fecha
        )

        # Cuando es un porcentaje negativo es por que no posee relación
        if porc_comision == Decimal(str('-1')):
            hecho5.comision = hecho5.comision_down
        else:
            hecho5.comision = hecho5.venta * porc_comision

        hecho5.saldo_bruto = hecho5.venta - \
            (hecho5.premio + hecho5.comision + hecho5.regalia)

        hecho5.participacion = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=distribuidor,
            fecha=self.fecha
        )

        hecho5.saldo_comer = hecho5.participacion
        hecho5.saldo_oper = hecho5.saldo_bruto - hecho5.saldo_comer + hecho5.regalia

        hecho5.queda_ref = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_queda',
            cadena=distribuidor,
            fecha=self.fecha
        )

        hecho5.save()

        # ===================================
        self.release_padlock_up()
        self.release_padlock_down()
        # ===================================

    def procesar_banca(self, banca):

        # ===================================
        self.open_padlock_down(banca)
        self.acquire_padlock_down()

        self.open_padlock_up(banca.bloque)
        self.acquire_padlock_up()
        # ===================================

        self.val_dimension_tiempo = self.dimensiones.get_dimension_tiempo(
            self.fecha)
        val_dimension_comercializacion = banca.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__distribuidor_id__isnull=False,
            comercializacion__banca_id=banca.pk,
            tiempo=self.val_dimension_tiempo
        )
        sum_down = hecho5.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('participacion'),
            Sum('regalia'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        hecho5.venta = sum_down['venta__sum']
        hecho5.premio = sum_down['premio__sum']

        hecho5.comision_down = sum_down['comision__sum']
        hecho5.participacion_down = sum_down['participacion__sum']
        hecho5.regalia_down = sum_down['regalia__sum']

        hecho5.regalia = hecho5.venta * ObtenerPorcentaje(
            codename='porcentaje_regalia',
            cadena=banca,
            fecha=self.fecha
        )

        porc_comision = ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=banca,
            fecha=self.fecha
        )

        # Cuando es un porcentaje negativo es por que no posee relación
        if porc_comision == Decimal(str('-1')):
            hecho5.comision = hecho5.comision_down
        else:
            hecho5.comision = hecho5.venta * porc_comision

        hecho5.saldo_bruto = hecho5.venta - \
            (hecho5.premio + hecho5.comision + hecho5.regalia)

        hecho5.participacion = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=banca,
            fecha=self.fecha
        )

        hecho5.saldo_comer = hecho5.participacion
        hecho5.saldo_oper = hecho5.saldo_bruto - hecho5.saldo_comer + hecho5.regalia

        hecho5.queda_ref = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_queda',
            cadena=banca,
            fecha=self.fecha
        )

        hecho5.save()

        # ===================================
        self.release_padlock_up()
        self.release_padlock_down()
        # ===================================

    def procesar_bloque(self, bloque):

        # ===================================
        self.open_padlock_down(bloque)
        self.acquire_padlock_down()
        # ===================================

        self.val_dimension_tiempo = self.dimensiones.get_dimension_tiempo(
            self.fecha)
        val_dimension_comercializacion = bloque.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__banca_id__isnull=False,
            comercializacion__bloque_id=bloque.pk,
            tiempo=self.val_dimension_tiempo
        )

        hecho5_alquiler = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__banca_id__in=list(Bancas.objects.filter(
                bloque_id=bloque.pk,
                modelo_negocio=Bancas.modelo_negocio_codenames[
                    'codename_negocio_alquiler']
            ).values_list('pk', flat=True)),
            comercializacion__bloque_id=bloque.pk,
            tiempo=self.val_dimension_tiempo
        )

        sum_down_alquiler = hecho5_alquiler.aggregate(
            Sum('venta'),
            Sum('premio'),
        )

        sum_down = hecho5.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('participacion'),
            Sum('regalia'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        hecho5.venta = sum_down['venta__sum']
        hecho5.premio = sum_down['premio__sum']

        hecho5.comision_down = sum_down['comision__sum']
        hecho5.participacion_down = sum_down['participacion__sum']
        hecho5.regalia_down = sum_down['regalia__sum']

        venta_alquiler = get_decimal_is_not_none(
            sum_down_alquiler['venta__sum'])
        premio_alquiler = get_decimal_is_not_none(
            sum_down_alquiler['premio__sum'])

        venta_bruta = hecho5.venta - venta_alquiler
        premio_bruto = hecho5.premio - premio_alquiler

        hecho5.regalia = venta_bruta * ObtenerPorcentaje(
            codename='porcentaje_regalia',
            cadena=bloque,
            fecha=self.fecha
        )

        porc_comision = ObtenerPorcentaje(
            codename='porcentaje_comision',
            cadena=bloque,
            fecha=self.fecha
        )

        # Cuando es un porcentaje negativo es por que no posee relación
        if porc_comision == Decimal(str('-1')):
            hecho5.comision = hecho5.comision_down
        else:
            hecho5.comision = hecho5.venta * porc_comision

        hecho5.saldo_bruto = venta_bruta - \
            (premio_bruto + hecho5.comision + hecho5.regalia)

        hecho5.participacion = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=bloque,
            fecha=self.fecha
        )

        hecho5.queda_ref = hecho5.saldo_bruto * ObtenerPorcentaje(
            codename='porcentaje_queda',
            cadena=bloque,
            fecha=self.fecha
        )

        hecho5.saldo_comer = hecho5.participacion + \
            (venta_alquiler - premio_alquiler)
        hecho5.saldo_oper = hecho5.saldo_bruto - hecho5.participacion + hecho5.regalia

        hecho5.save()

        # ===================================
        self.release_padlock_down()
        # ===================================


tasks.register(AsyncGestion_ProcessPorcentajesCadena)


class AsyncGestion_add_ticket_apuesta(AsyncGestionOperationalError):
    name = 'AsyncGestion_add_ticket_apuesta'
    queue = 'reportes'

    def run_try(self, *args, **kwargs):
        self.kwargs = kwargs
        self.mensaje = []
        self.mensaje.append('Ticket {0}'.format(kwargs.get('ticket')))
        ticket = Tickets.objects.only(
            'user__taquilla',
            'fecha',
            'monto',
        ).get(pk=kwargs.get('ticket'))

        fecha = ticket.fecha.strftime(FORMAT_STR_DATE_REPORTS)
        self.mensaje.append('Vendido {0}'.format(fecha))
        self.mensaje.append('Monto {0}'.format(ticket.monto))
        dimensiones = InitDimensiones()

        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho
        # 2 es por taquilla
        key = '{0}_{1}'.format('ventas_procesadas', ticket.user.taquilla_id)
        self.padlock = REDIS_DB.lock(key)
        self.set_acquire()
        # ================================================================================================
        if not self.kwargs.get('add_hecho2'):
            hecho2 = dimensiones.get_hecho2_ventas_cadenas(
                ticket.fecha, ticket.user.taquilla)
            hecho2.add_ticket(ticket)
            self.kwargs['add_hecho2'] = True
            self.mensaje.append('Hecho 2 listo.')

        # ================================================================================================
        # Quitamos el candado
        self.set_release()
        # ================================================================================================

        kwargs = {
            'fecha': fecha,
            'taquilla_id': ticket.user.taquilla_id,
            'key': 'taquilla_id',
        }
        task = AsyncGestion_ProcessPorcentajesCadena()
        task.delay(*(), **kwargs)

        return self.mensaje


tasks.register(AsyncGestion_add_ticket_apuesta)


class AsyncGestion_add_ticket_apuesta_En_Linea(AsyncGestionOperationalError):
    name = 'AsyncGestion_add_ticket_apuesta_En_Linea'
    queue = 'reportes'

    def run_try(self, *args, **kwargs):
        self.kwargs = kwargs
        self.mensaje = []
        self.mensaje.append('Ticket {0}'.format(self.kwargs.get('ticket')))
        ticket = Tickets.get_ticket_low(pk=self.kwargs.get('ticket'))

        self.mensaje.append(
            'Vendido {0}'.format(
                ticket.fecha.strftime('%d/%m/%Y %H:%M')))
        self.mensaje.append('Monto {0}'.format(ticket.monto))
        dimensiones = InitDimensiones()
        fecha = strFecha(ticket.fecha)
        fecha = fecha.getFecha()

        # Creamos candado
        key = '{0}_{1}'.format('ventas_en_linea', ticket.user_id)
        self.padlock = REDIS_DB.lock(key)

        # Activamos candado
        self.set_acquire()

        if not self.kwargs.get('add_hecho2'):
            hecho2_linea = dimensiones.get_hecho2_ventas_cadenas_linea(
                fecha, ticket.user.taquilla)
            hecho2_linea.add_ticket(ticket)
            self.kwargs['add_hecho2'] = True
            self.mensaje.append('Hecho 2 listo.')

        ticket_items = ticket.ticketsdetail_set.only('jugada').all()
        for item in ticket_items:
            if not self.kwargs.get('add_hecho1_{0}'.format(item.pk)):
                dimensiones.get_hecho1_ventas_cadenas_juegos(
                    fecha,
                    ticket.user.taquilla,
                    item.jugada
                ).add_apuesta(item.monto)
                self.kwargs['add_hecho1_{0}'.format(item.pk)] = True

            if not self.kwargs.get('add_hecho8_{0}'.format(item.pk)):
                dimensiones.get_hecho8_ventas_monitor_linea(
                    fecha,
                    ticket.user.taquilla,
                    item.jugada,
                ).add_apuesta(ticket.monto)
                self.kwargs['add_hecho8_{0}'.format(item.pk)] = True
        self.mensaje.append('Hecho 1 y 8 listo.')

        # Liberamos candado
        self.set_release()

        return self.mensaje


tasks.register(AsyncGestion_add_ticket_apuesta_En_Linea)


class AsyncGestion_rest_ticket_apuesta(AsyncGestionOperationalError):
    name = 'AsyncGestion_rest_ticket_apuesta'
    queue = 'reportes'

    def run_try(self, *args, **kwargs):
        self.kwargs = kwargs
        self.mensaje = []
        self.mensaje.append('Ticket {0}'.format(kwargs.get('ticket')))
        ticket = Tickets.get_ticket_low(pk=kwargs.get('ticket'))

        self.mensaje.append(
            'Vendido {0}'.format(
                ticket.fecha.strftime('%d/%m/%Y %H:%M')))
        self.mensaje.append('Monto {0}'.format(ticket.monto))
        dimensiones = InitDimensiones()
        fecha = strFecha(ticket.fecha)
        fecha = fecha.getFecha()

        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho
        # 2 es por taquilla
        key = '{0}_{1}'.format('ventas_procesadas', ticket.user.taquilla_id)
        self.padlock = REDIS_DB.lock(key)
        self.set_acquire()
        # ================================================================================================

        if not self.kwargs.get('rest_hecho2'):
            hecho2 = dimensiones.get_hecho2_ventas_cadenas(
                fecha, ticket.user.taquilla)
            hecho2.rest_ticket(ticket)
            self.kwargs['rest_hecho2'] = True
            self.mensaje.append('Hecho 2 listo.')

        # ================================================================================================
        # Quitamos el candado
        self.set_release()
        # ================================================================================================

        kwargs = {
            'fecha': fecha,
            'taquilla_id': ticket.user.taquilla_id,
            'key': 'taquilla_id',
        }
        task = AsyncGestion_ProcessPorcentajesCadena()
        task.delay(*(), **kwargs)

        return self.mensaje


tasks.register(AsyncGestion_rest_ticket_apuesta)


class AsyncGestion_rest_ticket_apuesta_En_Linea(AsyncGestionOperationalError):
    name = 'AsyncGestion_rest_ticket_apuesta_En_Linea'
    queue = 'reportes'

    def run_try(self, *args, **kwargs):
        self.kwargs = kwargs
        self.mensaje = []
        self.mensaje.append('Ticket {0}'.format(kwargs.get('ticket')))
        ticket = Tickets.get_ticket_low(pk=kwargs.get('ticket'))
        self.mensaje.append(
            'Vendido {0}'.format(
                ticket.fecha.strftime('%d/%m/%Y %H:%M')))
        self.mensaje.append('Monto {0}'.format(ticket.monto))
        dimensiones = InitDimensiones()
        fecha = strFecha(ticket.fecha)
        fecha = fecha.getFecha()

        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho
        # 2 es por taquilla
        key = '{0}_{1}'.format('ventas_en_linea', ticket.user_id)
        self.padlock = REDIS_DB.lock(key)
        self.set_acquire()
        # ================================================================================================

        if not self.kwargs.get('rest_hecho2'):
            hecho2_linea = dimensiones.get_hecho2_ventas_cadenas_linea(
                fecha, ticket.user.taquilla)
            hecho2_linea.rest_ticket(ticket)
            self.kwargs['rest_hecho2'] = True
            self.mensaje.append('Hecho 2 listo.')

        ticket_items = ticket.ticketsdetail_set.only('jugada').all()
        for item in ticket_items:
            if not self.kwargs.get('rest_hecho1_{0}'.format(item.pk)):
                dimensiones.get_hecho1_ventas_cadenas_juegos(
                    fecha,
                    ticket.user.taquilla,
                    item.jugada
                ).rest_apuesta(item.monto)
                self.kwargs['rest_hecho1_{0}'.format(item.pk)] = True

            if not self.kwargs.get('rest_hecho8_{0}'.format(item.pk)):
                dimensiones.get_hecho8_ventas_monitor_linea(
                    fecha,
                    ticket.user.taquilla,
                    item.jugada,
                ).rest_apuesta(ticket.monto)
                self.kwargs['rest_hecho8_{0}'.format(item.pk)] = True
        self.mensaje.append('Hecho 1 y 8 listo.')

        # ================================================================================================
        # Quitamos el candado
        self.set_release()
        # ================================================================================================

        return self.mensaje


tasks.register(AsyncGestion_rest_ticket_apuesta_En_Linea)


class AsyncGestion_add_MontoPremio(AsyncGestionOperationalError):
    name = 'AsyncGestion_add_MontoPremio'
    queue = 'reportes'

    def run_try(self, *args, **kwargs):
        self.kwargs = kwargs
        self.mensaje = []
        self.mensaje.append('Ticket {0}'.format(kwargs.get('ticket')))
        ticket = Tickets.objects.select_related('user').only(
            'user__taquilla',
            'fecha',
            'monto_premio',
        ).get(pk=kwargs.get('ticket'))

        if kwargs.get('monto_premio'):
            monto_premio = Decimal(kwargs.get('monto_premio'))
        else:
            monto_premio = ticket.monto_premio

        self.mensaje.append(
            'Vendido {0}'.format(
                ticket.fecha.strftime('%d/%m/%Y %H:%M')))
        self.mensaje.append('Monto premio {0}'.format(monto_premio))
        ticket_items = ticket.ticketsdetail_set.only('jugada').all()
        dimensiones = InitDimensiones()
        fecha = strFecha(ticket.fecha)
        fecha = fecha.getFecha()

        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho
        # 2 es por taquilla
        key = '{0}_{1}'.format('ventas_procesadas', ticket.user.taquilla_id)
        self.padlock = REDIS_DB.lock(key)
        self.set_acquire()
        # ================================================================================================

        if not self.kwargs.get('add_hecho2_ventas'):
            hecho2 = dimensiones.get_hecho2_ventas_cadenas(
                fecha, ticket.user.taquilla)
            hecho2.add_monto_premios(monto_premio)
            self.kwargs['add_hecho2_ventas'] = True
            self.mensaje.append('Hecho 2 ventas listo.')

        if not self.kwargs.get('add_hecho2_linea'):
            hecho2_linea = dimensiones.get_hecho2_ventas_cadenas_linea(
                fecha, ticket.user.taquilla)
            hecho2_linea.add_monto_premios(monto_premio)
            self.kwargs['add_hecho2_linea'] = True
            self.mensaje.append('Hecho 2 linea listo.')

        monto_premio_juego = Decimal(
            Decimal(monto_premio) /
            ticket_items.count())
        for item in ticket_items:
            if not self.kwargs.get('add_hecho1_{0}'.format(item.pk)):
                dimensiones.get_hecho1_ventas_cadenas_juegos(
                    fecha,
                    ticket.user.taquilla,
                    item.jugada
                ).add_monto_premios(monto_premio_juego)
                self.kwargs['add_hecho1_{0}'.format(item.pk)] = True
        self.mensaje.append('Hecho 1 listo.')

        # ================================================================================================
        # Quitamos el candado
        self.set_release()
        # ================================================================================================

        kwargs = {
            'fecha': fecha,
            'taquilla_id': ticket.user.taquilla_id,
            'key': 'taquilla_id',
        }
        task = AsyncGestion_ProcessPorcentajesCadena()
        task.delay(*(), **kwargs)

        return self.mensaje


tasks.register(AsyncGestion_add_MontoPremio)


class AsyncGestion_rest_MontoPremio(AsyncGestionOperationalError):
    name = 'AsyncGestion_rest_MontoPremio'
    queue = 'reportes'

    def run_try(self, *args, **kwargs):
        self.kwargs = kwargs
        self.mensaje = []
        self.mensaje.append('Ticket {0}'.format(kwargs.get('ticket')))
        ticket = Tickets.objects.select_related('user').only(
            'user__taquilla',
            'fecha',
            'monto_premio',
        ).get(pk=kwargs.get('ticket'))

        if kwargs.get('monto_premio'):
            monto_premio = Decimal(kwargs.get('monto_premio'))
        else:
            monto_premio = ticket.monto_premio

        self.mensaje.append(
            'Vendido {0}'.format(
                ticket.fecha.strftime('%d/%m/%Y %H:%M')))
        self.mensaje.append('Monto premio {0}'.format(monto_premio))
        ticket_items = ticket.ticketsdetail_set.only('jugada').all()
        dimensiones = InitDimensiones()
        fecha = strFecha(ticket.fecha)
        fecha = fecha.getFecha()

        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho
        # 2 es por taquilla
        key = '{0}_{1}'.format('ventas_procesadas', ticket.user.taquilla_id)
        self.padlock = REDIS_DB.lock(key)
        self.set_acquire()
        # ================================================================================================
        if not self.kwargs.get('rest_hecho2_ventas'):
            hecho2 = dimensiones.get_hecho2_ventas_cadenas(
                fecha, ticket.user.taquilla)
            hecho2.rest_monto_premios(monto_premio)
            self.kwargs['rest_hecho2_ventas'] = True
            self.mensaje.append('Hecho 2 ventas listo.')

        if not self.kwargs.get('rest_hecho2_linea'):
            hecho2_linea = dimensiones.get_hecho2_ventas_cadenas_linea(
                fecha, ticket.user.taquilla)
            hecho2_linea.rest_monto_premios(monto_premio)
            self.kwargs['rest_hecho2_linea'] = True
            self.mensaje.append('Hecho 2 linea listo.')

        monto_premio_juego = Decimal(
            Decimal(monto_premio) /
            ticket_items.count())
        for item in ticket_items:
            if not self.kwargs.get('rest_hecho1_{0}'.format(item.pk)):
                dimensiones.get_hecho1_ventas_cadenas_juegos(
                    fecha,
                    ticket.user.taquilla,
                    item.jugada
                ).rest_monto_premios(monto_premio_juego)
                self.kwargs['rest_hecho1_{0}'.format(item.pk)] = True
        self.mensaje.append('Hecho 1 listo.')

        # ================================================================================================
        # Quitamos el candado
        self.set_release()
        # ================================================================================================

        kwargs = {
            'fecha': fecha,
            'taquilla_id': ticket.user.taquilla_id,
            'key': 'taquilla_id',
        }
        task = AsyncGestion_ProcessPorcentajesCadena()
        task.delay(*(), **kwargs)

        return self.mensaje


tasks.register(AsyncGestion_rest_MontoPremio)


class AsyncGestion_GainComercializadoraBase(AsyncGestionOperationalError):
    queue = 'reportes'

    def procesar_taquillas(self, taquilla):
        val_dimension_comercializacion = taquilla.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        monto_alquiler = taquilla.monto_alquiler
        if not monto_alquiler:
            monto_alquiler = float(
                taquilla.agencia.get_preference_value_by_codename('preference_amount_rental'))

        hecho5.alquiler = monto_alquiler
        hecho5.saldo_oper = monto_alquiler

        hecho5.save(update_fields=['saldo_oper', 'alquiler'])

    def procesar_agencias(self, agencia):

        val_dimension_comercializacion = agencia.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__taquilla_id__isnull=False,
            comercializacion__agencia_id=agencia.pk,
            tiempo=self.val_dimension_tiempo
        )
        sum_down = hecho5.aggregate(
            Sum('alquiler'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        hecho5.alquiler = sum_down['alquiler__sum']
        hecho5.saldo_oper = sum_down['alquiler__sum']
        hecho5.save(update_fields=['saldo_oper', 'alquiler'])

    def procesar_distribuidores(self, distribuidor):

        val_dimension_comercializacion = distribuidor.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__agencia_id__isnull=False,
            comercializacion__distribuidor_id=distribuidor.pk,
            tiempo=self.val_dimension_tiempo
        )

        sum_down = hecho5.aggregate(
            Sum('alquiler'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        hecho5.alquiler = sum_down['alquiler__sum']
        hecho5.saldo_oper = sum_down['alquiler__sum']
        hecho5.save(update_fields=['saldo_oper', 'alquiler'])

    def procesar_bancas(self, banca):

        val_dimension_comercializacion = banca.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__distribuidor_id__isnull=False,
            comercializacion__banca_id=banca.pk,
            tiempo=self.val_dimension_tiempo
        )

        sum_down = hecho5.aggregate(
            Sum('alquiler'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        hecho5.alquiler = sum_down['alquiler__sum']
        hecho5.saldo_oper = sum_down['alquiler__sum']
        hecho5.save(update_fields=['saldo_oper', 'alquiler'])

    def procesar_bloques(self, bloque):
        val_dimension_comercializacion = bloque.get_dimension_arco_comercializadora()

        hecho5 = Hecho5_ComisionesCadena.objects.filter(
            comercializacion__banca_id__isnull=False,
            comercializacion__bloque_id=bloque.pk,
            tiempo=self.val_dimension_tiempo
        )

        sum_down = hecho5.aggregate(
            Sum('alquiler'),
        )

        hecho5 = Hecho5_ComisionesCadena.objects.get_or_create(
            tiempo=self.val_dimension_tiempo,
            comercializacion=val_dimension_comercializacion
        )[0]

        # como estoy en nivel de bloque, actualizo el saldo del operador,
        # con lo calculado por las tareas asiscronas, evitando asi, q si esta
        # tarea se ejecuta mas de una vez, no haga sumas acumuladas
        # ni elimine dinero que debe contemplarse, esto solo se hace a este nivel
        # de la cadena
        hecho5.saldo_oper = hecho5.saldo_bruto - hecho5.participacion + hecho5.regalia

        hecho5.alquiler = sum_down['alquiler__sum']
        hecho5.saldo_oper += sum_down['alquiler__sum']
        hecho5.save(update_fields=['saldo_oper', 'alquiler'])

    def run_try(self, *args, **kwargs):
        mensaje = []

        taquillas = Taquillas.objects.filter(
            modo_alquiler=True,
            agencia_id__in=get_agencias_alquiler_by_frecuencia(self.frecuencia)
        ).exclude(
            usuariostaquilla__taquillastatusdetail__enddate=None,
            usuariostaquilla__taquillastatusdetail__status__codename='status_bloqueado'
        ).distinct()

        self.dimensiones = InitDimensiones()
        self.val_dimension_tiempo = self.dimensiones.get_dimension_tiempo(
            now().date())

        agencias = {}
        distribuidores = {}
        bancas = {}
        bloques = {}

        mensaje.append('Procesando ...')
        mensaje.append('Taqu: N° {}'.format(taquillas.count()))
        for taquilla in taquillas:
            self.procesar_taquillas(taquilla=taquilla)

            pk_agencia = '{0}'.format(taquilla.agencia_id)
            if pk_agencia not in agencias:
                agencias[pk_agencia] = taquilla.agencia

        mensaje.append('Agen: N° {}'.format(len(agencias)))
        for agencia in agencias.values():
            self.procesar_agencias(agencia=agencia)

            pk_distribuidore = '{0}'.format(agencia.distribuidores_id)
            if pk_distribuidore not in distribuidores:
                distribuidores[pk_distribuidore] = agencia.distribuidores

        mensaje.append('Dist: N° {}'.format(len(distribuidores)))
        for distribuidor in distribuidores.values():
            self.procesar_distribuidores(distribuidor=distribuidor)

            pk_banca = '{0}'.format(distribuidor.banca_id)
            if pk_banca not in bancas:
                bancas[pk_banca] = distribuidor.banca

        mensaje.append('Banc: N° {}'.format(len(bancas)))
        for banca in bancas.values():
            self.procesar_bancas(banca=banca)

            pk_bloque = '{0}'.format(banca.bloque_id)
            if pk_bloque not in bloques:
                bloques[pk_bloque] = banca.bloque

        mensaje.append('Bloq: N° {}'.format(len(bloques)))
        for bloque in bloques.values():
            self.procesar_bloques(bloque=bloque)

        mensaje.append('OK')
        return mensaje


class AsyncGestion_GainComercializadora_AlquiladosSemanal(
        AsyncGestion_GainComercializadoraBase):
    """
    Esta tarea asincrona hace el calculo de cobros para las taquillas
    con frecuenta semanal
    """
    name = 'AsyncGestion_GainComercializadora_AlquiladosSemanal'
    frecuencia = 'frecuencia_semanal'


tasks.register(AsyncGestion_GainComercializadora_AlquiladosSemanal)


class AsyncGestion_GainComercializadora_AlquiladosQuincenal(
        AsyncGestion_GainComercializadoraBase):
    """
    Esta tarea asincrona hace el calculo de cobros para las taquillas
    con frecuenta quincinal
    """
    name = 'AsyncGestion_GainComercializadora_AlquiladosQuincenal'
    frecuencia = 'frecuencia_quincenal'


tasks.register(AsyncGestion_GainComercializadora_AlquiladosQuincenal)


class AsyncGestion_GainComercializadora_AlquiladosMensual(
        AsyncGestion_GainComercializadoraBase):
    """
    Esta tarea asincrona hace el calculo de cobros para las taquillas
    con frecuenta mensual
    """
    name = 'AsyncGestion_GainComercializadora_AlquiladosMensual'
    frecuencia = 'frecuencia_mensual'


tasks.register(AsyncGestion_GainComercializadora_AlquiladosMensual)


class AsyncCheckComer_tickets(AsyncGestionOperationalError):
    name = 'AsyncCheckComer_tickets'
    queue = 'reportes_async'

    def run_try(self, *args, **kwargs):
        mensaje = ['¿Procesado?', ]

        comer = Comercializadora.objects.get(
            pk=kwargs.get('id_comer')
        )
        comer_object = comer.get_object()
        fecha = now().strptime(kwargs.get('fecha'), FORMAT_STR_DATE_REPORTS)

        if not comer_object.get_tickets_is_day_unprocessed(
                fecha=fecha).exists():
            mensaje.append('Si')
            # Entra solo si todos los tickets estan procesados

            # ================================================================
            # Aqui se deben agregar las tareas asyncronas a ejecutar
            # Agregarlas en segundo plano, como ya todo esta calculado,
            # usar en esas tareas la cola 'reportes_async' como cola (queue)
            # por defecto
            tarea = AsyncProcesarSaldos()
            tarea.run(
                *(), **{
                    'comercializadora': kwargs.get('id_comer'),
                    'fecha': kwargs.get('fecha'),
                    'tipo': comer_object.prefix_filter,
                }
            )

            if comer_object.resumen_automatic:
                from admin_finanzas.task import AsyncImportSaldosAutomatic
                tarea = AsyncImportSaldosAutomatic()
                tarea.delay(
                    *(),
                    **{
                        'id_comer': kwargs.get('id_comer'),
                        'fecha_ini': kwargs.get('fecha'),
                        'tipo': comer_object.prefix_filter,
                    }
                )
            # ================================================================

            if kwargs.get('no_recursive'):
                pass
            else:
                # Se ejecuta la misma funcion con el objeto origen
                # Por primera vez el objeto es una agencia,
                # pero luego es un distribuidor, y luego una banca,
                # y asi se llaman recursivamente hasta llegar a la operadora
                # quien al revisar que todas sus ventas estan prcesadas para un dia,
                # ejecuta las tareas o procesos necesarios
                origen = comer_object.get_origen()
                if origen:
                    task = AsyncCheckComer_tickets()
                    if kwargs.get('start_delay'):
                        task.delay(
                            *(),
                            **{
                                'id_comer': origen.get_comercializadora().pk,
                                'tipo': origen.prefix_filter,
                                'fecha': kwargs.get('fecha'),
                                'start_delay': False,
                            }
                        )
                    else:
                        task.run(
                            *(),
                            **{
                                'id_comer': origen.get_comercializadora().pk,
                                'tipo': origen.prefix_filter,
                                'fecha': kwargs.get('fecha'),
                                'start_delay': False,
                            }
                        )
        else:
            mensaje.append('No')
        return mensaje


tasks.register(AsyncCheckComer_tickets)


class AsyncProcesarSaldos(AsyncGestionOperationalError):
    name = 'AsyncProcesarSaldos'
    queue = 'reportes_async'

    def run_try(self, *args, **kwargs):
        self.mensaje = []
        data = {}
        self.fecha = kwargs.get('fecha')

        # Buscar la comercializadora a la que pertence el pk
        self.comercializadora = Comercializadora.objects.get(
            pk=kwargs.get('comercializadora'),
        )

        self.mensaje.append(self.comercializadora.pk)

        dimensiones = InitDimensiones()
        if self.comercializadora.get_type_codename() != 'userprofile_operadora':
            self.arcocomercializacion = self.comercializadora.get_object(
            ).get_dimension_arco_comercializadora()

            # ================================================================================================
            # Obtenemos y activamos el candado
            # Sincronizamos por el id de taquilla, ya que el hecho en linea y
            # hecho 2 es por taquilla
            key = '{0}_{1}'.format(
                'procesar_saldos_hecho9_arco_comer',
                self.arcocomercializacion.pk)
            self.padlock = REDIS_DB.lock(key)
            self.set_acquire()
            # ================================================================================================

            # Se consulta o crea el registro del hecho9
            hecho9 = dimensiones.get_hecho9_ventas_saldo_cadena(
                self.fecha,
                self.arcocomercializacion
            )

            # Calculo de los cargos por fecha de corte de queda
            calculos = self.calculo_cargo()
            hecho9.queda_corte = calculos[0]
            hecho9.cargos = calculos[1]

            # Calculo de los movimientos financieros
            self.movimientos = Movimiento.objects.filter(
                dia__fecha=self.fecha,
                comercializadora_id=self.comercializadora.pk
            )

            hecho9.depositos = self.calculo_movimiento(('tipo_deposito', ''))
            hecho9.pagos = self.calculo_movimiento(('tipo_pago', ''))
            hecho9.ajustes = self.calculo_movimiento(
                ('tipo_ajuste_cobrar', 'tipo_ajuste_pagar'))

            # Se verifica si hay un saldo anterior sino empieza en 0
            hecho9_anterior = list(Hecho9_VentasSaldosCadena.objects.filter(
                comercializacion=self.arcocomercializacion
            ).filter(
                tiempo__fecha__lte=self.fecha
            ).order_by('-tiempo__fecha')[0:2])

            # Consulta del hecho5 de la fecha dada
            hecho5_dia = Hecho5_ComisionesCadena.objects.filter(
                tiempo__fecha=self.fecha,
                comercializacion=self.arcocomercializacion,
            )
            # Para los calculos solo de necesitan los saldos de participacion
            data['montos_sum'] = hecho5_dia.aggregate(
                Sum('saldo_comer'),
                Sum('saldo_oper'),
            )
            if data['montos_sum']['saldo_oper__sum'] is None:
                data['montos_sum']['saldo_oper__sum'] = 0

            subtotal = data['montos_sum']['saldo_oper__sum'] + hecho9.depositos + hecho9.pagos \
                + hecho9.ajustes - hecho9.cargos

            if len(hecho9_anterior) > 1:
                hecho9.saldo_anterior = hecho9_anterior[1].saldo_actual
                hecho9.saldo_actual = hecho9.saldo_anterior + subtotal
            else:
                hecho9.saldo_anterior = 0
                hecho9.saldo_actual = subtotal
            hecho9.save()

            # ================================================================================================
            # Quitamos el candado
            self.set_release()
            # ================================================================================================
        return self.mensaje

    def calculo_cargo(self):
        data = []
        queda = 0
        cargo = 0
        fecha_date = datetime.strptime(
            self.fecha, FORMAT_STR_DATE_REPORTS).date()
        if self.comercializadora.get_object(
        ).get_frecuencia_queda_is_corte_day_early(fecha_date):
            queda_hecho5 = Hecho5_ComisionesCadena.objects.filter(
                tiempo__fecha__range=self.comercializadora.get_object()
                .get_frecuencia_queda_is_range_corte(
                    fecha_date
                ),
                comercializacion=self.arcocomercializacion
            )
            queda = queda_hecho5.aggregate(
                Sum('queda_ref')
            )['queda_ref__sum']

            if queda is None or queda < 0:
                queda = 0

            if queda > 0:
                cargo = queda * (1 - ObtenerPorcentaje(
                    codename='porcentaje_participacion',
                    cadena=self.comercializadora.get_object(),
                    fecha=now()
                )
                )
        data.append(queda)
        data.append(cargo)
        return data

    def calculo_movimiento(self, codename):
        resultado = self.movimientos.filter(
            tipo__codename__in=codename
        ).aggregate(Sum('monto'))['monto__sum']
        if resultado is None:
            resultado = 0
        return resultado


tasks.register(AsyncProcesarSaldos)
