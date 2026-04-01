"""
find_unresolved_fk.py
Busca todos los modelos que tienen ForeignKey/ManyToMany cuyo modelo destino
sigue siendo un string sin resolver (no se ha completado el lazy lookup de Django).
"""
import os
import sys
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.apps import apps

print("=== BUSCANDO ForeignKey con modelo destino como STRING ===")
found = 0

for model in apps.get_models():
    for field in model._meta.get_fields():
        if not hasattr(field, 'remote_field') or field.remote_field is None:
            continue
        rel_model = field.remote_field.model
        if isinstance(rel_model, str):
            print(f"  PROBLEMA: {model._meta.app_label}.{model.__name__}.{field.name} -> '{rel_model}'")
            found += 1

if found == 0:
    print("  Ninguna FK sin resolver encontrada.")
else:
    print(f"\n  Total: {found} FKs sin resolver.")
