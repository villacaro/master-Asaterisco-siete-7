# -*- coding: utf-8 -*-
"""
algorithm_automatic.py
Algoritmo de procesamiento automatico de resultados de loteria y animalitos.
Sustituye la logica anterior de deportes/torneos por la logica de sorteos.
"""

from admin_finanzas.task import AsyncGestionDeTicketsPorJugada
from admin_juego.models import apuesta


class Algorithm_Generic(object):
    """
    Algoritmo generico para procesar resultados de sorteos.
    Tiene los estados posibles: ganado, perdido, anulado.
    """

    anulado_automatic = False

    def __init__(self, filter_cadena):
        """
        Inicializa el conteo de jugadas procesadas en 0
        """
        self.filter_cadena = filter_cadena
        self.count_jugadas = 0

    def lanzar(self, jugada, accion, anulado):
        """
        Lanza la ejecucion de los resultados de tickets por jugada.
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

        async_task = AsyncGestionDeTicketsPorJugada()
        async_task.delay(*(), **kwargs)
        self.count_jugadas += 1

    def procesar_sorteo(self):
        """
        Se procesa un sorteo de loteria (Triple, Animalitos, etc.)
        Logica central: compara el numero apostado con el resultado del sorteo.
        """
        codename = 'sorteo_directo'
        jugadas = apuesta.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():
            if self.anulado_automatic:
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            for jugada in jugadas:
                accion = False
                # Comparar el numero apostado con el resultado del sorteo
                if jugada.valor_etq_ref is not None:
                    numero_apostado = str(jugada.valor_etq_ref).strip()
                    numero_resultado = str(jugada.encuentros_modalidad.etiqueta_ref or '').strip()
                    if numero_apostado and numero_resultado:
                        accion = numero_apostado == numero_resultado

                self.lanzar(jugada, accion, False)

    def procesar_animalito(self):
        """
        Se procesa una apuesta de animalitos.
        Logica: compara el animal apostado con el resultado del sorteo.
        """
        codename = 'animalito'
        jugadas = apuesta.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():
            if self.anulado_automatic:
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            for jugada in jugadas:
                accion = False
                if jugada.condicion and jugada.condicion.modalidad:
                    indice_apostado = jugada.indice
                    # Obtener el resultado del sorteo de animalitos
                    anotaciones = self.anotacion.anotacionesdetail_set.filter(
                        condicion__isnull=False
                    )
                    for detalle in anotaciones:
                        if detalle.puntaje == indice_apostado:
                            accion = True
                            break

                self.lanzar(jugada, accion, False)

    def procesar_terminacion(self):
        """
        Se procesa una apuesta por terminacion (ultimo digito).
        """
        codename = 'terminacion'
        jugadas = apuesta.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        if jugadas.exists():
            if self.anulado_automatic:
                for jugada in jugadas:
                    self.lanzar(jugada, False, True)
                return

            for jugada in jugadas:
                accion = False
                if jugada.valor_etq_ref is not None:
                    terminacion = str(jugada.valor_etq_ref).strip()
                    resultado = str(jugada.encuentros_modalidad.etiqueta_ref or '').strip()
                    if terminacion and resultado:
                        accion = resultado.endswith(terminacion)

                self.lanzar(jugada, accion, False)


class Algorithm_SorteoNormal(Algorithm_Generic):
    """
    Algoritmo para sorteos normales de loteria (Triple, Lotto, etc.)
    """

    def __init__(self, anotacion, filter_cadena):
        super(Algorithm_SorteoNormal, self).__init__(filter_cadena)
        self.anotacion = anotacion
        self.automatic()

    def automatic(self):
        if self.anotacion.resultado.status.codename == 'status_valido_no_terminado':
            self.anulado_automatic = True
        self.procesar_sorteo()
        self.procesar_terminacion()


class Algorithm_Animalitos(Algorithm_Generic):
    """
    Algoritmo para sorteos de animalitos.
    """

    def __init__(self, anotacion, filter_cadena):
        super(Algorithm_Animalitos, self).__init__(filter_cadena)
        self.anotacion = anotacion
        self.automatic()

    def automatic(self):
        if self.anotacion.resultado.status.codename == 'status_valido_no_terminado':
            self.anulado_automatic = True
        self.procesar_animalito()


class Algorithm_Combinadas(Algorithm_Generic):
    """
    Algoritmo para combinaciones de apuestas (parle de sorteos).
    """

    def __init__(self, anotacion, filter_cadena):
        super(Algorithm_Combinadas, self).__init__(filter_cadena)
        self.anotacion = anotacion
        self.automatic()

    def automatic(self):
        self.procesar_sorteo()
        self.procesar_animalito()
        if self.anotacion.resultado.status.codename == 'status_valido_no_terminado':
            self.anulado_automatic = True
        self.procesar_terminacion()


# Alias para mantener compatibilidad con codigo legado
# Estas clases existen en el sistema antiguo de deportes y se redirigen a
# las nuevas implementaciones de loteria
Algorithm_MedioJuego = Algorithm_SorteoNormal
Algorithm_SegundaMita = Algorithm_SorteoNormal
Algorithm_JuegoCompleto = Algorithm_SorteoNormal
