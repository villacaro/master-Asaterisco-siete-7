# -*- coding: utf-8 -*-

from api.api_models import juegos
from api.api_models.comercializacion import agencias, bancas, bloques, distribuidores
from django.urls import include, re_path
from rest_framework import routers

app_name = 'api'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'encuentros', juegos.EncuentrosViewSet)
router.register(r'agencias', agencias.AgenciasViewSet)
router.register(r'distribuidores', distribuidores.DistribuidoresViewSet)
router.register(r'bancas', bancas.BancasViewSet)
router.register(r'bloques', bloques.BloquesViewSet)

urlpatterns = [
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^api/', include(router.urls)),
]
