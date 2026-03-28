# -*- coding: utf-8 -*-

from api.api_models import juegos
from api.api_models.comercializacion import agencias, bancas, bloques, distribuidores
from django.conf.urls import include, patterns, url
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'encuentros', juegos.EncuentrosViewSet)
router.register(r'agencias', agencias.AgenciasViewSet)
router.register(r'distribuidores', distribuidores.DistribuidoresViewSet)
router.register(r'bancas', bancas.BancasViewSet)
router.register(r'bloques', bloques.BloquesViewSet)

urlpatterns = patterns(
    '',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
)
