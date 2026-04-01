"""
fix_nonexistent_models.py
Elimina referencias a modelos que ya NO existen en admin_juego/models.py:
  Jugador, JugadorTipo, RestriccionesReferencias, SorteoTipoApuesta,
  Producto (→ no existe, usar TipoProducto si aplica)
En imports: los elimina del bloque from admin_juego.models import (...)
"""
import os, re

# Modelos que no existen y deben eliminarse de los imports
NONEXISTENT = {
    'Jugador', 'JugadorTipo', 'RestriccionesReferencias',
    'SorteoTipoApuesta', 'Producto',
}

ROOT = '.'
SKIP_DIRS = {'migrations', '__pycache__', '.git'}

fixed = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
    for filename in filenames:
        if not filename.endswith('.py') or filename.startswith('fix_'):
            continue
        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, encoding='utf-8', errors='replace') as fh:
                original = fh.read()
        except:
            continue

        content = original

        # Para cada modelo inexistente, eliminarlo de los imports
        for name in NONEXISTENT:
            # Patrón: ",\s*Name" o "Name,\s*" o sólo "Name" dentro de un import
            # Primero intentar eliminarlo con coma anterior
            content = re.sub(r',\s*\b' + re.escape(name) + r'\b', '', content)
            # Luego con coma posterior
            content = re.sub(r'\b' + re.escape(name) + r'\b\s*,\s*', '', content)
            # Finalmente si quedó solo
            content = re.sub(r'\b' + re.escape(name) + r'\b', '# REMOVED_' + name, content)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            fixed.append(filepath.replace('.\\', ''))

print(f'Corregidos: {len(fixed)} archivos')
for f in fixed:
    print(f'  {f}')
