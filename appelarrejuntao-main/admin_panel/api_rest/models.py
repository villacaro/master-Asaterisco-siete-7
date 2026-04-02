"""
api_rest/models.py  –  Control de sorteos y cupos
"""
from django.db import models
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class ControlSorteo(models.Model):
    SORTEOS = [
        ('triple_a',       'Triple A'),
        ('triple_b',       'Triple B'),
        ('triple_signo',   'Triple + Signo'),
        ('el_arrimao',     'El Arrimao'),
        ('el_pegadito',    'El Pegadito'),
        ('animalito',      'Animalito'),
        ('terminal_a',     'Terminal A'),
        ('terminal_b',     'Terminal B'),
        ('triple_c',       'Triple C'),
        ('terminal_c',     'Terminal C'),
        ('terminal_signo', 'Terminal + Signo'),
    ]

    HORARIOS = [
        ('10:00 AM', '10:00 AM'),
        ('01:00 PM', '01:00 PM'),
        ('04:00 PM', '04:00 PM'),
        ('07:00 PM', '07:00 PM'),
        ('11:00 PM', '11:00 PM'),
    ]

    sorteo        = models.CharField(max_length=40, choices=SORTEOS, verbose_name='Sorteo')
    horario       = models.CharField(max_length=20, choices=HORARIOS, verbose_name='Horario')
    abierto       = models.BooleanField(default=True, verbose_name='Abierto')
    cupo_venta    = models.PositiveIntegerField(
        default=0, help_text='0 = sin límite de cupo', verbose_name='Cupo de Venta'
    )
    ventas_hoy    = models.PositiveIntegerField(default=0, verbose_name='Ventas Hoy')
    fecha_apertura = models.DateTimeField(null=True, blank=True, verbose_name='Fecha/Hora de Apertura')
    fecha_cierre   = models.DateTimeField(null=True, blank=True, verbose_name='Fecha/Hora de Cierre')
    notas          = models.TextField(blank=True, verbose_name='Notas')
    actualizado    = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name        = 'Control de Sorteo'
        verbose_name_plural = 'Control de Sorteos'
        ordering            = ['sorteo', 'horario']
        unique_together     = [('sorteo', 'horario')]

    def __str__(self):
        estado   = '🟢 ABIERTO' if self.abierto else '🔴 CERRADO'
        cupo_txt = f' | Cupo: {self.cupo_venta}' if self.cupo_venta > 0 else ' | Sin límite'
        return f'{self.get_sorteo_display()} [{self.horario}] – {estado}{cupo_txt}'

    @property
    def cupo_disponible(self):
        if not self.abierto:
            return False
        if self.cupo_venta == 0:
            return True
        return self.ventas_hoy < self.cupo_venta

    # ── Sync a Firestore ──────────────────────────────────────────
    def sync_firestore(self):
        """Escribe el estado actual a Firestore para que las apps lo lean."""
        try:
            from usuarios import firebase_service as fb
            if not fb._init_firebase():
                return
            from firebase_admin import firestore
            db     = firestore.client()
            doc_id = f'{self.sorteo}_{self.horario.replace(":", "").replace(" ", "_")}'
            db.collection('control_sorteos').document(doc_id).set({
                'id':              self.id,
                'sorteo':          self.sorteo,
                'sorteo_nombre':   self.get_sorteo_display(),
                'horario':         self.horario,
                'abierto':         self.abierto,
                'cupo_venta':      self.cupo_venta,
                'ventas_hoy':      self.ventas_hoy,
                'cupo_disponible': self.cupo_disponible,
                'notas':           self.notas,
                'updated_at':      firestore.SERVER_TIMESTAMP,
            })
            logger.info(f'Firestore sync OK: {doc_id}')
        except Exception as e:
            logger.warning(f'Firestore sync failed: {e}')

    def save(self, *args, **kwargs):
        # Registrar timestamps automáticos
        if not self.abierto and not self.fecha_cierre:
            self.fecha_cierre = timezone.now()
        if self.abierto:
            self.fecha_cierre = None
            if not self.fecha_apertura:
                self.fecha_apertura = timezone.now()
        super().save(*args, **kwargs)
        self.sync_firestore()

    def abrir(self):
        self.abierto        = True
        self.fecha_apertura = timezone.now()
        self.fecha_cierre   = None
        self.save()

    def cerrar(self):
        self.abierto      = False
        self.fecha_cierre = timezone.now()
        self.save()


class ControlSorteoMatriz(ControlSorteo):
    """Proxy model que aparece en el menu del admin como 'Vista Matriz'."""
    class Meta:
        proxy               = True
        verbose_name        = '📊 Vista Matriz de Sorteos'
        verbose_name_plural = '📊 Vista Matriz de Sorteos'


# ════════════════════════════════════════════════════════════════
# MÓDULO VENTAS
# ════════════════════════════════════════════════════════════════

class TransaccionVenta(models.Model):
    """Registra cada apuesta/venta de ticket."""
    MODALIDADES = [
        ('triple_a',     'Triple A'),
        ('triple_b',     'Triple B'),
        ('triple_signo', 'Triple + Signo'),
        ('el_arrimao',   'El Arrimao'),
        ('el_pegadito',  'El Pegadito'),
        ('animalito',    'Animalito'),
        ('terminal_a',   'Terminal A'),
        ('terminal_b',   'Terminal B'),
    ]
    HORARIOS = [
        ('10:00 AM', '10:00 AM'),
        ('01:00 PM', '01:00 PM'),
        ('04:00 PM', '04:00 PM'),
        ('07:00 PM', '07:00 PM'),
        ('11:00 PM', '11:00 PM'),
    ]
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('ganador',   'Ganador'),
        ('perdedor',  'Perdedor'),
        ('anulado',   'Anulado'),
    ]

    fecha        = models.DateField(default=timezone.now, verbose_name='Fecha')
    horario      = models.CharField(max_length=20, choices=HORARIOS, verbose_name='Horario')
    modalidad    = models.CharField(max_length=30, choices=MODALIDADES, verbose_name='Modalidad')
    numero       = models.CharField(max_length=10, verbose_name='Número Apostado')
    monto        = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto Bs')
    taquillero   = models.CharField(max_length=80, blank=True, verbose_name='Taquillero')
    ticket_ref   = models.CharField(max_length=40, blank=True, verbose_name='Ref. Ticket')
    estado       = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    notas        = models.TextField(blank=True, verbose_name='Notas')
    creado       = models.DateTimeField(auto_now_add=True)
    actualizado  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Transacción de Venta'
        verbose_name_plural = 'Transacciones de Venta'
        ordering            = ['-creado']

    def __str__(self):
        return f'[{self.fecha}] {self.get_modalidad_display()} #{self.numero} – Bs.{self.monto} ({self.taquillero})'


# ════════════════════════════════════════════════════════════════
# MÓDULO PAGOS
# ════════════════════════════════════════════════════════════════

class Pago(models.Model):
    """Registra cobros de taquilleros (pago de ventas al sistema)."""
    METODOS = [
        ('efectivo',    'Efectivo'),
        ('transferencia', 'Transferencia Bancaria'),
        ('mobile',      'Pago Móvil'),
        ('zelle',       'Zelle'),
        ('cripto',      'Criptomoneda'),
        ('otro',        'Otro'),
    ]
    ESTADOS = [
        ('pendiente',   'Pendiente'),
        ('confirmado',  'Confirmado'),
        ('rechazado',   'Rechazado'),
    ]

    fecha         = models.DateField(default=timezone.now, verbose_name='Fecha')
    taquillero    = models.CharField(max_length=80, verbose_name='Taquillero')
    monto         = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Monto Bs')
    metodo        = models.CharField(max_length=25, choices=METODOS, default='efectivo', verbose_name='Método de Pago')
    referencia    = models.CharField(max_length=80, blank=True, verbose_name='Referencia / Comprobante')
    estado        = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    periodo_desde = models.DateField(null=True, blank=True, verbose_name='Período Desde')
    periodo_hasta = models.DateField(null=True, blank=True, verbose_name='Período Hasta')
    notas         = models.TextField(blank=True, verbose_name='Notas')
    confirmado_por = models.CharField(max_length=80, blank=True, verbose_name='Confirmado por')
    creado        = models.DateTimeField(auto_now_add=True)
    actualizado   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Pago de Taquillero'
        verbose_name_plural = 'Pagos de Taquilleros'
        ordering            = ['-creado']

    def __str__(self):
        return f'[{self.fecha}] {self.taquillero} – Bs.{self.monto} ({self.get_estado_display()})'


# ════════════════════════════════════════════════════════════════
# MÓDULO PREMIOS
# ════════════════════════════════════════════════════════════════

class PremioPagado(models.Model):
    """Registra el pago de premios a ganadores."""
    MODALIDADES = TransaccionVenta.MODALIDADES
    HORARIOS    = TransaccionVenta.HORARIOS
    ESTADOS = [
        ('pendiente',   'Pendiente de Pago'),
        ('pagado',      'Pagado'),
        ('rechazado',   'Rechazado / No Válido'),
        ('en_proceso',  'En Proceso de Verificación'),
    ]

    fecha         = models.DateField(default=timezone.now, verbose_name='Fecha Sorteo')
    horario       = models.CharField(max_length=20, choices=HORARIOS, verbose_name='Horario Sorteo')
    modalidad     = models.CharField(max_length=30, choices=MODALIDADES, verbose_name='Modalidad')
    numero_ganador = models.CharField(max_length=10, verbose_name='Número Ganador')
    ticket_ref    = models.CharField(max_length=40, blank=True, verbose_name='Ref. Ticket')
    ganador_nombre = models.CharField(max_length=120, verbose_name='Nombre del Ganador')
    ganador_id    = models.CharField(max_length=30, blank=True, verbose_name='Cédula / ID Ganador')
    taquillero    = models.CharField(max_length=80, blank=True, verbose_name='Taquillero')
    monto_apuesta = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto Apostado Bs')
    multiplicador = models.DecimalField(max_digits=8, decimal_places=2, default=70, verbose_name='Multiplicador Premio')
    monto_premio  = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Monto Premio Bs')
    estado        = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    pagado_por    = models.CharField(max_length=80, blank=True, verbose_name='Pagado por')
    fecha_pago    = models.DateTimeField(null=True, blank=True, verbose_name='Fecha/Hora de Pago')
    notas         = models.TextField(blank=True, verbose_name='Notas')
    creado        = models.DateTimeField(auto_now_add=True)
    actualizado   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Premio Pagado'
        verbose_name_plural = 'Premios Pagados'
        ordering            = ['-creado']

    def __str__(self):
        return f'[{self.fecha}] {self.get_modalidad_display()} #{self.numero_ganador} → {self.ganador_nombre} – Bs.{self.monto_premio}'

    def save(self, *args, **kwargs):
        # Auto-calcular monto premio si no está definido
        if not self.monto_premio and self.monto_apuesta and self.multiplicador:
            self.monto_premio = self.monto_apuesta * self.multiplicador
        # Registrar fecha de pago
        if self.estado == 'pagado' and not self.fecha_pago:
            self.fecha_pago = timezone.now()
        super().save(*args, **kwargs)
