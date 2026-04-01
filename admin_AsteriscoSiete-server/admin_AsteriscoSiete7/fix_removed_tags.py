"""
fix_removed_tags.py
Reemplaza todos los marcadores # REMOVED_XXX (que quedaron en código activo)
por el modelo equivalente en el nuevo vocabulario de lotería.
"""
import os, re

# Mapa: # REMOVED_XXX → nuevo nombre real
RESTORE_MAP = {
    '# REMOVED_SorteoTipoApuesta': 'SorteoModalidades',
    '# REMOVED_RestriccionesReferencias': 'RestriccionesSorteo',
    '# REMOVED_JugadorTipo': 'TipoNumeroSorteo',
    '# REMOVED_Jugador': 'NumeroSorteo',
    '# REMOVED_Producto': 'TipoProducto',
    # En strings de FK (admin_juego.# REMOVED_Producto)
    "admin_juego.# REMOVED_Producto": "admin_juego.TipoProducto",
    # En verbose_name y strings normales
    'Nombre del # REMOVED_Producto': 'Nombre del Tipo de Producto',
}

ROOT = '.'
SKIP = {'migrations', '__pycache__', '.git'}
fixed = []

for dirp, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith('.')]
    for fn in files:
        if not fn.endswith('.py') or fn.startswith('fix_') or fn.startswith('rename_'):
            continue
        fp = os.path.join(dirp, fn)
        try:
            with open(fp, encoding='utf-8', errors='replace') as fh:
                orig = fh.read()
        except:
            continue

        if '# REMOVED_' not in orig:
            continue

        content = orig
        # Aplicar desde el más específico al más genérico
        for old, new in sorted(RESTORE_MAP.items(), key=lambda x: -len(x[0])):
            content = content.replace(old, new)

        if content != orig:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            fixed.append(fp.replace('.\\', ''))

print(f'Restaurados: {len(fixed)} archivos')
for f in fixed:
    print(f'  {f}')
