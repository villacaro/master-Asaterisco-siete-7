from admin_comercializacion.models import Cupos, Porcentajes
from admin_juego.models import TipoProducto
from admin_permisologia.models import PermissionsSales, PermissionsSalesRestrictions
from admin_profiles.models import Direcciones
from rest_framework import serializers


class DireccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direcciones
        fields = (
            'direccion',
            'parroquia',
            'municipio',
            'estado',
            'latitud',
            'longitud',
        )


class PorcentajesSerializer(serializers.ModelSerializer):
    tipo = serializers.SlugRelatedField(read_only=True, slug_field='codename')

    class Meta:
        model = Porcentajes
        fields = (
            'tipo',
            'relacion',
            'porcentaje_ganancia',
            'porcentaje_maximo',
            'bloque_porc',
            'banca_porc',
            'distribuidor_porc',
            'agencia_porc',
            'taquilla_porc',
        )


class CupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupos
        fields = (
            'monto_diario',
            'monto_premio',
        )


class PermissionsSalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionsSales
        fields = (
            'deporte',
            'grupo',
            'modalidad',
            'breaking',
        )


class PermissionsSalesRestrictionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionsSalesRestrictions
        fields = (
            'deporte',
            'restrictions',
        )


class BaseRetrieveSerializer(serializers.ModelSerializer):
    direccion = serializers.SerializerMethodField('direccion_serializer')
    preferences_set = serializers.SerializerMethodField('preferences_serializer')
    porcentajes_set = serializers.SerializerMethodField('porcentajes_serializer')
    cupos_set = serializers.SerializerMethodField('cupo_serializer')
    factores_set = serializers.SerializerMethodField('factores_serializer')
    permissionssales_set = serializers.SerializerMethodField('permissionssales_serializer')
    permissionssalesrestrictions_set = serializers.SerializerMethodField('permissionssalesrestrictions_serializer')

    def direccion_serializer(self, obj):
        serializer = DireccionesSerializer(
            obj.direccion
        )
        return serializer.data

    def preferences_serializer(self, obj):
        return obj.get_queryset_preferencias_serialize()

    def porcentajes_serializer(self, obj):
        serializer = PorcentajesSerializer(
            obj.porcentajes_set.filter(fecha_fin=None),
            many=True,
        )
        return serializer.data

    def cupo_serializer(self, obj):
        serializer = CupoSerializer(
            obj.cupos_set.get(fecha_fin=None),
            many=False,
        )
        return serializer.data

    def factores_serializer(self, obj):
        factor = obj.get_comercializadora().get_factores_riesgo()
        if not isinstance(factor, list):
            return factor.factores
        else:
            return factor

    def permissionssales_serializer(self, obj):
        serializer = PermissionsSalesSerializer(
            obj.get_comercializadora().get_restrictions_ventas(),
            many=True,
        )
        return serializer.data

    def permissionssalesrestrictions_serializer(self, obj):

        pks = []
        for deporte_pk in TipoProducto.objects.all().values_list('pk'):
            restric = obj.get_comercializadora().get_permissions_sales_restrictions(deporte_id=deporte_pk)
            if restric:
                pks.append(restric.pk)

        serializer = PermissionsSalesRestrictionsSerializer(
            PermissionsSalesRestrictions.objects.filter(pk__in=pks),
            many=True,
        )
        return serializer.data
