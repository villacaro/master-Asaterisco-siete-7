from admin_comercializacion.models import Bloques, Operadoras
from api.api_models.comercializacion.base import BaseRetrieveSerializer
from rest_framework import serializers, viewsets


class BloquesRetrieveSerializer(BaseRetrieveSerializer, serializers.ModelSerializer):

    class Meta:
        model = Bloques
        fields = (
            # Atributos simples
            'nombre',
            'resumen_automatic',
            'telefono',
            'rif',
            'email',
            'direccion',
            'status',

            # Bloques
            'tipo',
            'is_sistema_juego',
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


class BloquesListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bloques
        fields = (
            'pk', 'nombre',
        )


class BloquesViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Bloques.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BloquesRetrieveSerializer
        else:
            return BloquesListSerializer

    def get_queryset(self):
        if self.action == 'list':
            if self.request.GET.get(Operadoras.prefix_filter):
                return self.queryset.filter(
                    operadora_id=self.request.GET.get(Operadoras.prefix_filter)
                ).only(
                    'pk', 'nombre',
                )
            else:
                return self.queryset.none()
        else:
            return self.queryset
