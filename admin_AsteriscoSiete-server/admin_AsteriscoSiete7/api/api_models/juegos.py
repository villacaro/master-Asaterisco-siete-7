# -*- coding: utf-8 -*-

from admin_asterisco7.settings import FORMAT_STR_DATETIME_SECONDS
from admin_juego.models import (
    Sorteo, SorteoDetalle, SorteoModalidades,
    ModalidadJuego, ModalidadPeriodo,
    GruposApuesta, Fechas, apuesta,
    TipoNumeroSorteo, NumeroSorteo,
    TipoProducto,
)
from django.utils.timezone import now
from rest_framework import serializers, viewsets


class JugadasSerializer(serializers.ModelSerializer):

    class Meta:
        model = apuesta
        exclude = (
            'sistema', 'origen', 'encuentros_modalidad',
            'pk_clone', 'created_at', 'updated_at'
        )


class EquiposSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModalidadJuego
        exclude = (
            'deporte', 'pk_clone', 'created_at', 'updated_at'
        )


class EquiposTemporadasSerializer(serializers.ModelSerializer):
    equipo = EquiposSerializer()

    class Meta:
        model = ModalidadPeriodo
        exclude = (
            'temporada', 'created_at', 'updated_at'
        )


class EncuentrosModalidadesSerializer(serializers.ModelSerializer):
    jugadas_set_filter = serializers.SerializerMethodField('jugadas_set')

    class Meta:
        model = SorteoModalidades
        exclude = (
            'encuentro', 'origen', 'sistema', 'pk_clone',
            'created_at', 'updated_at'
        )

    def jugadas_set(self, obj):
        serializer = JugadasSerializer(
            obj.jugadas_set.filter(origen=None),
            many=True
        )
        return serializer.data


class JugadorTipoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoNumeroSorteo
        exclude = (
            'deporte', 'pk_clone', 'created_at', 'updated_at'
        )


class JugadorSerializer(serializers.ModelSerializer):
    tipo = JugadorTipoSerializer()

    class Meta:
        model = NumeroSorteo
        exclude = (
            'equipos', 'pk_clone', 'created_at', 'updated_at'
        )


class EncuentrosDetailSerializer(serializers.ModelSerializer):
    equipos_temporadas = EquiposTemporadasSerializer()
    jugador = JugadorSerializer()

    class Meta:
        model = SorteoDetalle
        exclude = (
            'encuentro', 'pk_clone', 'created_at', 'updated_at'
        )


class TorneoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoProducto
        exclude = (
            'pk_clone', 'created_at', 'updated_at'
        )


class TemporadasSerializer(serializers.ModelSerializer):
    torneo = TorneoSerializer()

    class Meta:
        model = Fechas
        exclude = (
            'pk_clone', 'created_at', 'updated_at'
        )


class JornadasSerializer(serializers.ModelSerializer):
    temporadas = TemporadasSerializer()

    class Meta:
        model = Fechas
        exclude = (
            'sistema', 'pk_clone', 'created_at', 'updated_at'
        )


class GruposJuegoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GruposApuesta
        exclude = (
            'pk_clone', 'created_at', 'updated_at'
        )


class EncuentrosRetrieveSerializer(serializers.ModelSerializer):
    encuentrosdetail_set = EncuentrosDetailSerializer(
        many=True, read_only=True,
    )
    encuentrosmodalidades_set_filter = serializers.SerializerMethodField(
        'get_encuentrosmodalidades_set'
    )
    jornada = JornadasSerializer()
    grupo = GruposJuegoSerializer()
    horajuego = serializers.DateTimeField(format=FORMAT_STR_DATETIME_SECONDS)
    horacierre = serializers.DateTimeField(format=FORMAT_STR_DATETIME_SECONDS)
    created_at = serializers.DateTimeField(format=FORMAT_STR_DATETIME_SECONDS)
    updated_at = serializers.DateTimeField(format=FORMAT_STR_DATETIME_SECONDS)

    class Meta:
        model = Sorteo
        exclude = ('pk_clone', 'exists_tickets', 'updated_at_logros')

    def get_encuentrosmodalidades_set(self, obj):
        serializer = EncuentrosModalidadesSerializer(
            obj.encuentrosmodalidades_set.filter(origen=None),
            many=True
        )
        return serializer.data


class EncuentrosDetailSerializerList(serializers.ModelSerializer):
    equipos_temporadas = EquiposTemporadasSerializer()

    class Meta:
        model = SorteoDetalle
        fields = (
            'equipos_temporadas',
        )


class EncuentrosListSerializer(serializers.ModelSerializer):
    equipos = serializers.SerializerMethodField('equipos_filter')
    deporte = serializers.SerializerMethodField('get_deporte_name')
    torneo_temporada = serializers.SerializerMethodField('get_torneo_temporada_name')

    horajuego = serializers.DateTimeField(format=FORMAT_STR_DATETIME_SECONDS)
    updated_at = serializers.DateTimeField(format=FORMAT_STR_DATETIME_SECONDS)

    class Meta:
        model = Sorteo
        fields = (
            'pk', 'horajuego', 'updated_at', 'equipos', 'deporte', 'torneo_temporada'
        )

    def equipos_filter(self, obj):
        data = []
        names = False
        for equipo in obj.encuentrosdetail_set_order_all():
            data.append(
                equipo.equipos_temporadas.equipo.nombre
            )

            if names is False:
                self.deporte_name = '{0}'.format(
                    equipo.equipos_temporadas.equipo.deporte
                )

                self.torneo_temporada_name = '{0} {1}'.format(
                    equipo.equipos_temporadas.temporada,
                    equipo.equipos_temporadas.temporada.torneo,
                )

        return data

    def get_deporte_name(self, obj):
        return self.deporte_name

    def get_torneo_temporada_name(self, obj):
        return self.torneo_temporada_name


class EncuentrosViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Sorteo.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EncuentrosRetrieveSerializer
        else:
            return EncuentrosListSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return self.get_queryset_retrive()
        else:
            return self.get_queryset_list()

    def get_queryset_list(self):
        if self.request.GET.get('sistema') and self.request.GET.get('sistema').isdigit():
            return self.queryset.only(
                'pk', 'horajuego', 'updated_at',
            ).filter(
                horacierre__gt=now(),
                jornada__sistema_id=self.request.GET.get('sistema'),
            ).order_by(
                'jornada__temporadas__torneo__deporte__orden',
                'horajuego'
            )
        else:
            return self.queryset.none()

    def get_queryset_retrive(self):
        if self.request.GET.get('sistema') and self.request.GET.get('sistema').isdigit():
            return self.queryset.select_related(
                'status',
                'jornada__temporadas__torneo__deporte',
            ).filter(
                horacierre__gt=now()
            )
        else:
            return self.queryset.none()
