#!/usr/bin/env python
"""Diagnóstico del ContentType ID 66 y otros errores del admin."""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings')

import django
django.setup()

from django.contrib.contenttypes.models import ContentType

print("=" * 60)
ct = ContentType.objects.filter(pk=66).first()
if ct:
    print(f"ContentType 66: app_label={ct.app_label!r}, model={ct.model!r}")
    print(f"  tipo app_label: {type(ct.app_label)}")
    try:
        model_class = ct.model_class()
        print(f"  Clase: {model_class}")
    except Exception as e:
        print(f"  Error al obtener clase: {e}")
else:
    print("ContentType 66 NO EXISTE en la BD")

print("\nTodos los ContentTypes:")
for c in ContentType.objects.all().order_by('pk'):
    print(f"  {c.pk:3d}: {c.app_label}.{c.model}")
