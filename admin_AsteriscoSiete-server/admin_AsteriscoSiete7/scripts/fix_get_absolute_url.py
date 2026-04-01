#!/usr/bin/env python
"""
fix_get_absolute_url.py
Corrige todos los get_absolute_url que retornan una tupla (sintaxis antigua de
@models.permalink, eliminada en Django 3.1) a usar reverse() directamente.

Patrón viejo:
    def get_absolute_url(self):
        return ('some_url_name', (), {'pk': self.pk})

Patrón nuevo:
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('some_url_name', kwargs={'pk': self.pk})
        except NoReverseMatch:
            ...fallback...
"""
import re
import os

# Archivos a procesar (relativos al directorio de ejecución)
FILES_TO_FIX = [
    'admin_juego/models.py',
    'admin_finanzas/models.py',
    'admin_users/models.py',
    'admin_permisologia/models.py',
    'admin_apuestas/models.py',
]

# Patrón: línea con return ('url_name', (), {'pk': self.pk})
# o       return ('url_name', (), {'pk': self.pk_origin})
PATTERN = re.compile(
    r"""([ \t]*)return \('([a-z_]+)',\s*\(\),\s*\{'pk':\s*(self\.pk[a-z_]*)\}\)""",
    re.MULTILINE
)


def make_replacement(indent, url_name, pk_expr):
    return (
        f"{indent}from django.urls import reverse, NoReverseMatch\n"
        f"{indent}try:\n"
        f"{indent}    return reverse('{url_name}', kwargs={{'pk': {pk_expr}}})\n"
        f"{indent}except NoReverseMatch:\n"
        f"{indent}    return '/admin/'"
    )


total_fixed = 0
for rel_path in FILES_TO_FIX:
    abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), rel_path)
    if not os.path.exists(abs_path):
        print(f"  [SKIP] {rel_path} — no encontrado")
        continue

    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    count = 0

    def replacer(m):
        global count
        count += 1
        return make_replacement(m.group(1), m.group(2), m.group(3))

    content = PATTERN.sub(replacer, content)

    if count > 0:
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] {rel_path} — {count} reemplazo(s)")
        total_fixed += count
    else:
        print(f"  [--] {rel_path} — sin cambios necesarios")

print(f"\nTotal reemplazos: {total_fixed}")
