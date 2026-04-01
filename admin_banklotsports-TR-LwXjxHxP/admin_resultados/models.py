# -*- coding: utf-8 -*-
from admin_historic import auditoria
from django.db import models


class Resultados(models.Model):
    """Resultados: Resultados por encuentro

    Esta tabla posee la definicion basica para guardar los resultados
    de un encuentro

    Campos definidos:
        encuentro(foreign one): encuentro al que hace referencia el resultado

        status(foreign): status del encuentro referenciado, si es ganado
            o perdido por ejemplo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    encuentro = models.ForeignKey(
        'admin_juego.Encuentros',
        verbose_name='Encuentro'
    )
    sistema = models.ForeignKey(
        'admin_juego.SistemaJuego',
        null=True,
        verbose_name='Sistema',
    )
    status = models.ForeignKey(
        'admin_status.Status',
        null=True,
        blank=True,
        verbose_name='Status',
    )
    processed = models.BooleanField(
        default=False
    )
    processed_number = models.PositiveSmallIntegerField(
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Creado',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('encuentro', 'sistema')
        verbose_name = ('Resultado de un ecuentro')
        verbose_name_plural = ('Resultados por encuentros')

    def __str__(self):
        """
        Retorna el str correspondiente con el encuentro
        """
        return 'Encuentro {0}'.format(self.encuentro)

    @staticmethod
    def get_or_create_or_flush(encuentro, sistema):
        """
        Metodo statico que se encarga de gestionar las creacion
        y busqueda de resultados para x encuentro, de existir 2
        resultados asociados a un mismo encuentro, se procede a eliminar
        el mas nuevo, ya que el mas antiguo debe ser el correcto
        """
        try:
            resultado = Resultados.objects.filter(encuentro=encuentro, sistema=sistema)
            if resultado:
                return resultado[0]
            else:
                resultado = Resultados.objects.create(
                    encuentro=encuentro,
                    sistema=sistema,
                    status=encuentro.status)
                return resultado

        except Exception:
            resultados = Resultados.objects.filter(
                encuentro=encuentro,
                sistema=sistema
            ).order_by('created_at')

            resultado = resultados[0]
            for obj in resultados[1:]:
                obj.delete()
            return resultado, False

    def is_last(self, encuentros, sistema_resultados):
        """
            Metodo que verifica si este resultado es el ultimo cargado
        """
        not_resultado = False
        for encuentro in encuentros:
            if encuentro.get_exists_logros():
                if encuentro.get_exists_resultados(
                    sistema_resultados=sistema_resultados
                ):
                    pass
                else:
                    encuentro.resultado_object = encuentro.get_resultado(
                        sistema_resultados=sistema_resultados
                    )

                    status_result = None
                    if encuentro.resultado_object:
                        if encuentro.resultado_object.status:
                            status_result = encuentro.resultado_object.status

                    if not status_result:
                        status_result = encuentro.status

                    if (status_result.codename == 'status_habilitado' or
                            status_result.codename == 'status_valido_no_terminado'):
                        pass
                    else:
                        return not_resultado
        return not_resultado


class ResultadosRestric(models.Model):
    """ResultadosRestric: Restricciones por resultados

    Esta tabla posee la definicion basica para guardar dado un resultado
        todas las restricciones, teniendo un detalle de grupo y modalidad,

    Todos los resultados que tengan estas condiciones seran anulados

    Campos definidos:
        resultado(foreign): resultado al que hace referencia un encuentro

        grupo(foreign): grupo o categoria a la que pertenece el resultado

        modalidad(foreign): grupo o categoria a la que pertenece el resultado


    """
    resultado = models.ForeignKey(
        'Resultados'
    )
    grupo = models.ForeignKey(
        'admin_juego.GruposApuestas'
    )
    modalidad = models.ForeignKey(
        'admin_juego.Modalidades'
    )

    def __str__(self):
        return 'Grupo: {} | Modalidad: {}'.format(self.grupo, self.modalidad)

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Restriccion de resultado')
        verbose_name_plural = ('Restricciones de resultados')

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.resultado.__module__.split('.')[0],
            self.resultado.__class__.__name__.lower(),
            self.resultado_id
        )


class Anotaciones(models.Model):
    """Anotaciones: anotaciones por resultados de un encuentro y grupo

    Esta tabla posee la definicion basica para guardar las anotaciones por
    grupos de los resultados de un encuentro en particular

    Campos definidos:
        resultado(foreign): resultado al que hace referencia un encuentro

        grupo(foreign): grupo o categoria a la que pertenece el resultado

        created_at y updated_at: registros de creacion y actualizacion.
    """
    resultado = models.ForeignKey(
        'Resultados'
    )
    grupo = models.ForeignKey(
        'admin_juego.GruposApuestas'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Anotacion')
        verbose_name_plural = ('Anotaciones por grupo')

    def __str__(self):
        """
        Retorna el str correspondiente con el encuentro
        """
        return '{0} | {1}'.format(self.resultado, self.grupo)

    @staticmethod
    def get_or_create_or_flush(resultado, grupo):
        """
        Metodo statico que se encarga de gestionar las creacion
        y busqueda de una anotacion para x resultado segun un grupo, de existir 2
        anotaciones asociadas a un mismo resultado y grupo, se procede a eliminar
        el mas nuevo, ya que el mas antiguo debe ser el correcto
        """
        try:
            return Anotaciones.objects.get_or_create(
                resultado=resultado,
                grupo=grupo
            )
        except Exception:
            anotaciones = Anotaciones.objects.filter(
                resultado=resultado,
                grupo=grupo
            ).order_by('created_at')

            anotacion = anotaciones[0]
            for obj in anotaciones[1:]:
                obj.delete()
            return anotacion, False

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.resultado.__module__.split('.')[0],
            self.resultado.__class__.__name__.lower(),
            self.resultado_id
        )


class AnotacionesDetail(models.Model):
    """AnotacionesDetail: detalle de las anotaciones

    Esta tabla posee la definicion basica para guardar el detalle
    de las anotaciones, y asi poder ejecutar los algoritmos
    automaticos para la asignacion de resultados.


    Los registros que no tengan condicion son los que se cargan desde el formulario,
    los demas son calculados. Estos registros son los que se toman en cuenta en los
    algoritmos de resultados

    Campos definidos:
        anotacion(foreign): anotacion a la que se hace referencia

        encuentro_detail(foreign): detalle del encuentro al cual se
            hace referencia

        condicion(foreign): condicion a la que se hace referencia,
            en caso de ser por equipo el resultado, esta condicion es None

        puntaje(entero): puntaje de la anotacion, sirve tambien como indice

        created_at y updated_at: registros de creacion y actualizacion.
    """

    anotacion = models.ForeignKey(
        'Anotaciones'
    )

    encuentro_detail = models.ForeignKey(
        'admin_juego.EncuentrosDetail',
        null=True,
        blank=True
    )
    condicion = models.ForeignKey(
        'admin_juego.Condiciones',
        null=True,
        blank=True
    )

    puntaje = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Puntaje',
    )

    referencia = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Referencia'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Anotacion')
        verbose_name_plural = ('Anotaciones por grupo')

    def __str__(self):
        """
        Retorna el str correspondiente con el encuentro
        """
        return '{0} | {1}'.format(self.anotacion, self.get_label())

    def get_label(self):
        """
        Devuelve el label que identifica al detalle de anotacion
        """
        if self.condicion:
            return '{0} | {1}'.format(self.condicion.modalidad, self.condicion)
        else:
            return '{0}'.format(self.encuentro_detail.equipos_temporadas.equipo)

    def get_label_customize(self):
        """
        Devuelde el puntaje en caso de ser una anotacion por modalidad
        h+c+e, ya que esta se define como el mismo, en cado de no serlo
        se devuelve el nombre de la condicion haciendo un split por el
        puntaje, y si alguna cosa da error se devuelve una cadena vacia
        """
        try:
            if self.condicion.modalidad.codename == 'h+c+e':
                return self.puntaje
            elif self.condicion.modalidad.codename == 'anota_1ro':
                if self.referencia:
                    return self.referencia
                else:
                    return self.condicion.nombre.split('/')[self.puntaje - 1]
            else:
                return self.condicion.nombre.split('/')[self.puntaje - 1]
        except Exception:
            return ''

    @staticmethod
    def get_or_create_or_flush(anotacion, condicion=None, encuentro_detail=None):
        """
        Metodo statico que se encarga de gestionar las creacion
        y busqueda de un detalle de una anotacion para x resultado
        segun un grupo, de existir 2 detalles para la misma anotaciones
        se procede a eliminar el mas nuevo, ya que el mas antiguo debe ser el correcto
        """
        try:
            return AnotacionesDetail.objects.get_or_create(
                anotacion=anotacion,
                condicion=condicion,
                encuentro_detail=encuentro_detail
            )
        except Exception:
            anotaciones_detail = AnotacionesDetail.objects.filter(
                anotacion=anotacion,
                condicion=condicion,
                encuentro_detail=encuentro_detail
            ).order_by('created_at')

            anotacion_detail = anotaciones_detail[0]
            for obj in anotaciones_detail[1:]:
                obj.delete()
            return anotacion_detail, False

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.anotacion.resultado.__module__.split('.')[0],
            self.anotacion.resultado.__class__.__name__.lower(),
            self.anotacion.resultado_id
        )


auditoria.register(
    Resultados,
    ResultadosRestric,
    Anotaciones,
    AnotacionesDetail
)
