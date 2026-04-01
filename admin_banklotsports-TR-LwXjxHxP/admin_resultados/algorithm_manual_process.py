# -*- coding: utf-8 -*-

from admin_juego.models import Jugadas, SistemaJuego
from admin_resultados.models import Resultados


class AlgorithmsManual(object):
    """
    Clase base con la cual se reprocesa un resultado,
    esto es solo en caso de que las condiciones de apuesta
    de referencia etc, hallan cambiado,
    ya que los resultados se proceson con los datos del momento
    y no con los que finalizo el encuentro
    """

    def __init__(self, ticket_detail):
        """
        Inicializa el resultado en cuestion
        """
        super(AlgorithmsManual, self).__init__()
        self.ticket_detail = ticket_detail

        sistema_juego = SistemaJuego.objects.get_sistema_resultados_by_comercializadora(
            self.ticket_detail.ticket.user.taquilla.agencia.distribuidores.banca.get_comercializadora()
        )

        if sistema_juego:
            self.resultado = Resultados.objects.get(
                encuentro_id=self.ticket_detail.jugada.encuentros_modalidad.encuentro_id,
                sistema_id=sistema_juego.pk,
            )
        else:
            self.resultado = Resultados.objects.get(
                encuentro_id=self.ticket_detail.jugada.encuentros_modalidad.encuentro_id,
            )

    def manual(self):
        """
        Ejecuta el procesamiento, se invoca al procesar un ticket, en caso
        de haber datos cambiados, aqui se inicializa el proceso generico
        dependiendo de el grupo
        """
        anotacion = self.resultado.anotaciones_set.get(
            grupo=self.ticket_detail.jugada.encuentros_modalidad.modalidad_grupo.grupo
        )

        resultado = Algorithm_Generic_Manual(anotacion, self.ticket_detail)

        return resultado.manual()


class Algorithm_Generic_Manual(object):
    """
    clase generica que procesa el resultado dependiendo de los grupos
    de apuesta, para tickets en los cuales las condiciones de apuesta
    han cambiado en el tiempo
    """

    def __init__(self, anotacion, ticket_detail):
        super(Algorithm_Generic_Manual, self).__init__()
        self.anotacion = anotacion
        self.ticket_detail = ticket_detail

    def manual(self):
        """
        Se identifica la modalidad en cuestion y se ejecuta el metodo
        correspondiente.
        """
        codename = self.ticket_detail.jugada.condicion.modalidad.codename
        if codename == 'runline':
            return self.runline()

        elif codename == 'alta/baja':
            return self.altabaja()

        elif codename == 'super_runline':
            return self.superrunline()

        elif codename == 'h+c+e':
            return self.hce()

    def runline(self):
        """
        Algoritmo que procesa resultados en la modalidad de runline
        """
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename='runline'
        )

        if jugadas.exists():
            if self.ticket_detail.condicion_ref:
                anotacionesdetail = self.anotacion.anotacionesdetail_set.all().exclude(
                    condicion__isnull=False
                )

                puntaje_hembra = None
                puntaje_macho = None
                ref = self.ticket_detail.condicion_ref.replace(' ', '')
                if not ref:
                    return
                ref = float(ref.replace(',', '.'))
                if ref > 0:
                    puntaje_hembra = anotacionesdetail.filter(
                        encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                    )[0].puntaje

                    puntaje_macho = anotacionesdetail.exclude(
                        encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                    )[0].puntaje
                else:
                    puntaje_macho = anotacionesdetail.filter(
                        encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                    )[0].puntaje

                    puntaje_hembra = anotacionesdetail.exclude(
                        encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                    )[0].puntaje

                if ref < 0:
                    resultante = puntaje_macho + ref
                    if resultante > puntaje_hembra:
                        return 'status_ganado'
                    elif resultante < puntaje_hembra:
                        return 'status_perdido'
                    elif resultante == puntaje_hembra:
                        return 'status_anulado'
                else:
                    resultante = puntaje_hembra + ref
                    if resultante > puntaje_macho:
                        return 'status_ganado'
                    elif resultante < puntaje_macho:
                        return 'status_perdido'
                    elif resultante == puntaje_macho:
                        return 'status_anulado'

    def altabaja(self):
        """
        Algoritmo que procesa resultados de alta baja
        """
        jugadas = Jugadas.objects.filter(
            encuentros_modalidad__encuentro_id=self.anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=self.anotacion.grupo_id,
            condicion__modalidad__codename='alta/baja'
        )

        if jugadas.exists():
            if self.ticket_detail.modalidad_ref:
                anotacionesdetail = self.anotacion.anotacionesdetail_set.all().exclude(
                    condicion__isnull=False
                )
                puntaje_total = 0

                for detail in anotacionesdetail:
                    puntaje_total += detail.puntaje
                    # obtenemos puntaje total

                ref = self.ticket_detail.modalidad_ref.replace(' ', '')
                if not ref:
                    return
                ref = float(ref.replace(',', '.'))

                # las jugadas tienen un atributo indice, el cual es ascendente
                # como la condicion es Alta/Baja (tener en cuenta es sobre la condicion,
                # xq hay una modalidad
                # que es Home/visitante, pero la condicion va, Visitante/home,
                # por lo tanto el indice 1 corresponde a visitante)

                if self.ticket_detail.jugada.indice == 1:
                    if puntaje_total > ref:
                        return 'status_ganado'
                    elif puntaje_total < ref:
                        return 'status_perdido'
                    elif puntaje_total == ref:
                        return 'status_anulado'
                elif self.ticket_detail.jugada.indice == 2:
                    if puntaje_total > ref:
                        return 'status_perdido'
                    elif puntaje_total < ref:
                        return 'status_ganado'
                    elif puntaje_total == ref:
                        return 'status_anulado'

    def superrunline(self):
        """
        Algoritmo que procesa la modalidad superrunline
        """
        # segun veo es el mismo codigo de runline,
        # no le encuentro la diferencia, solo que pertenece al grupo de combinadas
        resultado = self.anotacion.resultado
        # sus calculos los debe sacar de juego_completo
        # por eso para esta modaliad sobreescribo el campo anotacion
        if self.ticket_detail.condicion_ref:
            anotacion_copia = resultado.anotaciones_set.get(grupo__codename='juego_completo')
            # hago una copia de los resultados de juego completo xq se saca de alli
            anotacionesdetail = anotacion_copia.anotacionesdetail_set.all().exclude(
                condicion__isnull=False
            )
            puntaje_hembra = None
            puntaje_macho = None
            ref = self.ticket_detail.condicion_ref.replace(' ', '')
            if not ref:
                return
            ref = float(ref.replace(',', '.'))
            if ref > 0:
                puntaje_hembra = anotacionesdetail.filter(
                    encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                )[0].puntaje

                puntaje_macho = anotacionesdetail.exclude(
                    encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                )[0].puntaje
            else:
                puntaje_macho = anotacionesdetail.filter(
                    encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                )[0].puntaje

                puntaje_hembra = anotacionesdetail.exclude(
                    encuentro_detail_id=self.ticket_detail.jugada.detalle_encuentro_id,
                )[0].puntaje

            if ref < 0:
                resultante = puntaje_macho + ref
                if resultante > puntaje_hembra:
                    return 'status_ganado'
                elif resultante < puntaje_hembra:
                    return 'status_perdido'
                elif resultante == puntaje_hembra:
                    return 'status_anulado'
            else:
                resultante = puntaje_hembra + ref
                if resultante > puntaje_macho:
                    return 'status_ganado'
                elif resultante < puntaje_macho:
                    return 'status_perdido'
                elif resultante == puntaje_macho:
                    return 'status_anulado'

    def hce(self):
        """
        Algoritmo que procesa los resultados de la modalidad h+c+e
        """
        if self.ticket_detail.modalidad_ref:
            ref = self.ticket_detail.modalidad_ref.replace(' ', '')
            if not ref:
                return
            ref = float(ref.replace(',', '.'))
            anotacionesdetail = self.anotacion.anotacionesdetail_set.get(
                condicion__modalidad__codename='h+c+e'
            )
            alta = False
            baja = False
            anulado = False
            if anotacionesdetail.puntaje > ref:
                alta = True
            elif anotacionesdetail.puntaje < ref:
                baja = True
            else:
                anulado = True

            if anulado is True:
                return 'status_anulado'

            if self.ticket_detail.jugada.indice == 1:
                if alta is True:
                    return 'status_ganado'
            elif self.ticket_detail.jugada.indice == 2:
                if baja is True:
                    return 'status_ganado'
            return 'status_perdido'
