from admin_comercializacion.models import Bancas, Bloques
from api.api_models.comercializacion.base import BaseRetrieveSerializer
from rest_framework import serializers, viewsets


class BancasRetrieveSerializer(BaseRetrieveSerializer, serializers.ModelSerializer):

    class Meta:
        model = Bancas
        fields = (
            # Atributos simples
            'nombre',
            'resumen_automatic',
            'telefono',
            'rif',
            'email',
            'direccion',
            'status',

            # Bancas
            'is_sistema_juego',
            'modelo_negocio',
            'permissions_create_user',
            'is_resultados',
            'is_logros',

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


class BancasListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bancas
        fields = (
            'pk', 'nombre',
        )


class BancasViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Bancas.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BancasRetrieveSerializer
        else:
            return BancasListSerializer

    def get_queryset(self):
        if self.action == 'list':
            if self.request.GET.get(Bloques.prefix_filter):
                return self.queryset.filter(
                    bloque_id=self.request.GET.get(Bloques.prefix_filter)
                ).only(
                    'pk', 'nombre',
                )
            else:
                return self.queryset.none()
        else:
            return self.queryset
