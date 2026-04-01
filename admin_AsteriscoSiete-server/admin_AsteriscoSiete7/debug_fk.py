"""
debug_fk.py — Encuentra qué InlineModelAdmin tiene un FK no resuelto.
Ejecutar: python debug_fk.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings')
django.setup()

from django.contrib import admin
from django.forms.models import _get_foreign_key

admin.autodiscover()

for model, modeladmin in admin.site._registry.items():
    for i, inline_class in enumerate(modeladmin.inlines):
        try:
            inline_obj = inline_class(model, admin.site)
            parent_model = model
            child_model = inline_obj.model
            
            # Verificar todas las FKs del modelo hijo
            for field in child_model._meta.get_fields():
                if hasattr(field, 'remote_field') and field.remote_field:
                    remote = field.remote_field.model
                    if isinstance(remote, str):
                        print(f"[STRING FK ENCONTRADO]")
                        print(f"  ModelAdmin:   {modeladmin.__class__.__name__}")
                        print(f"  Parent model: {model.__name__}")
                        print(f"  Inline class: {inline_class.__name__}")
                        print(f"  Child model:  {child_model.__name__}")
                        print(f"  FK field:     {field.name}")
                        print(f"  Target str:   '{remote}'")
                        print()
        except Exception as e:
            print(f"[ERROR] {modeladmin.__class__.__name__} inline[{i}] = {inline_class.__name__}: {e}")
