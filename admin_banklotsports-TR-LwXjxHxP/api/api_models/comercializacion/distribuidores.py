from admin_comercializacion.models import Bancas, Distribuidores
from api.api_models.comercializacion.base import BaseRetrieveSerializer
from rest_framework import serializers, viewsets


class DistribuidoresRetrieveSerializer(BaseRetrieveSerializer, serializers.ModelSerializer):

    class Meta:
        model = Distribuidores
        fields = (
            # Atributos simples
            'nombre',
            'resumen_automatic',
            'telefono',
            'rif',
            'email',
            'direccion',
            'status',

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


class DistribuidoresListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Distribuidores
        fields = (
            'pk', 'nombre',
        )


class DistribuidoresViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Distribuidores.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DistribuidoresRetrieveSerializer
        else:
            return DistribuidoresListSerializer

    def get_queryset(self):
        if self.action == 'list':
            if self.request.GET.get(Bancas.prefix_filter):
                return self.queryset.filter(
                    banca_id=self.request.GET.get(Bancas.prefix_filter)
                ).only(
                    'pk', 'nombre',
                )
            else:
                return self.queryset.none()
        else:
            return self.queryset
