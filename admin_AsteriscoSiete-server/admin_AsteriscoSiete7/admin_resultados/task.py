# -*- coding: utf-8 -*-

from admin_lib.util_task import AsyncGestionOperationalError
from admin_resultados.algorithm_automatic import (
    Algorithm_Combinadas, Algorithm_JuegoCompleto, Algorithm_MedioJuego, Algorithm_SegundaMita,
)
from admin_resultados.models import Resultados
try:
    from celery.registry import tasks
except ImportError:
    class _NoOpTaskRegistry:
        def register(self, *args, **kwargs):
            pass
    tasks = _NoOpTaskRegistry()


class Algorithms(AsyncGestionOperationalError):
    """
    Tarea asincrona que ejecuta el algoritmo automatico para
    el procesamiento de resultados en los encuentros
    """
    name = 'Algorithms'
    queue = 'resultados'

    def run_try(self, *args, **kwargs):
        resultado = Resultados.objects.get(
            encuentro_id=kwargs.get('encuentro'),
            sistema_id=kwargs.get('sistema_resultados')
        )
        resultado.processed_number = resultado.processed_number + 1
        resultado.save(update_fields=['processed_number'])
        jugadas = 0
        for anotacion in resultado.anotaciones_set.all():
            """
            Se recorren todas las anotaciones de resultado en cuestion a un encuentro
            y dependiendo de los grupos habilitados se procesan los resultados
            por cada algoritmo.
            """
            process = None
            if anotacion.grupo.codename == 'medio_juego':
                process = Algorithm_MedioJuego(anotacion, kwargs.get('filter_cadena'))
            elif anotacion.grupo.codename == 'segunda_mita':
                process = Algorithm_SegundaMita(anotacion, kwargs.get('filter_cadena'))
            elif anotacion.grupo.codename == 'juego_completo':
                process = Algorithm_JuegoCompleto(anotacion, kwargs.get('filter_cadena'))
            elif anotacion.grupo.codename == 'combinadas':
                process = Algorithm_Combinadas(anotacion, kwargs.get('filter_cadena'))

            if process is not None:
                jugadas += process.count_jugadas

        return 'resultado {0}, {1} jugadas'.format(resultado.pk, jugadas)


tasks.register(Algorithms)
