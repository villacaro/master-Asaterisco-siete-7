# -*- coding: utf-8 -*-
"""
Vista de Resultados de Lotería — Sistema Asterisco Siete (*7)
Sustituye la antigua lógica de 'Cargar Marcador Deportivo'.

URL sugerida en urls.py:
    url(r'^resultado/registrar/$', RegistrarResultadoLoteriaView.as_view(),
        name='admin_juego_resultado_loteria_registrar'),
    url(r'^resultado/(?P<sorteo_id>\d+)/ver/$', VerResultadoLoteriaView.as_view(),
        name='admin_juego_resultado_loteria_ver'),
"""
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic import View

from admin_juego.models import EventNotification, types_notification


# ─────────────────────────────────────────────────────────────────────────────
# Constantes del Sistema Asterisco Siete (*7)
# ─────────────────────────────────────────────────────────────────────────────

# Tipos de jugada y sus multiplicadores de pago (base)
TIPOS_JUGADA = {
    'triple':    {'digitos': 3, 'factor_pago': 400,  'usa_signo': False},
    'terminal':  {'digitos': 2, 'factor_pago': 40,   'usa_signo': False},
    'cuatro':    {'digitos': 4, 'factor_pago': 3000, 'usa_signo': False},
    'cinco':     {'digitos': 5, 'factor_pago': 60000,'usa_signo': False},
    'animalito': {'digitos': 2, 'factor_pago': 8,    'usa_signo': False},
    'signo':     {'digitos': 3, 'factor_pago': 100,  'usa_signo': True},
}

DATA_ORIGIN_RESULTADO = types_notification['data_type_origin']['encuentro_modalidad'][0]  # 6


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de validación de números
# ─────────────────────────────────────────────────────────────────────────────

def _validar_numero(numero_str, tipo_jugada):
    """
    Valida que el número recibido sea correcto para el tipo de jugada.
    Retorna (True, numero_limpio) o (False, mensaje_error).
    """
    if not numero_str:
        return False, 'Número no proporcionado.'

    numero_limpio = numero_str.strip().zfill(TIPOS_JUGADA[tipo_jugada]['digitos'])

    if not numero_limpio.isdigit():
        return False, 'El número debe contener solo dígitos.'

    digitos_esperados = TIPOS_JUGADA[tipo_jugada]['digitos']
    if len(numero_limpio) != digitos_esperados:
        return False, 'El número debe tener {0} dígito(s) para jugada tipo "{1}".'.format(
            digitos_esperados, tipo_jugada
        )

    return True, numero_limpio


def _evaluar_premio(numero_ganador, numero_apostado, tipo_jugada):
    """
    Evalúa si una apuesta ganó según el tipo de jugada.
    Retorna True si gana, False si no.

    Lógica:
        - triple:    coincidencia exacta de 3 dígitos
        - terminal:  últimos 2 dígitos del triple ganador == apuesta
        - cuatro/cinco: coincidencia exacta
        - animalito: número_apostado == número_ganador (ID del animal)
        - signo:     triple + signo deben coincidir (validado externamente)
    """
    if tipo_jugada == 'triple':
        return numero_ganador == numero_apostado

    elif tipo_jugada == 'terminal':
        # Los últimos 2 dígitos del resultado triple
        return numero_ganador[-2:] == numero_apostado

    elif tipo_jugada in ('cuatro', 'cinco'):
        return numero_ganador == numero_apostado

    elif tipo_jugada == 'animalito':
        return numero_ganador == numero_apostado

    return False


# ─────────────────────────────────────────────────────────────────────────────
# Vista principal: Registrar Resultado
# ─────────────────────────────────────────────────────────────────────────────

class RegistrarResultadoLoteriaView(View):
    """
    POST: Registra el número ganador de un sorteo del Sistema Asterisco Siete (*7).

    Parámetros POST esperados:
        sorteo_id      (int)  — ID del sorteo (equivalente a encuentro_id)
        tipo_jugada    (str)  — Uno de: triple, terminal, cuatro, cinco, animalito, signo
        numero_ganador (str)  — Dígitos del resultado
        signo          (str)  — (Opcional) Signo zodiacal para jugadas con signo

    GET: Lista los sorteos pendientes de resultado del día actual.
    """

    def post(self, request, *args, **kwargs):
        # ── 1. Seguridad ──────────────────────────────────────────────────────
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse(
                {'status': 'error', 'msg': 'No autorizado'},
                status=403
            )

        # ── 2. Parámetros ─────────────────────────────────────────────────────
        sorteo_id      = request.POST.get('sorteo_id', '').strip()
        tipo_jugada    = request.POST.get('tipo_jugada', 'triple').strip().lower()
        numero_ganador = request.POST.get('numero_ganador', '').strip()
        signo          = request.POST.get('signo', None)

        if not sorteo_id or not sorteo_id.isdigit():
            return JsonResponse(
                {'status': 'error', 'msg': 'sorteo_id inválido.'},
                status=400
            )

        if tipo_jugada not in TIPOS_JUGADA:
            return JsonResponse(
                {'status': 'error', 'msg': 'tipo_jugada desconocido: {0}'.format(tipo_jugada)},
                status=400
            )

        # ── 3. Validar número ─────────────────────────────────────────────────
        ok, valor = _validar_numero(numero_ganador, tipo_jugada)
        if not ok:
            return JsonResponse({'status': 'error', 'msg': valor}, status=400)
        numero_limpio = valor

        # ── 4. Verificar que no exista ya un resultado para este sorteo ───────
        ya_existe = EventNotification.objects.filter(
            data_origin=DATA_ORIGIN_RESULTADO,
            pk_origin=int(sorteo_id),
        ).exists()
        if ya_existe:
            return JsonResponse(
                {'status': 'error', 'msg': 'Ya existe un resultado registrado para este sorteo.'},
                status=409
            )

        # ── 5. Construir data del resultado ───────────────────────────────────
        resultado_data = {
            'numero':          numero_limpio,
            'tipo_jugada':     tipo_jugada,
            'signo':           signo,
            'fecha_registro':  now().isoformat(),
            'sistema':         'Asterisco Siete (*7)',
            'encuentro_id':    int(sorteo_id),
            'origen':          0,
        }

        # ── 6. Crear notificación de resultado ────────────────────────────────
        try:
            sistema_id = None
            try:
                from admin_principal.security import Security
                security = Security()
                sistema_id = security.get_sistemaJuego(request).pk
            except Exception:
                pass

            notificacion = EventNotification.objects.create(
                sistema=sistema_id,
                data_origin=DATA_ORIGIN_RESULTADO,  # 6 = Resultados Lotería
                pk_origin=int(sorteo_id),
                data=resultado_data,
                in_production=True,
            )

            return JsonResponse({
                'status':   'success',
                'msg':      'Resultado {numero} ({tipo}) registrado en Asterisco Siete (*7).'.format(
                    numero=numero_limpio,
                    tipo=tipo_jugada,
                ),
                'id':       notificacion.pk,
                'sorteo_id': sorteo_id,
            })

        except Exception as exc:
            return JsonResponse(
                {'status': 'error', 'msg': str(exc)},
                status=400
            )

    def get(self, request, *args, **kwargs):
        """
        Retorna los IDs de sorteos que ya tienen resultado registrado hoy,
        para que el frontend pueda marcarlos como cerrados.
        """
        from django.utils.timezone import localdate
        hoy = localdate()

        resultados_hoy = EventNotification.objects.filter(
            data_origin=DATA_ORIGIN_RESULTADO,
            date_production__date=hoy,
            in_production=True,
        ).values('pk_origin', 'data', 'pk')

        return JsonResponse({
            'status': 'success',
            'resultados': [
                {
                    'id':          r['pk'],
                    'sorteo_id':   r['pk_origin'],
                    'numero':      r['data'].get('numero', '-'),
                    'tipo_jugada': r['data'].get('tipo_jugada', '-'),
                    'signo':       r['data'].get('signo'),
                    'fecha':       r['data'].get('fecha_registro', '-'),
                }
                for r in resultados_hoy
            ],
        })


# ─────────────────────────────────────────────────────────────────────────────
# Vista auxiliar: Ver / consultar resultado de un sorteo
# ─────────────────────────────────────────────────────────────────────────────

class VerResultadoLoteriaView(View):
    """
    GET /asterisco7/resultado/<sorteo_id>/ver/
    Devuelve el resultado registrado para ese sorteo.
    """

    def get(self, request, sorteo_id, *args, **kwargs):
        try:
            notificacion = EventNotification.objects.filter(
                data_origin=DATA_ORIGIN_RESULTADO,
                pk_origin=int(sorteo_id),
            ).latest('pk')

            return JsonResponse({
                'status':      'success',
                'sorteo_id':   sorteo_id,
                'numero':      notificacion.data.get('numero', '-'),
                'tipo_jugada': notificacion.data.get('tipo_jugada', '-'),
                'signo':       notificacion.data.get('signo'),
                'fecha':       notificacion.data.get('fecha_registro', '-'),
                'sistema':     notificacion.data.get('sistema', '-'),
            })

        except EventNotification.DoesNotExist:
            return JsonResponse(
                {'status': 'error', 'msg': 'Sin resultado registrado para sorteo {0}'.format(sorteo_id)},
                status=404
            )
