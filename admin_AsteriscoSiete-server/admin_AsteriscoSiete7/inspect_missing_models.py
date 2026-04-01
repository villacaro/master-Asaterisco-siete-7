"""
inspect_missing_models.py
Inspecciona los campos requeridos de los modelos que faltan.
"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings_local'
import django; django.setup()
from django.apps import apps

TARGET = [
    ('admin_juego',   'SistemaJuego'),
    ('admin_juego',   'Sorteo'),
    ('admin_finanzas','Comercializadora'),
    ('admin_users',   'Users'),
]

for app_label, model_name in TARGET:
    M = apps.get_model(app_label, model_name)
    print(f"\n{'='*60}")
    print(f"  {app_label}.{model_name}")
    print(f"  tabla: {M._meta.db_table}")
    print(f"{'='*60}")
    for f in M._meta.concrete_fields:
        null_info = "NULL" if f.null else "NOT NULL"
        default_info = f"default={f.default}" if f.has_default() else "sin default"
        fk_info = f" → FK({f.related_model.__name__})" if hasattr(f, 'related_model') and f.related_model else ""
        print(f"  {f.name:<35} {null_info:<10} {default_info:<25}{fk_info}")
