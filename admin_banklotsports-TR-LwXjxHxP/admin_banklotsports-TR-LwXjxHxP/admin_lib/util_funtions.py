# -*- coding: utf-8 -*-
from decimal import Decimal


def get_decimal_is_not_none(valor_decimal):
    if valor_decimal:
        return valor_decimal
    else:
        return Decimal(str("0.00"))


def FiltersCadenaCsv(request):
    from admin_finanzas.models import Comercializadora
    filters = []

    if request.POST.get("bloque"):
        filters.append("Multibanca:")
        filters.append(Comercializadora.objects.get(bloque_id=request.POST.get('bloque')).get_object().nombre)

    if request.POST.get("banca"):
        filters.append("Banca:")
        filters.append(Comercializadora.objects.get(banca_id=request.POST.get('banca')).get_object().nombre)

    if request.POST.get("distribuidor"):
        filters.append("Distribuidor:")
        filters.append(
            Comercializadora.objects.get(
                distribuidor_id=request.POST.get('distribuidor')).get_object().nombre)

    if request.POST.get("agencia"):
        filters.append("Agencia:")
        filters.append(Comercializadora.objects.get(agencia_id=request.POST.get('agencia')).get_object().nombre)

    if len(filters) == 0:
        filters.append("Todos los comercializadores")

    return filters


def ObtenerObjectPorcentaje(codename, cadena, fecha):
    from admin_comercializacion.models import Porcentajes
    kwargs = {
        "tipo__codename": codename,
    }

    kwargs[cadena.prefix_filter + "_id"] = cadena.pk

    porcentaje = Porcentajes.objects.filter(
        **kwargs
    )

    if porcentaje.count() == 0:
        porcentaje = None
    elif porcentaje.count() == 1:
        porcentaje = porcentaje[0]
    else:
        porcentaje.filter(
            fecha_inicio__gte=fecha,
            fecha_fin__lte=fecha
        )
        if porcentaje.count() == 1:
            porcentaje = porcentaje[0]
        else:
            porcentaje = porcentaje.filter(
                fecha_fin=None
            )
            if porcentaje.count() == 1:
                porcentaje = porcentaje[0]
            else:
                porcentaje = None
    return porcentaje


def get_agencias_alquiler_by_frecuencia(frecuencia):
    from admin_comercializacion.models import Bancas, Agencias

    agencias = Agencias.objects.only('id').filter(
        distribuidores__banca__modelo_negocio=Bancas.modelo_negocio_codenames[
            'codename_negocio_alquiler']
    )
    array = []
    for agencia in agencias:
        if agencia.get_preference_value_by_codename(
                'preference_amount_rental_frequency') == frecuencia:
            array.append(agencia.id)

    return array
