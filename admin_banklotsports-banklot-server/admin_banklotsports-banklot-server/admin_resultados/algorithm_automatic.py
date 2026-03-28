# -*- coding: utf-8 -*-

from admin_finanzas.task import AsyncGestionDeTicketsPorJugada
from admin_juego.models import Jugadas


class Algorithm_Generic(object):
    """
    Alggoritmo generico para procesar resultados,
    tiene los 3 posibles estados a asignar como atributos
    mienbro de la clase
    """

    anulado_automatic = False

    def __init__(self, filter_cadena):
        """
        Inicializa el conteo de jugadas procesadas en 0
        """
        self.filter_cadena = filter_cadena
        self.count_jugadas = 0

    def set_restric(self, codename):
        return self.anotacion.resultado.resultadosrestric_set.filter(
            grupo_id=self.anotacion.grupo_id,
            modalidad__codename=codename
        ).exists()

    def lanzar(self, jugada, accion, anulado):
        """
        En este metodo se lanza la ejecucion de los resultados
        de tickets por jugada.
        """
        kwargs = {
            'jugada': jugada.pk,
            'filter_cadena': self.filter_cadena
        }

        if anulado:
            kwargs['status'] = 'status_anulado'

            if self.anulado_automatic:
                kwargs['force_anulado'] = True

        else:
            if accion:
                kwargs['status'] = 'status_ganado'
            else:
                kwargs['status'] = 'status_perdido'

        async = AsyncGestionDeTicketsPorJugada()
        async.delay(*(), **kwargs)
        self.count_jugadas += 1

    def empate(self):
        """
        Se procesa la modalidad de empate en caso de existir
        """
        codename = 'empate'

        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )
        for jugada in jugadas:
            if self.anulado_automatic or self.set_restric(codename):
                self.lanzar(jugada, False, True)
                continue

            anotacionesdetail = self.anotacion.anotacionesdetail_set.all().exclude(
                condicion__isnull=False
            )
            puntaje = anotacionesdetail[0].puntaje
            # tomamos como referencia el primero
            accion = True
            for detail in anotacionesdetail:
                if puntaje != detail.puntaje:
                    # verifica si algun puntaje es distinto
                    accion = False

            self.lanzar(jugada, accion, False)

    def ganador(self):
        """
        Se procesa la modalidad ganador
        """
        codename = 'ganador'
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():
            deporte = self.anotacion.resultado.encuentro.jornada.temporadas.torneo.deporte

            # se ordena dependiendo del modo de ganar, si es por puntaje debe ser -
            # pero si es por posicion debe ser +
            anotacionesdetail = self.anotacion.anotacionesdetail_set.all().exclude(
                condicion__isnull=False
            ).order_by('{0}{1}'.format(deporte.resultado, 'puntaje'))
            # importante este orden
            # como minimo en todo encuentro hay 2 equipos
            # entonces la siguiente validacion asegura q solo halla un unico puntaje mayor

            if self.anulado_automatic or self.set_restric(codename):

                for detail in anotacionesdetail:
                    jugadas_querryset = jugadas.filter(
                        detalle_encuentro_id=detail.encuentro_detail_id
                    )
                    for jugada in jugadas_querryset:
                        self.lanzar(jugada, False, True)
                return

            anulado = False
            perdio = False
            encuentro_detail_ganador = anotacionesdetail[0].encuentro_detail_id

            if anotacionesdetail[0].puntaje == anotacionesdetail[1].puntaje:
                perdio = True
                if(deporte.ganador_empate_not_null is False):
                    anulado = True

            for detail in anotacionesdetail:
                jugadas_querryset = jugadas.filter(
                    detalle_encuentro_id=detail.encuentro_detail_id
                )
                for jugada in jugadas_querryset:
                    accion = False
                    if perdio is False and jugada.detalle_encuentro_id == encuentro_detail_ganador:
                        accion = True
                    self.lanzar(jugada, accion, anulado)

    def runline(self):
        """
        se procesa la modalidad de runline
        """
        codename = 'runline'
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():

            if self.anulado_automatic or self.set_restric(codename):
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            anotacionesdetail = self.anotacion.anotacionesdetail_set.all().exclude(
                condicion__isnull=False
            )

            for jugada in jugadas:
                if jugada.valor_etq_ref:
                    ref = jugada.valor_etq_ref.replace(' ', '')
                    if not ref:
                        continue
                    jugada.puntaje_hembra = 0
                    jugada.puntaje_macho = 0

                    ref = float(ref.replace(',', '.'))
                    if ref > 0:
                        jugada.puntaje_hembra = anotacionesdetail.filter(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                        jugada.puntaje_macho = anotacionesdetail.exclude(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                    else:
                        jugada.puntaje_macho = anotacionesdetail.filter(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                        jugada.puntaje_hembra = anotacionesdetail.exclude(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                    anulado = False
                    accion = False
                    resultante = 0
                    if ref < 0:
                        resultante = jugada.puntaje_macho + ref
                        anulado = resultante == jugada.puntaje_hembra
                    else:
                        resultante = jugada.puntaje_hembra + ref
                        anulado = resultante == jugada.puntaje_macho

                    if anulado is False:
                        if ref < 0:
                            if resultante > jugada.puntaje_hembra:
                                accion = True
                        else:
                            if resultante > jugada.puntaje_macho:
                                accion = True

                    self.lanzar(jugada, accion, anulado)

    def altabaja(self):
        """
        Se procesa la modalidad alta baja
        """
        codename = 'alta/baja'
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():

            if self.anulado_automatic or self.set_restric(codename):
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            anotacionesdetail = self.anotacion.anotacionesdetail_set.all().exclude(
                condicion__isnull=False
            )
            puntaje_total = 0

            for detail in anotacionesdetail:
                puntaje_total += detail.puntaje
                # obtenemos puntaje total

            for jugada in jugadas.order_by('indice'):
                encuentros_modalidad = jugada.encuentros_modalidad
                if encuentros_modalidad.etiqueta_ref is None:
                    continue
                ref = encuentros_modalidad.etiqueta_ref.replace(' ', '')
                if not ref:
                    # Se puede presentar el caso de haber espacion en blanco,
                    # se eliminan y si no hay ningun numero se quitan
                    continue
                ref = float(ref.replace(',', '.'))
                accion = False
                anulado = False
                # las jugadas tienen un atributo indice, el cual es ascendente
                # como la condicion es Alta/Baja (tener en cuenta es sobre
                # la condicion, xq hay una modalidad
                # que es Home/visitante, pero la condicion va, Visitante/home,
                # por lo tanto el indice 1 corresponde a visitante)

                # por consecucia entonces el indice 1 equivale a la alta
                # y el 2 equivale a la baja
                if jugada.indice == 1:
                    # Alta, seria lo mismo q hacer condicion.nombre.split('/')[0]=='Alta'
                    if puntaje_total > ref:
                        accion = True
                    elif puntaje_total < ref:
                        accion = False
                    elif puntaje_total == ref:
                        anulado = True
                elif jugada.indice == 2:
                    # Baja, seria lo mismo q hacer condicion.nombre.split('/')[1]=='Baja'
                    if puntaje_total > ref:
                        accion = False
                    elif puntaje_total < ref:
                        accion = True
                    elif puntaje_total == ref:
                        anulado = True
                self.lanzar(jugada, accion, anulado)

    def superrunline(self):
        # segun veo es el mismo codigo de runline,
        # no le encuentro la diferencia, solo que pertenece al grupo de combinadas
        resultado = self.anotacion.resultado
        codename = 'super_runline'
        # sus calculos los debe sacar de juego_completo
        # por eso para esta modaliad sobreescribo el campo anotacion
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():

            if self.anulado_automatic or self.set_restric(codename):
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            anotacion_copia = resultado.anotaciones_set.get(
                grupo__codename='juego_completo'
            )
            # hago una copia de los resultados de juego completo xq se saca de alli
            anotacionesdetail = anotacion_copia.anotacionesdetail_set.all().exclude(
                condicion__isnull=False
            )

            for jugada in jugadas:
                if jugada.valor_etq_ref:
                    ref = jugada.valor_etq_ref.replace(' ', '')
                    if not ref:
                        continue
                    jugada.puntaje_hembra = 0
                    jugada.puntaje_macho = 0

                    ref = float(ref.replace(',', '.'))
                    if ref > 0:
                        jugada.puntaje_hembra = anotacionesdetail.filter(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                        jugada.puntaje_macho = anotacionesdetail.exclude(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                    else:
                        jugada.puntaje_macho = anotacionesdetail.filter(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                        jugada.puntaje_hembra = anotacionesdetail.exclude(
                            encuentro_detail_id=jugada.detalle_encuentro_id,
                        )[0].puntaje

                    anulado = False
                    accion = False
                    resultante = 0
                    if ref < 0:
                        resultante = jugada.puntaje_macho + ref
                        anulado = resultante == jugada.puntaje_hembra
                    else:
                        resultante = jugada.puntaje_hembra + ref
                        anulado = resultante == jugada.puntaje_macho

                    if anulado is False:
                        if ref < 0:
                            if resultante > jugada.puntaje_hembra:
                                accion = True
                        else:
                            if resultante > jugada.puntaje_macho:
                                accion = True

                    self.lanzar(jugada, accion, anulado)

    def hce(self):
        """
        Se procesa la modalidad hce
        """
        codename = 'h+c+e'
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():

            if self.anulado_automatic or self.set_restric(codename):
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            puntaje = self.anotacion.anotacionesdetail_set.get(
                condicion__modalidad__codename=codename
            ).puntaje

            for jugada in jugadas:
                encuentros_modalidad = jugada.encuentros_modalidad
                if encuentros_modalidad.etiqueta_ref is None:
                    continue
                ref = encuentros_modalidad.etiqueta_ref.replace(' ', '')
                if not ref:
                    # Se puede presentar el caso de haber espacion en blanco,
                    # se eliminan y si no hay ningun numero se quitan
                    continue
                ref = float(ref.replace(',', '.'))

                accion = False
                anulado = False
                if puntaje > ref:
                    if jugada.indice == 1:
                        # alta
                        accion = True
                elif puntaje < ref:
                    if jugada.indice == 2:
                        # Baja
                        accion = True
                else:
                    anulado = True
                self.lanzar(jugada, accion, anulado)

    def si_no(self):
        """
        Se procesa la modalidad si/no
        """
        codename = 'si/no'
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():
            if self.anulado_automatic or self.set_restric(codename):
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            anotacionesdetail = self.anotacion.anotacionesdetail_set.get(
                condicion__modalidad__codename=codename
            )

            for jugada in jugadas:
                accion = False
                if jugada.indice == anotacionesdetail.puntaje:
                    # si corresponde el indice es la correcta
                    accion = True
                self.lanzar(jugada, accion, False)

    def anota_1ro(self):
        """
        Se procesa la modalidad anota primero
        """
        codename = 'anota_1ro'
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():

            if self.anulado_automatic or self.set_restric(codename):
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            anotacionesdetail = self.anotacion.anotacionesdetail_set.get(
                condicion__modalidad__codename=codename
            )

            for jugada in jugadas:
                accion = False
                if jugada.indice == anotacionesdetail.puntaje:
                    # si corresponde el indice es la correcta
                    accion = True
                self.lanzar(jugada, accion, False)


class Algorithm_MedioJuego(Algorithm_Generic):
    """
    Agoritmo para modalidades de medio juego
    """

    def __init__(self, anotacion, filter_cadena):
        super(Algorithm_MedioJuego, self).__init__(filter_cadena)
        self.anotacion = anotacion
        self.automatic()

    def automatic(self):
        if self.anotacion.resultado.status.codename == 'status_valido_no_terminado':
            self.anulado_automatic = True
        self.empate()
        self.ganador()
        self.runline()
        self.altabaja()


class Algorithm_SegundaMita(Algorithm_Generic):
    """
    Agoritmo para modalidades de la segunda mita
    """

    def __init__(self, anotacion, filter_cadena):
        super(Algorithm_SegundaMita, self).__init__(filter_cadena)
        self.anotacion = anotacion
        self.automatic()

    def automatic(self):
        if self.anotacion.resultado.status.codename == 'status_valido_no_terminado':
            self.anulado_automatic = True
        self.empate()
        self.ganador()
        self.runline()
        self.altabaja()


class Algorithm_JuegoCompleto(Algorithm_Generic):
    """
    Agoritmo para modalidades de juego completo
    """

    def __init__(self, anotacion, filter_cadena):
        super(Algorithm_JuegoCompleto, self).__init__(filter_cadena)
        self.anotacion = anotacion
        self.automatic()

    def automatic(self):
        self.ganador()
        if self.anotacion.resultado.status.codename == 'status_valido_no_terminado':
            self.anulado_automatic = True
        self.empate()
        self.runline()
        self.altabaja()


class Algorithm_Combinadas(Algorithm_Generic):
    """
    Agoritmo para modalidades combinadas,
    enrealidad enta clase en la unica que se diferencia de las otras modalidades,
    ya que ejecuta metodos distintos.
    """

    def __init__(self, anotacion, filter_cadena):
        super(Algorithm_Combinadas, self).__init__(filter_cadena)
        self.anotacion = anotacion
        self.automatic()

    def automatic(self):
        self.si_no()
        self.anota_1ro()
        if self.anotacion.resultado.status.codename == 'status_valido_no_terminado':
            self.anulado_automatic = True
        self.superrunline()
        self.hce()
