# -*- coding: utf-8 -*-

from admin_finanzas.models import Comercializadora
from admin_lib.util_json import JsonDumps
from admin_users.models import UserProfile
from django.http import HttpResponse
from django.views.generic import View


class ComercializadorasListbyProfileAjax(View):

    def dispatch(self, request, *args, **kwargs):

        comercializadoras = Comercializadora.objects.none()
        for comercializadora in kwargs['object_user'].comercializadora.all():
            comercializadoras |= comercializadora.get_offspring_level1_by_profile(
                profile=UserProfile.get_userprofile_by_pk(pk=request.GET.get('profile'))
            )

        comercializadoras = comercializadoras.distinct()

        return HttpResponse(
            content=JsonDumps(
                [
                    {'pk': q.pk, 'nombre': '{0}'.format(q)}
                    for q in comercializadoras
                ]
            ),
            content_type='application/json'
        )
