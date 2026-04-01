# -*- coding: utf-8 -*-

from admin_lib.util_json import JsonDumps
from admin_profiles.models import Municipios, Parroquias
from django.http import HttpResponse
from django.views.generic import View


class CapitalesListAjax(View):

    def dispatch(self, request, *args, **kwargs):

        capitales = Municipios.objects.filter(
            estado_id=request.REQUEST.get('estado')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    capitales.values(
                        "pk",
                        "capital"
                    )
                )
            ),
            content_type='application/json'
        )


class MunicipiosListAjax(View):

    def dispatch(self, request, *args, **kwargs):

        municipios = Municipios.objects.filter(
            estado_id=request.REQUEST.get('estado')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    municipios.values(
                        "pk",
                        "nombre"
                    )
                )
            ),
            content_type='application/json'
        )


class MunicipioListAjax(View):

    def dispatch(self, request, *args, **kwargs):

        municipios = Municipios.objects.filter(
            pk=request.REQUEST.get('ciudad')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    municipios.values(
                        "pk",
                        "nombre"
                    )
                )
            ),
            content_type='application/json'
        )


class CiudadesListAjax(View):

    def dispatch(self, request, *args, **kwargs):

        ciudades = Parroquias.objects.filter(
            municipio_id=request.REQUEST.get('municipio')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    ciudades.values(
                        "pk",
                        "nombre"
                    )
                )
            ),
            content_type='application/json'
        )
