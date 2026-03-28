# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_banklotsports.settings import CACHES_CONF_TIME
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
    """DimensionJuegosNew: Dimension de juegos optimizada

    Campos definidos:
        sistema_id(entero): hace referencia al foraneo del sistema de juego

        deporte_id(entero): hace referencia al foraneo del deporte

        torneo_id(entero): hace referencia al foraneo del torneo

        temporada_id(entero): hace referencia al foraneo de la temporada

        jornada_id(entero): hace referencia al foraneo de la jornada

        encuentro_id(entero): hace referencia al foraneo del encuentro

        encuentros_modalidad_id(entero): hace referencia al foraneo del encuentros_modalidad

        grupo_id(entero): hace referencia al foraneo del grupo de apuesta

        modalidad_id(entero): hace referencia al foraneo de la modalidad

        condicion_id(entero): hace referencia al foraneo de la condicion

        equipo_id(entero): hace referencia al foraneo del equipo

        pertenece_id(entero): hace referencia al split de la condicion

        grupojuego_id(entero): hace referencia al grupo de juego del encuentro

        jugador_id(entero): hace referencia al foraneo del jugador

        created_at y updated_at: registros de creacion y actualizacion.
    """
    # este campo indica que nunca debe borrarse este registro
    not_delete = True

    sistema_id = models.IntegerField()
    deporte_id = models.IntegerField()
    torneo_id = models.IntegerField()
    temporada_id = models.IntegerField()
    jornada_id = models.IntegerField()
    encuentro_id = models.IntegerField()
    encuentros_modalidad_id = models.IntegerField()
    grupo_id = models.IntegerField()
    modalidad_id = models.IntegerField()
    condicion_id = models.IntegerField()

    equipo_id = models.IntegerField(
        null=True,
        blank=True
    )

    pertenece_id = models.IntegerField(
        null=True,
        blank=True
    )

    grupojuego_id = models.IntegerField(
        null=True,
        blank=True
    )

    jugador_id = models.IntegerField(
        null=True,
        blank=True
    )

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Dimension de juego')
        verbose_name_plural = ('Dimension de juegos')


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
        'admin_datamart.DimensionTiempo',
    )
    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionComercializacion'
    )
    juegos = models.ForeignKey(
        'admin_datamart.DimensionJuegos'
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
        'admin_datamart.DimensionTiempo',
    )
    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionComercializacion'
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
        'admin_datamart.DimensionTiempo',
    )

    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionArcoComercializacion'
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
        'admin_datamart.DimensionTiempo',
    )
    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionArcoComercializacion'
    )
    juegos = models.ForeignKey(
        'admin_datamart.DimensionJuegos'
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
        'admin_datamart.DimensionTiempo',
    )
    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionComercializacion'
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
        'admin_datamart.DimensionTiempo',
    )
    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionComercializacion'
    )
    juegos = models.ForeignKey(
        'admin_datamart.DimensionJuegosNew'
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
        'admin_datamart.DimensionTiempo',
    )
    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionArcoComercializacion'
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
    """Consolidado: Replica del resumen administrativo para integrar con el consolidado

    Campos definidos:
        Por motivos de rapidez, consultar:
            https://docs.google.com/spreadsheets/d/1SjgavwIxTOg__D8WsUEhhyzKI0J68lFTUGw2v6RciCY/edit#gid=0

    Nota: Comercializador es el bloque

    """

    id_sorteo = models.IntegerField()
    id_lista = models.IntegerField()
    id_tipo_lista = models.IntegerField()
    id_prestador_servicio = models.IntegerField()
    id_comercializador = models.IntegerField()
    id_banca = models.IntegerField()
    id_distribuidor = models.IntegerField()
    id_agencia = models.IntegerField()
    id_taquilla = models.IntegerField()
    id_operador = models.IntegerField()

    nporcentaje_comision_com = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_participacion_com = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_regalia_com = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_comision_ban = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_participacion_ban = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_regalia_ban = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_comision_dis = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_participacion_dis = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_regalia_dis = models.DecimalField(max_digits=5, decimal_places=2)
    nporcentaje_comision_agc = models.DecimalField(max_digits=5, decimal_places=2)

    mmonto_venta = models.DecimalField(max_digits=13, decimal_places=2)
    mmonto_venta_externa = models.DecimalField(max_digits=13, decimal_places=2)
    mmonto_venta_ganador = models.DecimalField(max_digits=13, decimal_places=2)
    mmonto_premios = models.DecimalField(max_digits=13, decimal_places=2)

    mmonto_comision_com = models.DecimalField(max_digits=30, decimal_places=16)
    mmonto_regalia_com = models.DecimalField(max_digits=30, decimal_places=16)
    mmonto_comision_ban = models.DecimalField(max_digits=30, decimal_places=16)
    mmonto_regalia_ban = models.DecimalField(max_digits=30, decimal_places=16)
    mmonto_comision_dis = models.DecimalField(max_digits=30, decimal_places=16)
    mmonto_regalia_dis = models.DecimalField(max_digits=30, decimal_places=16)
    mmonto_comision_agc = models.DecimalField(max_digits=30, decimal_places=16)

    msaldo_oper = models.DecimalField(max_digits=30, decimal_places=16)
    msaldo_com = models.DecimalField(max_digits=30, decimal_places=16)
    msaldo_ban = models.DecimalField(max_digits=30, decimal_places=16)
    msaldo_dis = models.DecimalField(max_digits=30, decimal_places=16)

    msaldo_agc = models.DecimalField(max_digits=30, decimal_places=16, null=True)
    msaldo_bruto_com = models.DecimalField(max_digits=30, decimal_places=16, null=True)
    msaldo_bruto_ban = models.DecimalField(max_digits=30, decimal_places=16, null=True)
    msaldo_bruto_dis = models.DecimalField(max_digits=30, decimal_places=16, null=True)
    msaldo_oper_ban = models.DecimalField(max_digits=30, decimal_places=16, null=True)
    msaldo_oper_dis = models.DecimalField(max_digits=30, decimal_places=16, null=True)
    msaldo_oper_cm = models.DecimalField(max_digits=30, decimal_places=16, null=True)
    msaldo_cm = models.DecimalField(max_digits=30, decimal_places=16, null=True)

    tserial_ifa = models.CharField(max_length=50)

    id_perfil_pago_premios = models.IntegerField()

    dfecha = models.DateField()

    class Meta:
        db_tablespace = "ts_finance"
        verbose_name = ('Consolidado')
        verbose_name_plural = ('Consolidado')
