"""
usuarios/models.py
No usamos base de datos para usuarios Firebase — son gestionados por Firebase Auth.
Solo necesitamos este archivo para que Django reconozca la app.
"""
from django.db import models
# Los "usuarios" son objetos de Firebase Auth, no modelos Django.
# Este archivo existe para que la app funcione correctamente.
