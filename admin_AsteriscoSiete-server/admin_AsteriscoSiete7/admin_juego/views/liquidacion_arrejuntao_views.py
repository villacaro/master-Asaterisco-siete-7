# -*- coding: utf-8 -*-
"""
liquidacion_arrejuntao_views.py — Sistema Asterisco Siete (*7)
==============================================================
Motor de liquidación del producto EL ARREJUNTAO.

Endpoints disponibles:
    POST  /asterisco7/liquidar/          → LiquidarArrejuntaoView
    GET   /asterisco7/liquidar/<id>/     → ConsultarLiquidacionView

Parámetros POST (liquidar):
    sorteo_id       (int)  — ID del sorteo a liquidar
    triple_a        (str)  — Resultado Triple A (3 dígitos)
    triple_b        (str)  — Resultado Triple B (3 dígitos, opcional)
    signo           (str)  — Signo zodiacal ganador (ej. ARIES)
    cuatro_digitos  (str)  — Resultado El Arrimao (4 dígitos)
    cinco_digitos   (str)  — Resultado El Pegadito (5 dígitos)
    animalito       (str)  — Figura ganadora (0-75 o '00')
"""
from decimal import Decimal

from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic import View

from admin_juego.constants_arrejuntao import (
    SIGNOS_ZODIACALES, TIPOS_JUGADA_ARREJUNTAO,
    es_figura_valida, es_tipo_valido, get_factor_pago, get_nombre_animalito,
)
from admin_juego.models import EventNotification, types_notification

DATA_ORIGIN_RESULTADO = types_notification['data_type_origin']['encuentro_modalidad'][0]  # 6


# ─────────────────────────────────────────────────────────────────────────────
# Motor de premiación — función pura, sin acceso a BD
# ─────────────────────────────────────────────────────────────────────────────

def evaluar_apuesta_arrejuntao(tipo_jugada, numero_apostado, signo_apostado, resultados):
    """
    Evalúa si una apuesta individual ganó en EL ARREJUNTAO.

    Args:
        tipo_jugada    (str): código del tipo (ej. 'TRIPLE_A', 'ANIMALITO')
        numero_apostado(str): número apostado por el jugador
        signo_apostado (str|None): signo apostado (solo para tipos con signo)
        resultados     (dict): resultados del sorteo con claves:
            triple_a, triple_b, signo, cuatro_digitos, cinco_digitos, animalito

    Returns:
        (bool, str): (ganó, descripción de resultado)
    """
    if not es_tipo_valido(tipo_jugada):
        return False, 'Tipo de jugada desconocido: {0}'.format(tipo_jugada)

    config = TIPOS_JUGADA_ARREJUNTAO[tipo_jugada]
    resultado_key = config['resultado_key']
    numero_ganador = resultados.get(resultado_key, '')

    if not numero_ganador:
        return False, 'Resultado no disponible para {0}'.format(resultado_key)

    # ── 1. Triple A / Triple B ────────────────────────────────────────────────
    if tipo_jugada in ('TRIPLE_A', 'TRIPLE_B'):
        gana = numero_apostado == numero_ganador
        return gana, 'Triple: {0} vs {1}'.format(numero_apostado, numero_ganador)

    # ── 2. Terminal A / Terminal B ────────────────────────────────────────────
    elif tipo_jugada in ('TERMINAL_A', 'TERMINAL_B'):
        terminal_ganador = numero_ganador[-2:]
        gana = numero_apostado == terminal_ganador
        return gana, 'Terminal: {0} vs {1} (últimos 2 de {2})'.format(
            numero_apostado, terminal_ganador, numero_ganador
        )

    # ── 3. Triple con Signo ───────────────────────────────────────────────────
    elif tipo_jugada in ('TRIPLE_SIGNO_A', 'TRIPLE_SIGNO_B'):
        signo_ganador = resultados.get('signo', '')
        gana_num = numero_apostado == numero_ganador
        gana_signo = (signo_apostado or '').upper() == signo_ganador.upper()
        gana = gana_num and gana_signo
        return gana, 'Triple+Signo: {0}/{1} vs {2}/{3}'.format(
            numero_apostado, signo_apostado, numero_ganador, signo_ganador
        )

    # ── 4. Terminal con Signo ─────────────────────────────────────────────────
    elif tipo_jugada in ('TERMINAL_SIGNO_A', 'TERMINAL_SIGNO_B'):
        terminal_ganador = numero_ganador[-2:]
        signo_ganador = resultados.get('signo', '')
        gana_num = numero_apostado == terminal_ganador
        gana_signo = (signo_apostado or '').upper() == signo_ganador.upper()
        gana = gana_num and gana_signo
        return gana, 'Terminal+Signo: {0}/{1} vs {2}/{3}'.format(
            numero_apostado, signo_apostado, terminal_ganador, signo_ganador
        )

    # ── 5. El Arrimao (4 dígitos) ─────────────────────────────────────────────
    elif tipo_jugada == 'ARRIMAO':
        gana = numero_apostado == numero_ganador
        return gana, 'Arrimao: {0} vs {1}'.format(numero_apostado, numero_ganador)

    # ── 6. El Pegadito (5 dígitos) ────────────────────────────────────────────
    elif tipo_jugada == 'PAGADITO':
        gana = numero_apostado == numero_ganador
        return gana, 'Pegadito: {0} vs {1}'.format(numero_apostado, numero_ganador)

    # ── 7. Animalitos (77 figuras) ────────────────────────────────────────────
    elif tipo_jugada == 'ANIMALITO':
        gana = str(numero_apostado) == str(numero_ganador)
        nombre_ganador = get_nombre_animalito(numero_ganador)
        return gana, 'Animalito: {0} vs {1} ({2})'.format(
            numero_apostado, numero_ganador, nombre_ganador
        )

    return False, 'Lógica no implementada para {0}'.format(tipo_jugada)


def liquidar_arrejuntao(sorteo_id, resultados, apuestas_qs=None):
    """
    Liquida todas las apuestas pendientes de un sorteo del producto EL ARREJUNTAO.

    Args:
        sorteo_id  (int): ID del sorteo
        resultados (dict): resultados con claves:
            triple_a, triple_b, signo, cuatro_digitos, cinco_digitos, animalito
        apuestas_qs: QuerySet de apuestas pendientes (opcional; si no se provee,
                     la función retorna solo el resumen de evaluación sin tocar BD)

    Returns:
        dict con estadísticas de liquidación:
            total, ganadoras, perdedoras, errores, detalle
    """
    stats = {
        'sorteo_id': sorteo_id,
        'resultados': resultados,
        'total': 0,
        'ganadoras': 0,
        'perdedoras': 0,
        'errores': 0,
        'detalle': [],
    }

    if apuestas_qs is None:
        # Modo simulación: solo retorna los resultados sin tocar la BD
        stats['modo'] = 'simulacion'
        return stats

    stats['modo'] = 'produccion'

    for apuesta in apuestas_qs:
        stats['total'] += 1
        try:
            gana, descripcion = evaluar_apuesta_arrejuntao(
                tipo_jugada=apuesta.tipo,
                numero_apostado=apuesta.numero,
                signo_apostado=getattr(apuesta, 'signo', None),
                resultados=resultados,
            )

            if gana:
                stats['ganadoras'] += 1
                apuesta.marcar_como_ganador(sistema='Asterisco Siete (*7)')
            else:
                stats['perdedoras'] += 1
                apuesta.marcar_como_perdedor()

            stats['detalle'].append({
                'apuesta_id': apuesta.pk,
                'tipo':       apuesta.tipo,
                'numero':     apuesta.numero,
                'gana':       gana,
                'detalle':    descripcion,
            })

        except Exception as exc:
            stats['errores'] += 1
            stats['detalle'].append({
                'apuesta_id': getattr(apuesta, 'pk', None),
                'error':      str(exc),
            })

    return stats


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de validación de resultados
# ─────────────────────────────────────────────────────────────────────────────

def _validar_resultados(data):
    """
    Valida el diccionario de resultados recibido por POST.
    Retorna (True, resultados_limpios) o (False, mensaje_error).
    """
    errores = []

    triple_a = data.get('triple_a', '').strip().zfill(3)
    triple_b = data.get('triple_b', '').strip().zfill(3) if data.get('triple_b') else None
    signo    = (data.get('signo', '') or '').strip().upper()
    cuatro   = data.get('cuatro_digitos', '').strip().zfill(4)
    cinco    = data.get('cinco_digitos', '').strip().zfill(5)
    animalito = data.get('animalito', '').strip()

    if not triple_a.isdigit() or len(triple_a) != 3:
        errores.append('triple_a debe tener 3 dígitos.')
    if triple_b and (not triple_b.isdigit() or len(triple_b) != 3):
        errores.append('triple_b debe tener 3 dígitos si se proporciona.')
    if signo and signo not in SIGNOS_ZODIACALES:
        errores.append('Signo inválido: {0}. Válidos: {1}'.format(
            signo, ', '.join(SIGNOS_ZODIACALES)
        ))
    if cuatro and (not cuatro.isdigit() or len(cuatro) != 4):
        errores.append('cuatro_digitos debe tener 4 dígitos.')
    if cinco and (not cinco.isdigit() or len(cinco) != 5):
        errores.append('cinco_digitos debe tener 5 dígitos.')
    if animalito and not es_figura_valida(animalito):
        errores.append('Figura de animalito inválida: {0}'.format(animalito))

    if errores:
        return False, ' | '.join(errores)

    return True, {
        'triple_a':      triple_a,
        'triple_b':      triple_b or triple_a,   # fallback a triple_a si no hay B
        'signo':         signo,
        'cuatro_digitos': cuatro,
        'cinco_digitos':  cinco,
        'animalito':      animalito,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Vista: Liquidar sorteo
# ─────────────────────────────────────────────────────────────────────────────

class LiquidarArrejuntaoView(View):
    """
    POST /asterisco7/liquidar/

    Registra los resultados de un sorteo y dispara la liquidación de apuestas.
    Si no se provee un queryset de apuestas (entorno de prueba), funciona
    en modo simulación y retorna el resumen sin tocar la BD.
    """

    def post(self, request, *args, **kwargs):
        # ── Seguridad ─────────────────────────────────────────────────────────
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'status': 'error', 'msg': 'No autorizado'}, status=403)

        sorteo_id = request.POST.get('sorteo_id', '').strip()
        if not sorteo_id or not sorteo_id.isdigit():
            return JsonResponse({'status': 'error', 'msg': 'sorteo_id inválido.'}, status=400)

        # ── Validar resultados ────────────────────────────────────────────────
        ok, valor = _validar_resultados(request.POST)
        if not ok:
            return JsonResponse({'status': 'error', 'msg': valor}, status=400)
        resultados = valor

        # ── Verificar duplicado ───────────────────────────────────────────────
        ya_existe = EventNotification.objects.filter(
            data_origin=DATA_ORIGIN_RESULTADO,
            pk_origin=int(sorteo_id),
        ).exists()
        if ya_existe:
            return JsonResponse(
                {'status': 'error', 'msg': 'Ya existe resultado para este sorteo.'},
                status=409
            )

        try:
            # ── Obtener sistema ───────────────────────────────────────────────
            sistema_id = None
            try:
                from admin_principal.security import Security
                sistema_id = Security().get_sistemaJuego(request).pk
            except Exception:
                pass

            # ── Guardar resultado en EventNotification ────────────────────────
            nombre_animalito = get_nombre_animalito(resultados['animalito'])
            data_resultado = {
                **resultados,
                'nombre_animalito': nombre_animalito,
                'fecha_registro':   now().isoformat(),
                'sistema':          'Asterisco Siete (*7)',
                'encuentro_id':     int(sorteo_id),
                'origen':           0,
            }

            EventNotification.objects.create(
                sistema=sistema_id,
                data_origin=DATA_ORIGIN_RESULTADO,
                pk_origin=int(sorteo_id),
                data=data_resultado,
                in_production=True,
            )

            # ── Liquidar apuestas ─────────────────────────────────────────────
            # Para conectar con tu modelo de apuestas real, descomenta y ajusta:
            # from admin_apuestas.models import ApuestaDetalle
            # apuestas = ApuestaDetalle.objects.filter(
            #     sorteo_id=sorteo_id, estatus='Pendiente'
            # )
            # stats = liquidar_arrejuntao(int(sorteo_id), resultados, apuestas)
            stats = liquidar_arrejuntao(int(sorteo_id), resultados)  # modo simulación

            return JsonResponse({
                'status':            'success',
                'msg':               'Sorteo {0} liquidado — Asterisco Siete (*7)'.format(sorteo_id),
                'resultados':        resultados,
                'nombre_animalito':  nombre_animalito,
                'estadisticas':      {k: v for k, v in stats.items() if k != 'detalle'},
            })

        except Exception as exc:
            return JsonResponse({'status': 'error', 'msg': str(exc)}, status=400)


# ─────────────────────────────────────────────────────────────────────────────
# Vista: Consultar liquidación de un sorteo
# ─────────────────────────────────────────────────────────────────────────────

class ConsultarLiquidacionView(View):
    """
    GET /asterisco7/liquidar/<sorteo_id>/
    Retorna el resultado registrado y las estadísticas de un sorteo liquidado.
    """

    def get(self, request, sorteo_id, *args, **kwargs):
        try:
            notif = EventNotification.objects.filter(
                data_origin=DATA_ORIGIN_RESULTADO,
                pk_origin=int(sorteo_id),
            ).latest('pk')

            return JsonResponse({
                'status':    'success',
                'sorteo_id': sorteo_id,
                'resultado': {
                    'triple_a':        notif.data.get('triple_a', '-'),
                    'triple_b':        notif.data.get('triple_b', '-'),
                    'signo':           notif.data.get('signo', '-'),
                    'cuatro_digitos':  notif.data.get('cuatro_digitos', '-'),
                    'cinco_digitos':   notif.data.get('cinco_digitos', '-'),
                    'animalito':       notif.data.get('animalito', '-'),
                    'nombre_animalito':notif.data.get('nombre_animalito', '-'),
                    'fecha_registro':  notif.data.get('fecha_registro', '-'),
                },
            })

        except EventNotification.DoesNotExist:
            return JsonResponse(
                {'status': 'error', 'msg': 'Sin resultado para sorteo {0}'.format(sorteo_id)},
                status=404
            )
