# -*- coding: utf-8 -*-
"""
models_arrejuntao.py — Sistema Asterisco Siete (*7)
====================================================
Modelos para la gestión de Productos de Lotería (Plantillas).

Permite definir productos como "EL ARREJUNTAO" con sus jugadas habilitadas,
rangos de animalitos, y límites de venta por tipo de jugada.

Requiere migración:
    python manage.py makemigrations admin_juego
    python manage.py migrate
"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from jsonfield import JSONField

from admin_juego.constants_arrejuntao import (
    ANIMALITO_MAX, ANIMALITO_MIN, SIGNOS_ZODIACALES, TIPOS_JUGADA_ARREJUNTAO,
)
from admin_juego.models import types_notification

# ─────────────────────────────────────────────────────────────────────────────
# Choices generados desde las constantes del Arrejuntao
# ─────────────────────────────────────────────────────────────────────────────
CHOICES_TIPO_JUGADA = [
    (codigo, config['nombre'])
    for codigo, config in TIPOS_JUGADA_ARREJUNTAO.items()
]

CHOICES_SIGNO = [(s, s.capitalize()) for s in SIGNOS_ZODIACALES]


# ─────────────────────────────────────────────────────────────────────────────
# PlantillaProducto — Define un producto de lotería (ej. EL ARREJUNTAO)
# ─────────────────────────────────────────────────────────────────────────────

class PlantillaProducto(models.Model):
    """
    Define la estructura base de un producto de lotería.

    Ejemplo:
        nombre = "EL ARREJUNTAO"
        modulos_activos = {
            "TRIPLE_A": True, "TRIPLE_B": True,
            "TERMINAL_A": True, "TERMINAL_B": True,
            "TRIPLE_SIGNO_A": True, "TRIPLE_SIGNO_B": True,
            "TERMINAL_SIGNO_A": True, "TERMINAL_SIGNO_B": True,
            "ARRIMAO": True, "PAGADITO": True, "ANIMALITO": True
        }
        animalito_min = 0
        animalito_max = 75
        usa_doble_cara = True  # True = tiene variantes A y B
    """

    nombre = models.CharField(
        max_length=120,
        unique=True,
        verbose_name='Nombre del Tipo de Producto',
        help_text='Ej: EL ARREJUNTAO, TRIPLE ZULIA, etc.',
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción',
    )

    activo = models.BooleanField(
        default=True,
        verbose_name='¿TipoProducto activo?',
        db_index=True,
    )

    # JSON con los tipos de jugada activos: {'TRIPLE_A': True, 'ANIMALITO': True, ...}
    modulos_activos = JSONField(
        default=dict,
        verbose_name='Módulos de jugada activos',
        help_text='Diccionario de tipos de jugada habilitados para este producto.',
    )

    # Rango de figuras de animalitos configurado para este producto
    animalito_min = models.IntegerField(
        default=ANIMALITO_MIN,
        verbose_name='Figura mínima de Animalito',
    )
    animalito_max = models.IntegerField(
        default=ANIMALITO_MAX,
        verbose_name='Figura máxima de Animalito',
        help_text='75 para la tabla completa del Arrejuntao.',
    )

    usa_doble_cara = models.BooleanField(
        default=True,
        verbose_name='¿Usa Triple A y B (doble cara)?',
        help_text='EL ARREJUNTAO usa triple_a y triple_b; algunos productos solo uno.',
    )

    usa_signo = models.BooleanField(
        default=True,
        verbose_name='¿Acepta jugadas con Signo Zodiacal?',
    )

    logo = models.ImageField(
        upload_to='productos/logos/',
        null=True,
        blank=True,
        verbose_name='Logo del TipoProducto',
    )

    orden = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Orden de presentación',
    )

    sistema = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Sistema de Juego',
        help_text='ID del SistemaJuego al que pertenece este producto.',
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Plantilla de TipoProducto'
        verbose_name_plural = 'Plantillas de Productos'
        ordering = ['orden', 'nombre']

    def __str__(self):
        estado = '✓' if self.activo else '✗'
        return '[{0}] {1}'.format(estado, self.nombre)

    def get_jugadas_activas(self):
        """Retorna la lista de códigos de jugada habilitados para este producto."""
        return [k for k, v in (self.modulos_activos or {}).items() if v]

    def get_config_jugada(self, tipo_jugada):
        """Retorna la configuración completa de un tipo de jugada."""
        return TIPOS_JUGADA_ARREJUNTAO.get(tipo_jugada)

    @classmethod
    def crear_arrejuntao(cls, sistema_id=None):
        """
        Factory: crea o retorna la plantilla estándar del producto EL ARREJUNTAO.
        Se puede llamar desde un fixture o desde el shell de Django.
        """
        producto, creado = cls.objects.get_or_create(
            nombre='EL ARREJUNTAO',
            defaults={
                'descripcion': (
                    'TipoProducto completo con Triple A/B, Terminal, Signos, '
                    'El Arrimao (4 dígitos), El Pegadito (5 dígitos) y 77 Animalitos.'
                ),
                'modulos_activos': {k: True for k in TIPOS_JUGADA_ARREJUNTAO},
                'animalito_min': 0,
                'animalito_max': 75,
                'usa_doble_cara': True,
                'usa_signo': True,
                'orden': 1,
                'sistema': sistema_id,
            }
        )
        return producto, creado


# ─────────────────────────────────────────────────────────────────────────────
# PlantillaJugada — Configuración individual por tipo de jugada dentro del producto
# ─────────────────────────────────────────────────────────────────────────────

class PlantillaJugada(models.Model):
    """
    Configuración de cada tipo de jugada dentro de un producto.

    Permite sobrescribir el factor de pago y el monto máximo de apuesta
    por producto, sin tocar las constantes globales.
    """

    producto = models.ForeignKey(
        'PlantillaProducto',
        on_delete=models.CASCADE,
        related_name='jugadas',
    )

    tipo_jugada = models.CharField(
        max_length=30,
        choices=CHOICES_TIPO_JUGADA,
        verbose_name='Tipo de Jugada',
        db_index=True,
    )

    activa = models.BooleanField(
        default=True,
        verbose_name='¿Jugada activa?',
    )

    # Factor de pago: cuánto se multiplica el monto apostado si gana
    factor_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Factor de Pago (multiplicador)',
        help_text='Ej: 400 para Triple, 8 para Animalito.',
    )

    # Límite de venta total por sorteo para este tipo de jugada
    monto_maximo_venta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Monto máximo de venta por sorteo',
        help_text='0 = sin límite.',
    )

    # Límite por número individual (cupo)
    cupo_por_numero = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Cupo máximo por número',
        help_text='Límite de venta para un mismo número en el sorteo. 0 = sin límite.',
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Configuración de Jugada'
        verbose_name_plural = 'Configuraciones de apuesta'
        unique_together = [('producto', 'tipo_jugada')]
        ordering = ['producto', 'tipo_jugada']

    def __str__(self):
        return '{0} → {1} (x{2})'.format(
            self.producto.nombre,
            self.get_tipo_jugada_display(),
            self.factor_pago,
        )

    def tiene_cupo_disponible(self, numero, monto_solicitado, ventas_actuales):
        """
        Verifica si un número específico tiene cupo disponible.

        Args:
            numero (str): número apostado
            monto_solicitado (Decimal): monto de la apuesta nueva
            ventas_actuales (Decimal): suma de ventas ya registradas para ese número

        Returns:
            (bool, str): (tiene_cupo, mensaje)
        """
        if self.cupo_por_numero <= 0:
            return True, 'Sin límite de cupo.'

        if (ventas_actuales + monto_solicitado) > self.cupo_por_numero:
            disponible = max(0, self.cupo_por_numero - ventas_actuales)
            return False, (
                'Cupo agotado para el número {numero}. '
                'Disponible: {disponible:.2f}'.format(
                    numero=numero,
                    disponible=disponible,
                )
            )
        return True, 'Cupo disponible.'


# ─────────────────────────────────────────────────────────────────────────────
# LiquidacionSorteo — Tabla financiera de liquidación por sorteo
# ─────────────────────────────────────────────────────────────────────────────

class LiquidacionSorteo(models.Model):
    """
    Registra el resumen financiero completo de un sorteo liquidado.

    Jerarquía de actores:
        Prestador de Servicio → Comercializador/Bloque → Banca
        → Distribuidor → Agencia → Taquilla → Operador

    Incluye:
        - Comisiones, participaciones y regalías por actor
        - Montos de venta, premios y saldos netos/brutos
        - Serial de impresora fiscal (IFA)
    """

    # ── Identificadores de jerarquía ──────────────────────────────────────────
    id_sorteo = models.IntegerField(
        db_index=True,
        verbose_name='ID SorteoArrejuntao',
        help_text='Identificación del sorteo liquidado.',
    )
    id_lista = models.IntegerField(
        verbose_name='ID Lista',
        help_text='Identificación de la lista.',
    )
    id_tipo_lista = models.IntegerField(
        verbose_name='ID Tipo de Lista',
        help_text='Identificación del tipo de lista.',
    )
    id_prestador_servicio = models.IntegerField(
        verbose_name='ID Prestador de Servicio',
        help_text='Identificación del Prestador de Servicio.',
    )
    id_comercializador = models.IntegerField(
        db_index=True,
        verbose_name='ID Comercializador / Bloque',
        help_text='Identificación del Comercializador / Bloque.',
    )
    id_banca = models.IntegerField(
        db_index=True,
        verbose_name='ID Banca',
        help_text='Identificación de la Banca.',
    )
    id_distribuidor = models.IntegerField(
        db_index=True,
        verbose_name='ID Distribuidor',
        help_text='Identificación del Distribuidor.',
    )
    id_agencia = models.IntegerField(
        db_index=True,
        verbose_name='ID Agencia',
        help_text='Identificación de la Agencia.',
    )
    id_taquilla = models.IntegerField(
        verbose_name='ID Taquilla',
        help_text='Identificación de la Taquilla.',
    )
    id_operador = models.IntegerField(
        verbose_name='ID Operador',
        help_text='Identificación del Operador.',
    )

    # ── Porcentajes — Comercializador / Bloque ────────────────────────────────
    nporcentaje_comision_com = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Comercializador',
        help_text='Porcentaje de comisión asignado al Comercializador / Bloque.',
    )
    nporcentaje_participacion_com = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Participación Comercializador',
        help_text='Porcentaje de participación asignado al Comercializador / Bloque.',
    )
    nporcentaje_regalia_com = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Regalía Comercializador',
        help_text='Porcentaje de regalía asignado al Comercializador / Bloque.',
    )

    # ── Porcentajes — Banca ───────────────────────────────────────────────────
    nporcentaje_comision_ban = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Banca',
        help_text='Porcentaje de comisión asignado a la Banca.',
    )
    nporcentaje_participacion_ban = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Participación Banca',
        help_text='Porcentaje de participación asignado a la Banca.',
    )
    nporcentaje_regalia_ban = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Regalía Banca',
        help_text='Porcentaje de regalía asignado a la Banca.',
    )

    # ── Porcentajes — Distribuidor ────────────────────────────────────────────
    nporcentaje_comision_dis = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Distribuidor',
        help_text='Porcentaje de comisión asignado al Distribuidor.',
    )
    nporcentaje_participacion_dis = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Participación Distribuidor',
        help_text='Porcentaje de participación asignado al Distribuidor.',
    )
    nporcentaje_regalia_dis = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Regalía Distribuidor',
        help_text='Porcentaje de regalía asignado al Distribuidor.',
    )

    # ── Porcentajes — Agencia ─────────────────────────────────────────────────
    nporcentaje_comision_agc = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Agencia',
        help_text='Porcentaje de comisión asignado a la Agencia.',
    )

    # ── Montos de venta y premios ─────────────────────────────────────────────
    mmonto_venta = models.DecimalField(
        max_digits=13, decimal_places=2,
        verbose_name='Monto de Venta',
        help_text='Monto total de ventas del sorteo.',
    )
    mmonto_venta_ganador = models.DecimalField(
        max_digits=13, decimal_places=2,
        verbose_name='Monto de Venta al Número Ganador',
        help_text='Monto de venta al número/figura ganadora.',
    )
    mmonto_premios = models.DecimalField(
        max_digits=13, decimal_places=2,
        verbose_name='Monto de Premios',
        help_text='Monto total de premios a pagar.',
    )

    # ── Comisiones y regalías a pagar (montos calculados) ─────────────────────
    mmonto_comision_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Comercializador',
        help_text='Monto a pagar en comisión al Comercializador / Bloque.',
    )
    mmonto_regalia_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Regalía Comercializador',
        help_text='Monto a pagar en regalía al Comercializador / Bloque.',
    )
    mmonto_comision_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Banca',
        help_text='Monto a pagar en comisión a la Banca.',
    )
    mmonto_regalia_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Regalía Banca',
        help_text='Monto a pagar en regalía a la Banca.',
    )
    mmonto_comision_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Distribuidor',
        help_text='Monto a pagar en comisión al Distribuidor.',
    )
    mmonto_regalia_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Regalía Distribuidor',
        help_text='Monto a pagar en regalía al Distribuidor.',
    )
    mmonto_comision_agc = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Agencia',
        help_text='Monto a pagar en comisión a la Agencia.',
    )

    # ── Saldos netos por actor ────────────────────────────────────────────────
    msaldo_oper = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Operador',
    )
    msaldo_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Comercializador / Bloque',
    )
    msaldo_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Banca',
    )
    msaldo_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Distribuidor',
    )
    msaldo_agc = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Agencia',
    )

    # ── Serial de Impresora Fiscal (IFA) ──────────────────────────────────────
    tserial_ifa = models.CharField(
        max_length=50,
        verbose_name='Serial Impresora Fiscal (IFA)',
        help_text='Serial de la Impresora Fiscal asociada al sorteo.',
    )

    # ── Saldos brutos ─────────────────────────────────────────────────────────
    msaldo_bruto_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Bruto Comercializador / Bloque',
    )
    msaldo_bruto_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Bruto Banca',
    )
    msaldo_bruto_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Bruto Distribuidor',
    )

    # ── Perfil de pago de premios ─────────────────────────────────────────────
    id_perfil_pago_premios = models.IntegerField(
        null=True, blank=True,
        verbose_name='ID Perfil de Pago de Premios',
        help_text='Identificación del perfil de pago de premios.',
    )

    # ── Saldos operador por actor ─────────────────────────────────────────────
    msaldo_oper_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Operador Banca',
    )
    msaldo_oper_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Operador Distribuidor',
    )
    msaldo_oper_cm = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Operador Comercializador / Bloque',
    )
    msaldo_cm = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Comercializador / Bloque (alt.)',
        help_text='Campo alternativo de saldo del Comercializador.',
    )

    # ── Auditoría ─────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Liquidación de SorteoArrejuntao'
        verbose_name_plural = 'Liquidaciones de Sorteos'
        unique_together = [('id_sorteo', 'id_lista', 'id_agencia', 'id_taquilla')]
        ordering = ['-id_sorteo', 'id_agencia']
        indexes = [
            models.Index(fields=['id_sorteo', 'id_banca'], name='idx_liq_sorteo_banca'),
            models.Index(fields=['id_sorteo', 'id_distribuidor'], name='idx_liq_sorteo_dis'),
            models.Index(fields=['id_sorteo', 'id_agencia'], name='idx_liq_sorteo_agc'),
        ]

    def __str__(self):
        return 'Liquidación SorteoArrejuntao {0} | Agencia {1} | Taquilla {2}'.format(
            self.id_sorteo, self.id_agencia, self.id_taquilla
        )

    def get_utilidad_neta(self):
        """Retorna la utilidad neta: venta - premios - todas las comisiones."""
        comisiones = (
            (self.mmonto_comision_com or 0) +
            (self.mmonto_regalia_com  or 0) +
            (self.mmonto_comision_ban or 0) +
            (self.mmonto_regalia_ban  or 0) +
            (self.mmonto_comision_dis or 0) +
            (self.mmonto_regalia_dis  or 0) +
            (self.mmonto_comision_agc or 0)
        )
        return self.mmonto_venta - self.mmonto_premios - comisiones

    def get_resumen_saldos(self):
        """Retorna dict con saldos de todos los actores para reportes."""
        return {
            'operador':       float(self.msaldo_oper or 0),
            'comercializador':float(self.msaldo_com  or 0),
            'banca':          float(self.msaldo_ban  or 0),
            'distribuidor':   float(self.msaldo_dis  or 0),
            'agencia':        float(self.msaldo_agc  or 0),
        }


# ─────────────────────────────────────────────────────────────────────────────
# Animalito — Catálogo de las 77 figuras del producto EL ARREJUNTAO
# ─────────────────────────────────────────────────────────────────────────────

class Animalito(models.Model):
    """
    Catálogo de los 77 animalitos/figuras del Sistema Asterisco Siete (*7).
    El número se almacena como texto para preservar el '0' y el '00'.
    """
    numero = models.CharField(
        max_length=2,
        unique=True,
        verbose_name='Número de Figura',
        help_text="'0', '00', '1'…'75'",
    )
    nombre = models.CharField(
        max_length=60,
        verbose_name='Nombre del Animal',
    )
    imagen = models.ImageField(
        upload_to='animalitos/',
        null=True,
        blank=True,
        verbose_name='Imagen',
        help_text='Ícono del animalito (PNG 64×64 recomendado).',
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Animalito'
        verbose_name_plural = 'Animalitos'
        ordering = ['id']

    def __str__(self):
        return '#{0} — {1}'.format(self.numero.zfill(2), self.nombre)


# ─────────────────────────────────────────────────────────────────────────────
# Ticket — Encabezado del ticket de venta
# ─────────────────────────────────────────────────────────────────────────────

class Ticket(models.Model):
    """
    Encabezado del comprobante de venta del Sistema Asterisco Siete (*7).
    Cada ticket agrupa N líneas de ApuestaDetalle de cualquier tipo de jugada.
    """

    serie = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Serie del Ticket',
        help_text='Identificador único generado por el sistema (ej. A7-20260328-0001).',
    )
    producto = models.ForeignKey(
        'admin_juego.ProductoLoteria',
        on_delete=models.CASCADE,
        related_name='tickets',
    )
    vendedor = models.ForeignKey(
        'admin_comercializacion.UsuariosTaquilla',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        help_text='Operador de taquilla que emitió el ticket.',
    )
    # ID del sorteo al que pertenece este ticket
    sorteo_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='ID SorteoArrejuntao',
    )
    fecha_emision = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Emisión',
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Total Bs.',
    )
    anulado = models.BooleanField(
        default=False,
        verbose_name='Anulado',
        db_index=True,
    )
    tserial_ifa = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Serial Impresora Fiscal (IFA)',
    )
    # Agencia y taquilla de origen
    id_agencia  = models.IntegerField(null=True, blank=True, verbose_name='ID Agencia')
    id_taquilla = models.IntegerField(null=True, blank=True, verbose_name='ID Taquilla')

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-fecha_emision']
        indexes = [
            models.Index(fields=['sorteo_id', 'anulado'], name='idx_ticket_sorteo_estado'),
        ]

    def __str__(self):
        estado = '🚫' if self.anulado else '✓'
        return '{0} Ticket {1} — Bs. {2}'.format(estado, self.serie, self.total)

    def calcular_total(self):
        """Recalcula y guarda el total sumando todas las apuestas activas."""
        from django.db.models import Sum
        total = self.apuestas.filter(estatus='P').aggregate(s=Sum('monto_apostado'))['s'] or 0
        self.total = total
        self.save(update_fields=['total'])
        return total

    def anular(self):
        """Anula el ticket y todas sus apuestas pendientes."""
        self.apuestas.filter(estatus='P').update(estatus='A')
        self.anulado = True
        self.save(update_fields=['anulado'])


# ─────────────────────────────────────────────────────────────────────────────
# ApuestaDetalle — Cada línea del ticket
# ─────────────────────────────────────────────────────────────────────────────

class ApuestaDetalle(models.Model):
    """
    Línea individual de apuesta dentro de un Ticket.

    El campo `numero_apostado` se define como CharField(max_length=5)
    para no perder ceros a la izquierda (ej. '007', '00', '01234').
    """

    TIPOS_JUEGO = [
        ('TRIPLE_A',       'Triple A'),
        ('TRIPLE_B',       'Triple B'),
        ('TERMINAL_A',     'Terminal A'),
        ('TERMINAL_B',     'Terminal B'),
        ('TRIPLE_SIGNO_A', 'Triple con Signo A'),
        ('TRIPLE_SIGNO_B', 'Triple con Signo B'),
        ('TERMINAL_SIGNO_A', 'Terminal con Signo A'),
        ('TERMINAL_SIGNO_B', 'Terminal con Signo B'),
        ('ARRIMAO',        'El Arrimao (4 dígitos)'),
        ('PAGADITO',       'El Pegadito (5 dígitos)'),
        ('ANIMALITO',      'Animalito (77 figuras)'),
    ]

    SIGNOS = [
        ('ARIES', 'Aries'), ('TAURO', 'Tauro'), ('GEMINIS', 'Géminis'),
        ('CANCER', 'Cáncer'), ('LEO', 'Leo'), ('VIRGO', 'Virgo'),
        ('LIBRA', 'Libra'), ('ESCORPIO', 'Escorpio'), ('SAGITARIO', 'Sagitario'),
        ('CAPRICORNIO', 'Capricornio'), ('ACUARIO', 'Acuario'), ('PISCIS', 'Piscis'),
    ]

    ESTADO = [
        ('P', 'Pendiente'),
        ('G', 'Ganador'),
        ('L', 'Perdedor'),
        ('A', 'Anulado'),
    ]

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='apuestas',
    )
    tipo_jugada = models.CharField(
        max_length=20,
        choices=TIPOS_JUEGO,
        verbose_name='Tipo de Jugada',
        db_index=True,
    )
    # CharField para preservar ceros a la izquierda: '007', '001', '00'
    numero_apostado = models.CharField(
        max_length=5,
        verbose_name='Número Apostado',
        help_text='Se guarda como texto para no perder los ceros (ej. "007").',
    )
    # Signo zodiacal (solo para tipo TRIPLE_SIGNO_* y TERMINAL_SIGNO_*)
    signo = models.CharField(
        max_length=15,
        choices=SIGNOS,
        null=True,
        blank=True,
        verbose_name='Signo Zodiacal',
    )
    # Relación al catálogo de animalitos (solo para ANIMALITO)
    animalito = models.ForeignKey(
        Animalito,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apuestas',
        help_text='Solo aplica para tipo de jugada ANIMALITO.',
    )
    monto_apostado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Monto Apostado Bs.',
    )
    monto_premio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Monto Premio Bs.',
    )
    estatus = models.CharField(
        max_length=1,
        choices=ESTADO,
        default='P',
        verbose_name='Estatus',
        db_index=True,
    )
    # Auditoría de liquidación
    liquidado_en = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Liquidación',
    )
    sistema_liquidacion = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        verbose_name='Sistema que liquidó',
    )

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Apuesta Detalle'
        verbose_name_plural = 'Apuestas Detalle'
        ordering = ['ticket', 'tipo_jugada']
        indexes = [
            models.Index(fields=['estatus', 'tipo_jugada'], name='idx_apuesta_estado_tipo'),
            models.Index(
                fields=['ticket', 'estatus'],
                name='idx_apuesta_ticket_estado',
            ),
        ]

    def __str__(self):
        return '{0} | {1} → {2} | Bs. {3} [{4}]'.format(
            self.ticket.serie,
            self.get_tipo_jugada_display(),
            self.numero_apostado,
            self.monto_apostado,
            self.get_estatus_display(),
        )

    # Helpers llamados por el motor de liquidación
    def marcar_como_ganador(self, sistema='Asterisco Siete (*7)'):
        from django.utils.timezone import now
        from admin_juego.constants_arrejuntao import get_factor_pago
        self.estatus = 'G'
        self.monto_premio = self.monto_apostado * get_factor_pago(self.tipo_jugada)
        self.liquidado_en = now()
        self.sistema_liquidacion = sistema
        self.save(update_fields=['estatus', 'monto_premio', 'liquidado_en', 'sistema_liquidacion'])

    def marcar_como_perdedor(self):
        from django.utils.timezone import now
        self.estatus = 'L'
        self.monto_premio = 0
        self.liquidado_en = now()
        self.save(update_fields=['estatus', 'monto_premio', 'liquidado_en'])


# ─────────────────────────────────────────────────────────────────────────────
# ResultadoSorteo — Resultados del sorteo (auto-dispara liquidación)
# ─────────────────────────────────────────────────────────────────────────────

class ResultadoSorteo(models.Model):
    """
    Registra los números ganadores de un sorteo de EL ARREJUNTAO.
    Al guardar, dispara automáticamente la liquidación de todas las
    apuestas pendientes asociadas al sorteo.
    """

    SIGNOS = ApuestaDetalle.SIGNOS

    producto = models.ForeignKey(
        'admin_juego.ProductoLoteria',
        on_delete=models.CASCADE,
        related_name='resultados',
    )
    sorteo_id = models.IntegerField(
        unique=True,
        db_index=True,
        verbose_name='ID SorteoArrejuntao',
    )
    fecha_sorteo = models.DateTimeField(
        verbose_name='Fecha y Hora del SorteoArrejuntao',
    )

    # ── Resultados ganadores ───────────────────────────────────────────────
    res_triple_a = models.CharField(
        max_length=3,
        verbose_name='Triple A Ganador',
        help_text='3 dígitos (ej. 123).',
    )
    res_triple_b = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name='Triple B Ganador',
        help_text='3 dígitos. Opcional si el producto usa doble cara.',
    )
    res_signo = models.CharField(
        max_length=15,
        choices=SIGNOS,
        blank=True,
        null=True,
        verbose_name='Signo Zodiacal Ganador',
    )
    res_animalito = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        verbose_name='Animalito Ganador',
        help_text='Número de figura (0, 00, 1…75).',
    )
    res_cuatro_cifras = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name='El Arrimao (4 dígitos)',
    )
    res_cinco_cifras = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name='El Pegadito (5 dígitos)',
    )

    # ── Estado de liquidación ──────────────────────────────────────────────
    liquidado = models.BooleanField(
        default=False,
        verbose_name='¿Liquidado?',
        db_index=True,
    )
    liquidado_en = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Liquidación',
    )
    stats_liquidacion = JSONField(
        default=dict,
        verbose_name='Estadísticas de Liquidación',
        help_text='Resumen JSON del proceso: total, ganadoras, perdedoras.',
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Resultado de SorteoArrejuntao'
        verbose_name_plural = 'Resultados de Sorteos'
        ordering = ['-fecha_sorteo']

    def __str__(self):
        estado = '✅' if self.liquidado else '⏳'
        return '{0} SorteoArrejuntao {1} — {2}'.format(
            estado, self.sorteo_id, self.fecha_sorteo.strftime('%d/%m/%Y %H:%M')
        )

    def get_resultados_dict(self):
        """Retorna el diccionario de resultados para el motor de liquidación."""
        return {
            'triple_a':       self.res_triple_a or '',
            'triple_b':       self.res_triple_b or self.res_triple_a or '',
            'signo':          self.res_signo or '',
            'cuatro_digitos': self.res_cuatro_cifras or '',
            'cinco_digitos':  self.res_cinco_cifras or '',
            'animalito':      self.res_animalito or '',
        }

    def liquidar_apuestas(self):
        """
        Motor de liquidación: evalúa todas las apuestas pendientes
        del sorteo y las marca como Ganadoras o Perdedoras.
        Se llama automáticamente vía signal post_save.
        """
        from django.utils.timezone import now
        from admin_juego.views.liquidacion_arrejuntao_views import liquidar_arrejuntao

        if self.liquidado:
            return  # No reliquidar

        apuestas = ApuestaDetalle.objects.filter(
            ticket__sorteo_id=self.sorteo_id,
            ticket__anulado=False,
            estatus='P',
        )

        resultados = self.get_resultados_dict()
        stats = liquidar_arrejuntao(self.sorteo_id, resultados, apuestas)

        self.liquidado = True
        self.liquidado_en = now()
        self.stats_liquidacion = stats
        self.save(update_fields=['liquidado', 'liquidado_en', 'stats_liquidacion'])
        return stats


# ─────────────────────────────────────────────────────────────────────────────
# LimiteCentro — Límites operativos por Centro de Apuesta (Agencia)
# ─────────────────────────────────────────────────────────────────────────────

class LimiteCentro(models.Model):
    """
    Define los límites operativos para un Centro de Apuesta (Agencia).

    Permite controlar:
        - Máximo de tickets emitidos por día
        - Monto máximo de venta diaria
    """

    agencia = models.ForeignKey(
        'admin_comercializacion.Agencias',
        on_delete=models.CASCADE,
        related_name='limites',
        verbose_name='Centro de Apuesta',
    )
    max_tickets_diarios = models.PositiveIntegerField(
        default=0,
        verbose_name='Máximo de tickets diarios',
        help_text='0 = sin límite',
    )
    monto_maximo_diario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Monto máximo diario',
        help_text='0.00 = sin límite de monto',
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Límite del Centro'
        verbose_name_plural = 'Límites del Centro'
        ordering = ['agencia']

    def __str__(self):
        return 'Límite {0}: max={1} tickets / Bs.{2}/día'.format(
            self.agencia,
            self.max_tickets_diarios or '∞',
            self.monto_maximo_diario or '∞',
        )
@receiver(post_save, sender=ResultadoSorteo)
def auto_liquidar_on_save(sender, instance, created, **kwargs):
    """
    Signal: cuando se guarda un ResultadoSorteo nuevo (no liquidado),
    dispara automáticamente la liquidación de apuestas.
    """
    if created and not instance.liquidado:
        instance.liquidar_apuestas()


# =============================================================================
# ARQUITECTURA MULTI-PRODUCTO — Sistema Asterisco Siete (*7)
# =============================================================================
# Jerarquía:
#   Loteria  →  ProductoLoteria  →  SorteoArrejuntao
#                    ↕
#             GrupoAnimales  →  Animalito (reutiliza el modelo ya definido)
#
# Ventaja: crear "Triple Táchira", "Lotto 40 Figuras", etc. desde el panel
#          de administración sin tocar una sola línea de código.
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
# Loteria — La entidad madre
# ─────────────────────────────────────────────────────────────────────────────

class Loteria(models.Model):
    """
    Representa una lotería o ente emisor.
    Ejemplos: 'Triple Táchira', 'Lotto Activo', 'El Arrejuntao'.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre de la Lotería',
    )
    logo = models.ImageField(
        upload_to='loterias/',
        null=True,
        blank=True,
        verbose_name='Logo',
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activa',
        db_index=True,
    )
    orden = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Orden de presentación',
    )
    sistema = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='ID Sistema de Juego',
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Lotería'
        verbose_name_plural = 'Loterías'
        ordering = ['orden', 'nombre']

    def __str__(self):
        estado = '✓' if self.activo else '✗'
        return '[{0}] {1}'.format(estado, self.nombre)

    def get_productos_activos(self):
        """Retorna los productos activos de esta lotería."""
        return self.productos.filter(activo=True).order_by('orden')


# ─────────────────────────────────────────────────────────────────────────────
# GrupoAnimales — Set de animalitos reutilizable entre productos
# ─────────────────────────────────────────────────────────────────────────────

class GrupoAnimales(models.Model):
    """
    Agrupa un catálogo de animalitos.
    Ejemplos:
        'Set El Arrejuntao (77 figuras)'  → figuras 0-75 + 00
        'Set Tradicional (38 figuras)'    → figuras 1-38
        'Set Express (20 figuras)'        → figuras 1-20

    Permite que distintos productos usen conjuntos diferentes de animales.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del Set',
        help_text='Ej: "Set El Arrejuntao (77)", "Set Tradicional (38)"',
    )
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Grupo de Animalitos'
        verbose_name_plural = 'Grupos de Animalitos'
        ordering = ['nombre']

    def __str__(self):
        return '{0} ({1} figuras)'.format(
            self.nombre,
            self.animales.filter(activo=True).count(),
        )


class AnimalFigura(models.Model):
    """
    Figura de animalito perteneciente a un GrupoAnimales.
    Permite tener 'Perico' en el Set-77 con número '7'
    y 'Perico' en cualquier otro set con un número diferente.
    """
    grupo = models.ForeignKey(
        GrupoAnimales,
        on_delete=models.CASCADE,
        related_name='animales',
    )
    numero = models.CharField(
        max_length=3,
        verbose_name='Número de Figura',
        help_text="'0', '00', '1'…'75'",
    )
    nombre = models.CharField(max_length=60, verbose_name='Nombre')
    imagen = models.ImageField(
        upload_to='animalitos/',
        null=True,
        blank=True,
        verbose_name='Imagen (PNG 64×64)',
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'Figura de Animalito'
        verbose_name_plural = 'Figuras de Animalitos'
        unique_together = [('grupo', 'numero')]
        ordering = ['grupo', 'numero']

    def __str__(self):
        return '#{num} {nombre} [{grupo}]'.format(
            num=self.numero.zfill(2),
            nombre=self.nombre,
            grupo=self.grupo.nombre,
        )


# ─────────────────────────────────────────────────────────────────────────────
# ProductoLoteria — Reglas de cada tipo de juego (configurable desde admin)
# ─────────────────────────────────────────────────────────────────────────────

class ProductoLoteria(models.Model):
    """
    Define las reglas de un tipo de juego dentro de una Lotería.

    Ejemplo para 'Triple Táchira':
        loteria            = Lotería "Triple Táchira"
        nombre_producto    = "Triple A"
        tipo               = NUMERICO
        digitos_requeridos = 3
        es_terminal        = False
        requiere_signo     = False
        multiplicador_pago = 400.00

    Ejemplo para 'Terminal con Signo - Arrejuntao':
        tipo               = NUMERICO
        digitos_requeridos = 2
        es_terminal        = True
        requiere_signo     = True
        multiplicador_pago = 25.00
        resultado_key      = 'triple_a'

    Ejemplo para 'Animalitos Express (20 figuras)':
        tipo               = ANIMALITOS
        grupo_animales     = GrupoAnimales "Set Express (20)"
        multiplicador_pago = 30.00
    """

    TIPOS = [
        ('NUMERICO',   'Numérico (Triples / Terminal / Arrimao / Pagadito)'),
        ('ANIMALITOS', 'Animalitos (por figura)'),
    ]

    RESULTADO_KEYS = [
        ('triple_a',       'Triple A'),
        ('triple_b',       'Triple B'),
        ('cuatro_digitos', 'Arrimao (4 dígitos)'),
        ('cinco_digitos',  'Pegadito (5 dígitos)'),
        ('animalito',      'Animalito'),
    ]

    loteria = models.ForeignKey(
        Loteria,
        on_delete=models.CASCADE,
        related_name='productos',
    )
    nombre_producto = models.CharField(
        max_length=100,
        verbose_name='Nombre del Tipo de Producto',
        help_text='Ej: "Triple A", "Terminal con Signo", "Animalitos 77".',
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        verbose_name='Tipo de TipoProducto',
    )
    activo = models.BooleanField(default=True, verbose_name='Activo', db_index=True)
    orden = models.PositiveSmallIntegerField(default=0, verbose_name='Orden')

    # ── Reglas para tipo NUMERICO ─────────────────────────────────────────────
    digitos_requeridos = models.IntegerField(
        default=3,
        verbose_name='Dígitos requeridos',
        help_text='2=Terminal, 3=Triple, 4=Arrimao, 5=Pegadito.',
    )
    es_terminal = models.BooleanField(
        default=False,
        verbose_name='¿Es Terminal?',
        help_text='Si True, compara los últimos N dígitos del resultado.',
    )
    requiere_signo = models.BooleanField(
        default=False,
        verbose_name='¿Requiere Signo Zodiacal?',
    )
    # Clave del resultado con el que se compara (de get_resultados_dict)
    resultado_key = models.CharField(
        max_length=30,
        choices=RESULTADO_KEYS,
        default='triple_a',
        verbose_name='Fuente de Resultado',
        help_text='Campo del resultado del sorteo con el que se compara la apuesta.',
    )

    # ── Reglas para tipo ANIMALITOS ────────────────────────────────────────────
    grupo_animales = models.ForeignKey(
        GrupoAnimales,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos',
        help_text='Solo para tipo ANIMALITOS.',
    )

    # ── Pago ──────────────────────────────────────────────────────────────────
    multiplicador_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Multiplicador de Pago',
        help_text='Ej: 400 para Triple, 8 para Animalito, 3000 para Arrimao.',
    )
    cupo_por_numero = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Cupo máximo por número',
        help_text='0 = sin límite de cupo.',
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'TipoProducto de Lotería'
        verbose_name_plural = 'Productos de Lotería'
        unique_together = [('loteria', 'nombre_producto')]
        ordering = ['loteria', 'orden', 'nombre_producto']

    def __str__(self):
        return '{0} — {1} (×{2})'.format(
            self.loteria.nombre,
            self.nombre_producto,
            self.multiplicador_pago,
        )

    def calcular_premio(self, monto_apostado):
        """Calcula el monto del premio para una apuesta ganadora."""
        return monto_apostado * self.multiplicador_pago

    @property
    def producto(self):
        """
        Nombre del producto/marca al que pertenece esta modalidad.
        Por defecto 'EL ARREJUNTAO'. En el futuro puede leerse de un campo
        o de la lotería padre.
        """
        return 'EL ARREJUNTAO'

    @property
    def tipo_label(self):
        """Etiqueta legible del tipo de producto para el dashboard."""
        labels = {
            'NUMERICO':   'Números',
            'ANIMALITOS': 'Figuras',
        }
        return labels.get(self.tipo, self.tipo)


# ─────────────────────────────────────────────────────────────────────────────
# SorteoArrejuntao — Horarios/instancias de sorteo de un producto
# ─────────────────────────────────────────────────────────────────────────────

class SorteoArrejuntao(models.Model):
    """
    Define un horario de sorteo dentro de un ProductoLoteria.
    Ejemplo:
        TipoProducto: "Triple Táchira"  →  SorteoArrejuntao: "1:00 PM Matutino"
        TipoProducto: "Triple Táchira"  →  SorteoArrejuntao: "4:00 PM Vespertino"
        TipoProducto: "Triple Táchira"  →  SorteoArrejuntao: "7:00 PM Nocturno"
    """
    producto = models.ForeignKey(
        ProductoLoteria,
        on_delete=models.CASCADE,
        related_name='sorteos',
    )
    descripcion = models.CharField(
        max_length=80,
        verbose_name='Descripción',
        help_text='Ej: "1:00 PM - Matutino"',
    )
    hora_sorteo = models.TimeField(
        verbose_name='Hora del SorteoArrejuntao',
    )
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        db_index=True,
    )
    # Cierre de venta: minutos antes del sorteo en que se bloquea la venta
    minutos_cierre = models.PositiveSmallIntegerField(
        default=15,
        verbose_name='Minutos de cierre previo',
        help_text='La venta se bloquea N minutos antes del sorteo.',
    )

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = 'SorteoArrejuntao'
        verbose_name_plural = 'Sorteos'
        unique_together = [('producto', 'hora_sorteo')]
        ordering = ['producto', 'hora_sorteo']

    def __str__(self):
        return '{0} | {1} ({2})'.format(
            self.producto.loteria.nombre,
            self.descripcion,
            self.hora_sorteo.strftime('%H:%M'),
        )

    def esta_abierto(self):
        """
        Retorna True si la venta está abierta para este sorteo
        (faltan más de `minutos_cierre` para el sorteo).
        """
        from datetime import datetime, timedelta
        from django.utils.timezone import localtime, now
        ahora = localtime(now()).time()
        cierre = (
            datetime.combine(datetime.today(), self.hora_sorteo)
            - timedelta(minutes=self.minutos_cierre)
        ).time()
        return ahora < cierre


# ─────────────────────────────────────────────────────────────────────────────
# Motor de liquidación DINÁMICO — lee las reglas desde ProductoLoteria
# ─────────────────────────────────────────────────────────────────────────────

def liquidar_dinamico(sorteo_pk, resultados, apuestas_qs=None):
    """
    Motor de liquidación dinámico para el Sistema Asterisco Siete (*7).

    Lee las reglas del ProductoLoteria asociado al SorteoArrejuntao y evalúa
    cada apuesta sin lógica hardcodeada.

    Args:
        sorteo_pk  (int): PK del objeto SorteoArrejuntao en la BD
        resultados (dict): {
            'triple_a': '123', 'triple_b': '456',
            'signo': 'ARIES', 'cuatro_digitos': '1234',
            'cinco_digitos': '12345', 'animalito': '37'
        }
        apuestas_qs: QuerySet de ApuestaDetalle con estatus='P'.
                     Si None, funciona en modo simulación.

    Returns:
        dict con estadísticas: total, ganadoras, perdedoras, errores.
    """
    try:
        sorteo_obj = SorteoArrejuntao.objects.select_related('producto__loteria').get(pk=sorteo_pk)
    except SorteoArrejuntao.DoesNotExist:
        return {'error': 'SorteoArrejuntao {0} no existe.'.format(sorteo_pk)}

    producto = sorteo_obj.producto
    stats = {
        'sorteo_pk':  sorteo_pk,
        'loteria':    producto.loteria.nombre,
        'producto':   producto.nombre_producto,
        'tipo':       producto.tipo,
        'resultados': resultados,
        'total': 0, 'ganadoras': 0, 'perdedoras': 0, 'errores': 0,
        'modo': 'simulacion' if apuestas_qs is None else 'produccion',
        'detalle': [],
    }

    if apuestas_qs is None:
        return stats

    for apuesta in apuestas_qs:
        stats['total'] += 1
        try:
            es_ganador = False
            descripcion = ''

            if producto.tipo == 'NUMERICO':
                # Obtener el número resultado según la fuente configurada
                num_resultado = resultados.get(producto.resultado_key, '')

                if not num_resultado:
                    descripcion = 'Sin resultado para key={0}'.format(producto.resultado_key)
                else:
                    # Comparar los últimos N dígitos (Terminal) o exacto (Triple, Arrimao)
                    num_comparar = (
                        num_resultado[-producto.digitos_requeridos:]
                        if producto.es_terminal
                        else num_resultado
                    )
                    gana_num = apuesta.numero_apostado == num_comparar

                    # Si requiere signo, también debe coincidir
                    if producto.requiere_signo:
                        gana_signo = (
                            (apuesta.signo or '').upper() ==
                            (resultados.get('signo', '') or '').upper()
                        )
                        es_ganador = gana_num and gana_signo
                        descripcion = 'Número: {0}={1} / Signo: {2}={3}'.format(
                            apuesta.numero_apostado, num_comparar,
                            apuesta.signo, resultados.get('signo'),
                        )
                    else:
                        es_ganador = gana_num
                        descripcion = 'Número: {0} vs {1}'.format(
                            apuesta.numero_apostado, num_comparar
                        )

            elif producto.tipo == 'ANIMALITOS':
                num_resultado = resultados.get('animalito', '')
                es_ganador = str(apuesta.numero_apostado) == str(num_resultado)
                descripcion = 'Figura: {0} vs {1}'.format(
                    apuesta.numero_apostado, num_resultado
                )

            # Marcar resultado
            if es_ganador:
                stats['ganadoras'] += 1
                # Calcular premio con el multiplicador del producto
                from decimal import Decimal
                apuesta.monto_premio = (
                    Decimal(str(apuesta.monto_apostado)) *
                    Decimal(str(producto.multiplicador_pago))
                )
                apuesta.estatus = 'G'
                apuesta.save(update_fields=['estatus', 'monto_premio'])
            else:
                stats['perdedoras'] += 1
                apuesta.estatus = 'L'
                apuesta.monto_premio = 0
                apuesta.save(update_fields=['estatus', 'monto_premio'])

            stats['detalle'].append({
                'apuesta_id': apuesta.pk,
                'tipo':       producto.nombre_producto,
                'numero':     apuesta.numero_apostado,
                'gana':       es_ganador,
                'info':       descripcion,
            })

        except Exception as exc:
            stats['errores'] += 1
            stats['detalle'].append({'apuesta_id': getattr(apuesta, 'pk', None), 'error': str(exc)})

    return stats

