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
