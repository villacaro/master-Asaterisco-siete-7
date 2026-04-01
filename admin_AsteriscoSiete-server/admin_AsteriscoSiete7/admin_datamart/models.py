# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_asterisco7.settings import CACHES_CONF_TIME
from admin_lib.util_models import ProtectDelete
from django.core.cache import cache
from django.db import models


class DimensionTiempo(ProtectDelete, models.Model):
    """DimensionTiempo: Dimension de tiempo

    Campos definidos:
        fecha(date): define la fecha de la dimencion

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True
    fecha = models.DateField(
        db_index=True
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Dimension de tiempo')
        verbose_name_plural = ('Dimension de tiempos')

    @staticmethod
    def get_dimension_tiempo(fecha):
        dimension = cache.get('get_dimension_tiempo_{0}'.format(fecha))
        if not dimension:
            try:
                dimension = DimensionTiempo.objects.get_or_create(
                    fecha=fecha
                )[0]
            except DimensionTiempo.MultipleObjectsReturned:
                # procesar flush
                dimensiones = DimensionTiempo.objects.filter(
                    fecha=fecha
                ).order_by('id')
                dimension = dimensiones[0]
                for obj in dimensiones[1:]:
                    obj.replace_related(replace=dimension)
                    obj.delete()

            cache.set(
                'get_dimension_tiempo_{0}'.format(fecha),
                dimension,
                CACHES_CONF_TIME['registros_db']['workers']
            )
        return dimension

    def replace_related(self, replace):
        """
        Cambia de relacion los hechos relacionados a la dimension invalidad
        """
        for related in self._meta.get_all_related_objects():
            related_set = getattr(self, related.get_accessor_name())
            related_set.all().update(tiempo_id=replace.pk)


class DimensionComercializacion(ProtectDelete, models.Model):
    """DimensionComercializacion: Dimension de comercializacion

    Campos definidos:
        operadora_id(entero): hace referencia al foraneo del operadora

        bloque_id(entero): hace referencia al foraneo del bloque

        banca_id(entero): hace referencia al foraneo de la banca

        distribuidor_id(entero): hace referencia al foraneo del distribuidor

        agencia_id(entero): hace referencia al foraneo de la agencia

        taquilla_id(entero): hace referencia al foraneo de la taquilla

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    operadora_id = models.IntegerField()
    bloque_id = models.IntegerField()
    banca_id = models.IntegerField()
    distribuidor_id = models.IntegerField()
    agencia_id = models.IntegerField()
    taquilla_id = models.IntegerField(
        db_index=True,
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Dimension de comercializacion')
        verbose_name_plural = ('Dimension de comercializaciones')


class DimensionJuegos(ProtectDelete, models.Model):
    """DimensionJuegos: Dimension de juegos

    Campos definidos:
        deporte_id(entero): hace referencia al foraneo del deporte

        torneo_id(entero): hace referencia al foraneo del torneo

        temporada_id(entero): hace referencia al foraneo de la temporada

        jornada_id(entero): hace referencia al foraneo de la jornada

        encuentro_id(entero): hace referencia al foraneo del encuentro

        encuentros_modalidad_id(entero): hace referencia al foraneo del encuentros_modalidad

        modalidad_id(entero): hace referencia al foraneo de la modalidad

        condicion_id(entero): hace referencia al foraneo de la condicion

        pertenece_id(strin): hace referencia al foraneo del pertenece en un encuentro

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    deporte_id = models.IntegerField()
    torneo_id = models.IntegerField()
    temporada_id = models.IntegerField()
    jornada_id = models.IntegerField()
    encuentro_id = models.IntegerField()
    encuentros_modalidad_id = models.IntegerField()
    modalidad_id = models.IntegerField()
    condicion_id = models.IntegerField()
    pertenece = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Dimension de juego')
        verbose_name_plural = ('Dimension de juegos')


class DimensionJuegosNew(ProtectDelete, models.Model):
    """DimensionJuegosNew: Dimensión de juegos optimizada para Loterías

    Campos definidos para Sistema Asterisco siete (*7):

        sistema_id: ID del sistema Asterisco siete
        loteria_id: ID de la operadora (Zulia, Táchira, Cojedes, etc.)
        producto_id: ID del producto base (EL ARREJUNTAO, EL ARRIMAO)
        sorteo_id: ID del sorteo específico (Hora/Fecha)
        horario_id: ID del bloque horario (Matutino, Vespertino, Nocturno)
        modalidad_id: ID del tipo (Triple, Terminal, Animalito)
        sub_modalidad_id: ID de variante (Triple A, Triple B, Signo)
        numero_apostado: número de 1-5 cifras o ID de animalito
        signo_id: ID del signo zodiacal si aplica
        animalito_id: ID de la figura (0-75)
        grupo_agencia_id: ID del grupo o zona de ventas
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    sistema_id = models.IntegerField(
        db_index=True,
        help_text="ID del sistema Asterisco siete (*7)"
    )

    # ── Jerarquía de Lotería ──────────────────────────────────────────────────
    loteria_id = models.IntegerField(
        db_index=True,
        help_text="ID de la operadora (Zulia, Táchira, Cojedes, etc.)"
    )
    producto_id = models.IntegerField(
        db_index=True,
        help_text="ID del producto base (EL ARREJUNTAO, EL ARRIMAO, etc.)"
    )

    # ── Tiempo y Sorteo ───────────────────────────────────────────────────────
    sorteo_id = models.IntegerField(
        db_index=True,
        help_text="ID del sorteo específico (Hora/Fecha)"
    )
    horario_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID del bloque horario (Matutino, Vespertino, Nocturno)"
    )

    # ── Detalles de la Jugada ─────────────────────────────────────────────────
    modalidad_id = models.IntegerField(
        db_index=True,
        help_text="ID del tipo de jugada (Triple, Terminal, Animalito)"
    )
    sub_modalidad_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID de variante (Triple A, Triple B, Signo)"
    )

    # ── Selección del Cliente ─────────────────────────────────────────────────
    numero_apostado = models.CharField(
        max_length=5,
        db_index=True,
        help_text="Número de 1 a 5 cifras o ID de animalito (0-75)"
    )
    signo_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID del signo zodiacal si aplica"
    )
    animalito_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ID de la figura de animalito (0-75)"
    )

    # ── Clasificación de Venta ────────────────────────────────────────────────
    grupo_agencia_id = models.IntegerField(
        db_index=True,
        help_text="ID del grupo o zona de ventas"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = "Dimensión de Lotería"
        verbose_name_plural = "Dimensiones de Lotería"


class DimensionArcoComercializacion(ProtectDelete, models.Model):
    """DimensionArcoComercializacion: Dimension de un arco de comercializacion

    Campos definidos:

        operadora_id(entero): hace referencia al foraneo del operadora

        bloque_id(entero): hace referencia al foraneo del bloque

        banca_id(entero): hace referencia al foraneo de la banca

        distribuidor_id(entero): hace referencia al foraneo del distribuidor

        agencia_id(entero): hace referencia al foraneo de la agencia

        taquilla_id(entero): hace referencia al foraneo de la taquilla

        created_at y updated_at: registros de creacion y actualizacion.

        Nota: esta tabla es un arco, pero para poder saber de quien
        hereda cada comercializadora, se escribira tambien el campo
        del origen superior. solamente ese campo.

        Ejemplo
            bloque_id = None
            banca_id = 1
            distribuidor_id = 1
            agencia_id = None
            taquilla_id = None

            esa data representa un distribuidor, puesto que es el inferior
            y solo se muesta la infor de su padre

    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True
    operadora_id = models.IntegerField(
        null=True,
        blank=True
    )
    bloque_id = models.IntegerField(
        null=True,
        blank=True
    )
    banca_id = models.IntegerField(
        null=True,
        blank=True
    )
    distribuidor_id = models.IntegerField(
        null=True,
        blank=True
    )
    agencia_id = models.IntegerField(
        null=True,
        blank=True
    )
    taquilla_id = models.IntegerField(
        null=True,
        blank=True
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Dimension de arco comercializacion')
        verbose_name_plural = ('Dimension de arco comercializaciones')

    def get_object(self):
        """
        Devuelve el objeto de la comercializadora
        """
        if self.operadora_id and not self.bloque_id:
            # es operadora
            from admin_comercializacion.models import Operadoras
            return Operadoras.objects.get(pk=self.operadora_id)
        elif self.bloque_id and self.operadora_id and not self.banca_id:
            # es bloque
            from admin_comercializacion.models import Bloques
            return Bloques.objects.get(pk=self.bloque_id)
        elif self.banca_id and self.bloque_id and not self.distribuidor_id:
            # es banca
            from admin_comercializacion.models import Bancas
            return Bancas.objects.get(pk=self.banca_id)
        elif self.distribuidor_id and self.banca_id and not self.agencia_id:
            # es distribuidor
            from admin_comercializacion.models import Distribuidores
            return Distribuidores.objects.get(pk=self.distribuidor_id)
        elif self.agencia_id and self.distribuidor_id and not self.taquilla_id:
            # es agencia
            from admin_comercializacion.models import Agencias
            return Agencias.objects.get(pk=self.agencia_id)
        elif self.taquilla_id and self.agencia_id and not self.distribuidor_id:
            from admin_comercializacion.models import Taquillas
            return Taquillas.objects.get(pk=self.taquilla_id)
        else:
            raise ValueError(
                "Error: La dimension no pertenece a ninguna comercializadora")

    def get_kwargs_comercializadora_origen(self, prefix=""):
        """
        Devuelve el kwargs del objeto origen de la comercializadora
        """
        kwargs = {}
        if self.operadora_id and not self.bloque_id:
            # es operadora
            raise ValueError("Error: La dimension no posee origen")
        elif self.bloque_id and self.operadora_id and not self.banca_id:
            # es bloque
            kwargs[prefix + "operadora_id"] = self.operadora_id
        elif self.banca_id and self.bloque_id and not self.distribuidor_id:
            # es banca
            kwargs[prefix + "bloque_id"] = self.bloque_id
        elif self.distribuidor_id and self.banca_id and not self.agencia_id:
            # es distribuidor
            kwargs[prefix + "banca_id"] = self.banca_id
        elif self.agencia_id and self.distribuidor_id and not self.taquilla_id:
            # es agencia
            kwargs[prefix + "distribuidor_id"] = self.distribuidor_id
        elif self.taquilla_id and self.agencia_id and not self.distribuidor_id:
            kwargs[prefix + "taquilla_id"] = self.taquilla_id
        else:
            raise ValueError(
                "Error: La dimension no pertenece a ninguna comercializadora")

        return kwargs

    def get_kwargs_comercializadora(self, prefix=""):
        """
        Devuelve el kwargs del objeto de la comercializadora
        """
        kwargs = {}

        if self.operadora_id and not self.bloque_id:
            # es operadora
            kwargs[prefix + "operadora_id"] = self.operadora_id
        elif self.bloque_id and self.operadora_id and not self.banca_id:
            # es bloque
            kwargs[prefix + "bloque_id"] = self.bloque_id
        elif self.banca_id and self.bloque_id and not self.distribuidor_id:
            # es banca
            kwargs[prefix + "banca_id"] = self.banca_id
        elif self.distribuidor_id and self.banca_id and not self.agencia_id:
            # es distribuidor
            kwargs[prefix + "distribuidor_id"] = self.distribuidor_id
        elif self.agencia_id and self.distribuidor_id and not self.taquilla_id:
            # es agencia
            kwargs[prefix + "agencia_id"] = self.agencia_id
        elif self.taquilla_id and self.agencia_id and not self.distribuidor_id:
            kwargs[prefix + "taquilla_id"] = self.taquilla_id
        else:
            raise ValueError(
                "Error: La dimension no pertenece a ninguna comercializadora")

        return kwargs

    def get_hijos(self):
        """
        Cada objeto tiene representados 2 filas menos la operadora,
        pero la operadora tiene todos los demas campos nulos,
        encambio los demas tienen en campo que los identifica
        mas el del padre y los demas nulos, pero basta con saber que otro
        es nulo para descartarlo
        """
        if self.operadora_id and not self.bloque_id:
            # es operadora
            return DimensionArcoComercializacion.objects.filter(
                operadora_id=self.operadora_id,
                bloque_id__isnull=False
            )
        elif self.bloque_id and self.operadora_id and not self.banca_id:
            # es bloque
            return DimensionArcoComercializacion.objects.filter(
                bloque_id=self.bloque_id,
                banca_id__isnull=False
            )
        elif self.banca_id and self.bloque_id and not self.distribuidor_id:
            # es banca
            return DimensionArcoComercializacion.objects.filter(
                banca_id=self.banca_id,
                distribuidor_id__isnull=False
            )
        elif self.distribuidor_id and self.banca_id and not self.agencia_id:
            # es distribuidor
            return DimensionArcoComercializacion.objects.filter(
                distribuidor_id=self.distribuidor_id,
                agencia_id__isnull=False
            )
        elif self.agencia_id and self.distribuidor_id and not self.taquilla_id:
            # es agencia
            return DimensionArcoComercializacion.objects.filter(
                agencia_id=self.agencia_id,
                taquilla_id__isnull=False
            )
        else:
            DimensionArcoComercializacion.objects.none()


class Hecho1_VentasCadenasJuegos(ProtectDelete, models.Model):
    """Hecho1_VentasCadenasJuegos: Hecho 1: Ventas de la cadena por juego

    Campos definidos:

        Dimenciones:

            tiempo(foreign): hace referencia a la dimencion de tiempo

            comercializacion(foreign): hace referencia a la dimencion de comercializacion

            juegos(foreign): hace referencia a la dimencion de juegos

        Indicadores:
            monto_total(decimal): monto total vendido

            monto_premios(decimal): monto en premios

            count_apuestas(entero): cantidad de apuestas realizadas

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    # Dimenciones
    tiempo = models.ForeignKey(
        'admin_datamart.DimensionTiempo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    juegos = models.ForeignKey(
        'admin_datamart.DimensionJuegos',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    # Indicadores
    monto_total = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    monto_premios = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    count_apuestas = models.IntegerField(
        null=True,
        default=0
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 1: Ventas por cadena y juego')
        verbose_name_plural = ('Hecho 1: ventas por toda la cadena y juegos')

    # funtions
    def add_apuesta(self, monto):
        """
        Suma un monto al registro
        y a su vez una apuesta, ya que
        esta data se guarda por cada item
        de un ticket
        """
        self.monto_total += Decimal(monto)
        self.count_apuestas += 1
        self.save(update_fields=["monto_total", "count_apuestas"])

    def rest_apuesta(self, monto):
        """
        Resta un monto al registro
        y a su vez una apuesta, ya que
        esta data se guarda por cada item
        de un ticket
        """
        self.monto_total -= Decimal(monto)
        self.count_apuestas -= 1
        self.save(update_fields=["monto_total", "count_apuestas"])

    def add_monto_premios(self, monto):
        """
        Suma el un monto de premio
        """
        self.monto_premios += Decimal(monto)
        self.save(update_fields=["monto_premios", ])

    def rest_monto_premios(self, monto):
        """
        Resta el un monto de premio
        """
        self.monto_premios -= Decimal(monto)
        self.save(update_fields=["monto_premios", ])


class Hecho2_VentasCadenasAbstract(models.Model):
    """Hecho2_VentasCadenasAbstract: Hecho 2: Ventas de la cadena

    Campos definidos:

        Dimenciones:

            tiempo(foreign): hace referencia a la dimencion de tiempo

            comercializacion(foreign): hace referencia a la dimencion de comercializacion

        Indicadores:
            monto_total(decimal): monto total vendido

            monto_premios(decimal): monto en premios

            count_apuestas(entero): cantidad de apuestas realizadas

            count_tickets(entero): cantidad de tickect vendidos

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    # Dimenciones
    tiempo = models.ForeignKey(
        'admin_datamart.DimensionTiempo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    # Indicadores
    monto_total = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    monto_premios = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    count_apuestas = models.IntegerField(
        null=True,
        default=0
    )
    count_tickets = models.IntegerField(
        null=True,
        default=0
    )

    class Meta:
        abstract = True

    # funtions
    def add_ticket(self, ticket):
        """
        Suma un ticket, agregando a su vez
        el numero de apuestad del ticket
        y el monto del ticket
        """
        self.monto_total += ticket.monto
        self.count_tickets += 1
        self.count_apuestas += ticket.ticketsdetail_set.all().count()
        self.save(
            update_fields=[
                "monto_total",
                "count_tickets",
                "count_apuestas"])

    def rest_ticket(self, ticket):
        """
        Resta un ticket, agregando a su vez
        el numero de apuestad del ticket
        y el monto del ticket
        """
        self.monto_total -= ticket.monto
        self.count_tickets -= 1
        self.count_apuestas -= ticket.ticketsdetail_set.all().count()
        self.save(
            update_fields=[
                "monto_total",
                "count_tickets",
                "count_apuestas"])

    def add_monto_premios(self, monto):
        """
        Suma un monto de un ticket premiado
        """
        self.monto_premios += Decimal(monto)
        self.save(update_fields=["monto_premios", ])

    def rest_monto_premios(self, monto):
        """
        Resta un monto de un ticket premiado
        """
        self.monto_premios -= Decimal(monto)
        self.save(update_fields=["monto_premios", ])


class Hecho2_VentasCadenas(ProtectDelete, Hecho2_VentasCadenasAbstract):

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 2: Ventas por cadena')
        verbose_name_plural = ('Hecho 2: ventas por toda la cadena')


class Hecho2_VentasCadenasLinea(ProtectDelete, Hecho2_VentasCadenasAbstract):

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 2 en linea: Ventas por cadena')
        verbose_name_plural = ('Hecho 2 en linea: ventas por toda la cadena')


class Hecho5_ComisionesCadena(ProtectDelete, models.Model):
    """Hecho5_ComisionesCadena: Hecho 5: Comisiones de la cadena

    Campos definidos:

        Dimenciones:

            tiempo(foreign): hace referencia a la dimencion de tiempo

            comercializacion(foreign): hace referencia a la dimencion de comercializacion

        Indicadores:
            venta(decimal): monto total vendido

            premio(decimal): monto en premios

            comision(decimal): monto de la comision total

            comision_down(decimal): monto de la comision de los hijos

            participacion(decimal): monto de la participacion total

            participacion_down(decimal): monto de la participacion de los hijos

            regalia(decimal): monto de la regalia total

            regalia_down(decimal): monto de la regalia de los hijos

            queda(decimal): monto de la queda total, se calcula cada corte, se le
                suma a la comercializadora y se le resta a la operadora,
                en caso de la comercializadora tenga menos participacion que su
                operadora.

            queda_down(decimal): monto de la queda de los hijos, Esta queda en el unico campo
                de los down que se debe usar de manera distinta, es decir, la queda_down solo
                se calcula los dias de corte, y con la queda de cada uno de los
                hijos para el acarreo, se usa igual que la queda del comercializador.

            queda_ref(decimal): monto de la queda referencial, se calcula diaria

            participacion(decimal): monto de la participacion total

            participacion_down(decimal): monto de la participacion de los hijos

            alquiler(decimal): monto del alquiler

            saldo_bruto(decimal): monto total del saldo en bruto

            saldo_comer(decimal): monto total del saldo para la comercializadora padre

            saldo_oper(decimal): monto total de mi saldo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    # Dimensiones
    tiempo = models.ForeignKey(
        'admin_datamart.DimensionTiempo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    # indicadores
    venta = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    premio = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    comision = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    comision_down = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    participacion = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    participacion_down = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    regalia = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    regalia_down = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda_down = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda_ref = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    alquiler = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    saldo_bruto = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    saldo_comer = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    saldo_oper = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 5: Comisiones por cadena')
        verbose_name_plural = ('Hecho 5: Comisiones por toda la cadena')


class Hecho6_ComisionesCadenaJuego(ProtectDelete, models.Model):
    """Hecho6_ComisionesCadenaJuego: Hecho 6: Comisiones de la cadena

    Campos definidos:

        Dimenciones:

            tiempo(foreign): hace referencia a la dimencion de tiempo

            comercializacion(foreign): hace referencia a la dimencion de comercializacion

            juegos(foreign): hace referencia a la dimencion de juegos

        Indicadores:
            venta(decimal): monto total vendido

            premio(decimal): monto en premios

            comision(decimal): monto de la comision total

            comision_down(decimal): monto de la comision de los hijos

            participacion(decimal): monto de la participacion total

            participacion_down(decimal): monto de la participacion de los hijos

            regalia(decimal): monto de la regalia total

            regalia_down(decimal): monto de la regalia de los hijos

            participacion(decimal): monto de la participacion total

            participacion_down(decimal): monto de la participacion de los hijos

            queda_ref(decimal): monto de la queda referencial, se calcula diaria

            saldo_bruto(decimal): monto total del saldo en bruto

            saldo_comer(decimal): monto total del saldo para la comercializadora padre

            saldo_oper(decimal): monto total de mi saldo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    # Dimensiones
    tiempo = models.ForeignKey(
        'admin_datamart.DimensionTiempo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    juegos = models.ForeignKey(
        'admin_datamart.DimensionJuegos',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    # indicadores
    venta = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    premio = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    comision = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    comision_down = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    regalia = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    regalia_down = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    participacion = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    participacion_down = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda_ref = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    saldo_bruto = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    saldo_comer = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    saldo_oper = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 6: Comisiones por cadena y juegos')
        verbose_name_plural = (
            'Hecho 6: Comisiones por toda la cadena y juegos')


class Hecho7_ComisionesQuedaCadena(ProtectDelete, models.Model):
    """Hecho7_ComisionesQuedaCadena: Hecho 7: Comisiones de la quedan en la cadena

    Campos definidos:

        Dimenciones:

            tiempo(foreign): hace referencia a la dimencion de tiempo

            comercializacion(foreign): hace referencia a la dimencion de comercializacion

        Indicadores:
            queda_taquilla(decimal): Campo no auditado pero se reserva.

            queda_agencia(decimal): Monto total de la queda para la agencia, en un corte.

            queda_distribuidor(decimal): Monto total de la queda para el distribuidor,
                en un corte.

            queda_banca(decimal): Monto total de la queda para la banca, en un corte.

            queda_bloque(decimal): Monto total de la queda para el bloque, en un corte.

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    # Dimensiones
    tiempo = models.ForeignKey(
        'admin_datamart.DimensionTiempo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    # indicadores
    queda_taquilla = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda_agencia = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda_distribuidor = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda_banca = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )
    queda_bloque = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 7: Comisiones de la queda')
        verbose_name_plural = (
            'Hecho 7: Comisiones de la queda por toda la cadena')


class Hecho8_VentasMonitorLinea(ProtectDelete, models.Model):
    """Hecho8_VentasMonitor: Hecho 8: Monitor de ventas

    Campos definidos:

        Dimensiones:

            tiempo(foreign): hace referencia a la dimension de tiempo

            comercializacion(foreign): hace referencia a la dimension de comercializacion

            juegos(foreign): hace referencia a la dimension de juegos optimizada

        Indicadores:
            monto_venta(decimal): monto venta referencial por ticket


        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    # Dimensiones
    tiempo = models.ForeignKey(
        'admin_datamart.DimensionTiempo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    juegos = models.ForeignKey(
        'admin_datamart.DimensionJuegos',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    # Indicadores
    monto_venta = models.DecimalField(
        null=True,
        max_digits=30,
        decimal_places=16,
        default=0
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 8: Monitor de ventas')
        verbose_name_plural = ('Hecho 8: Monitor de ventas')

    # functions
    def add_apuesta(self, monto):
        """
        Suma un monto al registro
        y a su vez una apuesta, ya que
        esta data se guarda por cada item
        de un ticket
        """
        self.monto_venta += Decimal(monto)
        self.save(update_fields=["monto_venta", ])

    def rest_apuesta(self, monto):
        """
        Resta un monto al registro
        y a su vez una apuesta, ya que
        esta data se guarda por cada item
        de un ticket
        """
        self.monto_venta -= Decimal(monto)
        self.save(update_fields=["monto_venta", ])


class Hecho9_VentasSaldosCadena(ProtectDelete, models.Model):
    """Hecho9_VentasSaldosCadena: Hecho 9: Saldos de la cadena

    Campos definidos:

        Dimensiones:

            tiempo(foreign): hace referencia a la dimension de tiempo

            comercializacion(foreign): hace referencia a la dimension de comercializacion

        Indicadores:
            saldo_inicial(decimal): saldo inicial de la comercializadora

            saldo_actual(decimal): saldo actual de la comercializadora

            depositos(decimal): depositos de la comercializadora

            pagos(decimal): pagos de la comercializadora

            ajustes(decimal): ajustes de la comercializadora

            cargos(decimal): cargos de la comercializadora (queda por ahora)

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    # Dimensiones
    tiempo = models.ForeignKey(
        'admin_datamart.DimensionTiempo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    # Indicadores
    queda_corte = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=8,
        default=0
    )

    saldo_actual = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=8,
        default=0
    )

    saldo_anterior = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=8,
        default=0
    )

    depositos = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=8,
        default=0
    )

    pagos = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=8,
        default=0
    )

    ajustes = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=8,
        default=0
    )

    cargos = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=8,
        default=0
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Hecho 9 Saldos Cadena')
        verbose_name_plural = ('Hecho 9: Saldos Cadena')


class Consolidado(models.Model):
    """
    Consolidado — Resumen Administrativo del Datamart
    ==================================================
    Replica el resumen administrativo para su integración con el
    integrador externo de datamart. Almacena un snapshot por sorteo/taquilla.

    Nota: "Comercializador" = Bloque (Multi Banca) en la jerarquía del sistema.

    Esquema de referencia (definición oficial del integrador):
        https://docs.google.com/spreadsheets/d/1SjgavwIxTOg__D8WsUEhhyzKI0J68lFTUGw2v6RciCY/

    Jerarquía:
        Operador → Comercializador/Bloque → Banca → Distribuidor → Agencia → Taquilla
    """

    # ── Identificadores de navegación ─────────────────────────────────────────
    id_sorteo = models.IntegerField(
        db_index=True,
        verbose_name='ID Sorteo',
        help_text='Identificación de sorteo',
    )
    id_lista = models.IntegerField(
        db_index=True,
        verbose_name='ID Lista',
        help_text='Identificación de la lista',
    )
    id_tipo_lista = models.IntegerField(
        verbose_name='ID Tipo Lista',
        help_text='Identificación del tipo de lista',
    )

    # ── Jerarquía comercial ───────────────────────────────────────────────────
    id_prestador_servicio = models.IntegerField(
        db_index=True,
        verbose_name='ID Prestador de Servicio',
        help_text='Identificación del Prestador de Servicio',
    )
    id_comercializador = models.IntegerField(
        db_index=True,
        verbose_name='ID Comercializador (Bloque)',
        help_text='Identificación del comercializador / bloque (Multi Banca)',
    )
    id_banca = models.IntegerField(
        db_index=True,
        verbose_name='ID Banca',
        help_text='Identificación de la Banca',
    )
    id_distribuidor = models.IntegerField(
        db_index=True,
        verbose_name='ID Distribuidor',
        help_text='Identificación del Distribuidor',
    )
    id_agencia = models.IntegerField(
        db_index=True,
        verbose_name='ID Agencia (Centro de Apuesta)',
        help_text='Identificación de la Agencia',
    )
    id_taquilla = models.IntegerField(
        db_index=True,
        verbose_name='ID Taquilla',
        help_text='Identificación de la Taquilla',
    )
    id_operador = models.IntegerField(
        db_index=True,
        verbose_name='ID Operador',
        help_text='Identificación del Operador',
    )

    # ── Porcentajes — Comercializador / Bloque ────────────────────────────────
    nporcentaje_comision_com = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Comercializador',
        help_text='Valor del Porcentaje de comisión asignado al comercializador / bloque',
    )
    nporcentaje_participacion_com = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Participación Comercializador',
        help_text='Valor del Porcentaje de participación asignado al comercializador / bloque',
    )
    nporcentaje_regalia_com = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Regalía Comercializador',
        help_text='Valor del Porcentaje de regalía asignado al comercializador / bloque',
    )

    # ── Porcentajes — Banca ───────────────────────────────────────────────────
    nporcentaje_comision_ban = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Banca',
        help_text='Valor del Porcentaje de comisión asignado a la banca',
    )
    nporcentaje_participacion_ban = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Participación Banca',
        help_text='Valor del Porcentaje de participación asignado a la banca',
    )
    nporcentaje_regalia_ban = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Regalía Banca',
        help_text='Valor del Porcentaje de regalía asignado a la banca',
    )

    # ── Porcentajes — Distribuidor ─────────────────────────────────────────────
    nporcentaje_comision_dis = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Distribuidor',
        help_text='Valor del Porcentaje de comisión asignado al distribuidor',
    )
    nporcentaje_participacion_dis = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Participación Distribuidor',
        help_text='Valor del Porcentaje de participación asignado al distribuidor',
    )
    nporcentaje_regalia_dis = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Regalía Distribuidor',
        help_text='Valor del Porcentaje de regalía asignado al distribuidor',
    )

    # ── Porcentajes — Agencia ─────────────────────────────────────────────────
    nporcentaje_comision_agc = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='% Comisión Agencia',
        help_text='Valor del Porcentaje de comisión asignado a la agencia',
    )

    # ── Montos de Venta ───────────────────────────────────────────────────────
    mmonto_venta = models.DecimalField(
        max_digits=13, decimal_places=2,
        verbose_name='Monto de Venta',
        help_text='Monto total de venta',
    )
    mmonto_venta_ganador = models.DecimalField(
        max_digits=13, decimal_places=2,
        verbose_name='Monto Venta al Nro Ganador',
        help_text='Monto de Venta al número ganador',
    )
    mmonto_premios = models.DecimalField(
        max_digits=13, decimal_places=2,
        verbose_name='Monto Premios',
        help_text='Monto total de premios',
    )

    # ── Montos de Comisión y Regalía ─────────────────────────────────────────
    mmonto_comision_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Comercializador',
        help_text='Monto a pagar en comisión al Comercializador / bloque',
    )
    mmonto_regalia_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Regalía Comercializador',
        help_text='Monto a pagar en regalía al Comercializador / bloque',
    )
    mmonto_comision_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Banca',
        help_text='Monto a pagar en comisión a la banca',
    )
    mmonto_regalia_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Regalía Banca',
        help_text='Monto a pagar en regalía a la banca',
    )
    mmonto_comision_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Distribuidor',
        help_text='Monto a pagar en comisión al distribuidor',
    )
    mmonto_regalia_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Regalía Distribuidor',
        help_text='Monto a pagar en regalía al distribuidor',
    )
    mmonto_comision_agc = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Monto Comisión Agencia',
        help_text='Monto a pagar en comisión a la agencia',
    )

    # ── Saldos (NOT NULL) ─────────────────────────────────────────────────────
    msaldo_oper = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Operador',
        help_text='Saldo del Operador',
    )
    msaldo_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Comercializador',
        help_text='Saldo del Comercializador / bloque',
    )
    msaldo_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Banca',
        help_text='Saldo de la Banca',
    )
    msaldo_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        verbose_name='Saldo Distribuidor',
        help_text='Saldo del Distribuidor',
    )

    # ── Saldos (nullable — opcionales según integrador) ───────────────────────
    msaldo_agc = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Agencia',
        help_text='Saldo de la Agencia',
    )
    msaldo_bruto_com = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Bruto Comercializador',
        help_text='Saldo Bruto del comercializador / bloque',
    )
    msaldo_bruto_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Bruto Banca',
        help_text='Saldo Bruto de la Banca',
    )
    msaldo_bruto_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Bruto Distribuidor',
        help_text='Saldo Bruto del Distribuidor',
    )
    msaldo_oper_ban = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Operador-Banca',
        help_text='Saldo Operador de la Banca',
    )
    msaldo_oper_dis = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Operador-Distribuidor',
        help_text='Saldo Operador del Distribuidor',
    )
    msaldo_oper_cm = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Operador-Comercializador',
        help_text='Saldo Operador del Comercializador / bloque',
    )
    msaldo_cm = models.DecimalField(
        max_digits=30, decimal_places=16,
        null=True, blank=True,
        verbose_name='Saldo Comercializador/Bloque',
        help_text='Saldo Comercializador / Bloque',
    )

    # ── Datos adicionales ─────────────────────────────────────────────────────
    tserial_ifa = models.CharField(
        max_length=50,
        verbose_name='Serial IFA',
        help_text='Serial de la Impresora Fiscal',
    )
    id_perfil_pago_premios = models.IntegerField(
        null=True, blank=True,
        verbose_name='ID Perfil Pago Premios',
        help_text='Identificación del perfil de pago de premios',
    )
    dfecha = models.DateField(
        db_index=True,
        verbose_name='Fecha',
        help_text='Fecha del consolidado',
    )

    class Meta:
        db_tablespace   = 'ts_finance'
        verbose_name    = 'Consolidado Datamart'
        verbose_name_plural = 'Consolidados Datamart'
        ordering        = ['-dfecha', 'id_sorteo', 'id_taquilla']
        indexes = [
            models.Index(fields=['dfecha', 'id_sorteo'], name='idx_consol_fecha_sorteo'),
            models.Index(fields=['id_taquilla', 'dfecha'], name='idx_consol_taquilla_fecha'),
            models.Index(fields=['id_agencia', 'dfecha'], name='idx_consol_agencia_fecha'),
        ]

    def __str__(self):
        return 'Consolidado sorteo={0} taquilla={1} fecha={2}'.format(
            self.id_sorteo, self.id_taquilla, self.dfecha,
        )
