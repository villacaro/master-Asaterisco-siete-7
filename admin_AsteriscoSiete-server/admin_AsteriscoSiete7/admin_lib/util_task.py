# -*- coding: utf-8 -*-

try:
    from celery.app.task import Task
except ImportError:
    # Entorno local sin Celery: usamos una clase base simple
    class Task:
        request = type('obj', (object,), {'retries': 0})()
        def retry(self, *a, **kw): raise RuntimeError('Celery not available')

from django.db.utils import OperationalError


class AsyncGestionOperationalError(Task):
    """
    Clase base diseñada para gestionar la reprogramacion de tareas canceladas al fallas la conexion de postgres
    """

    def set_acquire(self):
        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho 2 es por taquilla
        try:
            self.padlock.acquire()
            self.mensaje.append('Acquire succes')
        except Exception:
            self.mensaje.append('Acquire faile')
        # ================================================================================================

    def set_release(self):
        # ================================================================================================
        # Quitamos el candado
        try:
            self.padlock.release()
            self.mensaje.append('Release succes')
        except Exception:
            self.mensaje.append('Release faile')
        # ================================================================================================

    def all_release(self):
        # ================================================================================================
        # Quitamos el candado
        for key in self.padlocks:
            try:
                self.padlocks[key].release()
                self.mensaje.append('Release succes')
            except Exception:
                self.mensaje.append('Release faile')
        # ================================================================================================

    def run(self, *args, **kwargs):
        try:
            return self.run_try(*args, **kwargs)
        except OperationalError as exc:

            if hasattr(self, 'padlock'):
                self.set_release()

            if hasattr(self, 'padlocks'):
                self.all_release()

            if hasattr(self, 'kwargs'):
                kwargs = self.kwargs

            # reinicia la tarea en tiempo exponencial, e intenta 7 veces
            # retrie 1, inicia en 5 segundos
            # retrie 2, inicia en 25 segundos
            # retrie 3, inicia en 125 segundos
            # retrie 4, inicia en 625 segundos
            # retrie 5, inicia en 3128 segundos (casi una hora)
            # retrie 6, inicia en 4 horas
            # retrie 7, inicia en 21 horas
            raise self.retry(exc=exc, countdown=5**self.request.retries, max_retries=7, kwargs=kwargs)

    def run_try(self, *args, **kwargs):
        raise NotImplementedError("Esta funcion debe ser sobreescrita")
