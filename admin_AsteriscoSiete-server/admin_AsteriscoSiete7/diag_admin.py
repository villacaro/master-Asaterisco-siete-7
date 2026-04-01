"""
Diagnostico: encuentra el admin inline cuya FK apunta a un string (no a un modelo).
"""
import os
import sys
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.admin.sites import all_sites
from django.contrib.admin import helpers
from django.contrib.admin.utils import get_fields_from_path
from django.apps import apps

print("=== Revisando InlineModelAdmin registrados ===")

for site in all_sites:
    for model, admin_obj in site._registry.items():
        for inline_cls in admin_obj.inlines:
            try:
                inline_instance = inline_cls(model, site)
                fk_field = inline_instance.fk_name
                inline_model = inline_cls.model

                if inline_model is None:
                    print(f"  [WARN] {inline_cls.__name__} sin modelo")
                    continue

                # Comprobar si hay FKs con string como destino
                for field in inline_model._meta.get_fields():
                    if hasattr(field, 'remote_field') and field.remote_field:
                        rel_model = field.remote_field.model
                        if isinstance(rel_model, str):
                            print(f"  [ERROR] {inline_cls.__name__} -> campo {field.name} -> FK a STRING: '{rel_model}'")
            except Exception as e:
                if '_meta' in str(e) or 'str' in str(e).lower():
                    print(f"  [CRASH] {inline_cls.__name__} en {admin_obj.__class__.__name__}: {e}")

print("=== Fin del diagnostico ===")
