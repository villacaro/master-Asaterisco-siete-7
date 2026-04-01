from admin_comercializacion.models import Agencias, Distribuidores, Taquillas, UsuariosTaquilla
from api.api_models.comercializacion.base import BaseRetrieveSerializer
from rest_framework import serializers, viewsets


class UsuariosTaquillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuariosTaquilla
        fields = (
            'pk',
            'user',
            'nombre',
            'status',
        )


class TaquillasSerializer(serializers.ModelSerializer):

    usuariostaquilla = serializers.SerializerMethodField('usuariostaquilla_serializer')

    class Meta:
        model = Taquillas
        fields = (
            'pk',
            'taquilla',
            'monto_alquiler',
            'modo_alquiler',
            'is_taquilla_master',
            'usuariostaquilla',

        )

    def usuariostaquilla_serializer(self, obj):
        serializer = UsuariosTaquillaSerializer(
            obj.usuariostaquilla,
        )
        return serializer.data


class AgenciasRetrieveSerializer(BaseRetrieveSerializer, serializers.ModelSerializer):

    taquillas_set = serializers.SerializerMethodField('taquillas_set_serializer')

    class Meta:
        model = Agencias
        fields = (
            # Atributos simples
            'nombre',
            'resumen_automatic',
            'telefono',
            'rif',
            'email',
            'direccion',
            'status',
            'num_taquillas',
            'codigo',

            # Dependencias de taquilla
            'taquillas_set',

            # Preferencias
            'preferences_set',

            # Porcentajes
            'porcentajes_set',

            # Cupos
            'cupos_set',

            # Factor de riesgo
            'factores_set',

            # Permisos de venta
            'permissionssales_set',
            'permissionssalesrestrictions_set',
        )

    def taquillas_set_serializer(self, obj):
        serializer = TaquillasSerializer(
            obj.taquillas_set.all(),
            many=True,
        )
        return serializer.data


class AgenciasListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agencias
        fields = (
            'pk', 'nombre',
        )


class AgenciasViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Agencias.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AgenciasRetrieveSerializer
        else:
            return AgenciasListSerializer

    def get_queryset(self):
        if self.action == 'list':
            if self.request.GET.get(Distribuidores.prefix_filter):
                return self.queryset.filter(
                    distribuidores_id=self.request.GET.get(Distribuidores.prefix_filter)
                ).only(
                    'pk', 'nombre',
                )
            else:
                return self.queryset.none()
        else:
            return self.queryset
