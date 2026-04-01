"""
fix_all_imports.py
Corrige todos los imports de modelos con nombres viejos (Deportes, Encuentros, etc.)
en views, forms, y otros archivos Python del proyecto (EXCEPTO migrations/).
"""
import os
import re

# Mapa de renombres: nombre_viejo → nombre_nuevo
RENAME_MAP = {
    'Deportes_Grupos':       'TipoProducto_Grupos',
    'Deportes':              'TipoProducto',
    'Torneos':               'Producto',
    'Equipos':               'ModalidadJuego',
    'Modalidades_Grupos':    'ModalidadJuego_Grupos',
    'Modalidades':           'TipoApuesta',
    'Encuentros':            'Sorteo',
    'EncuentrosDetail':      'SorteoDetalle',
    'EncuentrosModalidades': 'SorteoTipoApuesta',
    'Jornadas':              'Fechas',
    'Temporadas':            'Fechas',
    'GruposApuestas':        'GruposApuesta',
    # Nombres que no existen en models.py → usar equivalente correcto
    'Jugadas':               'apuesta',
    'Jugador':               'Jugador',  # mantener si existe
    'JugadorTipo':           'JugadorTipo',  # mantener si existe
}

ROOT = '.'
SKIP_DIRS = {'migrations', '__pycache__', '.git', 'fix_'}

fixed_files = []
errors = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    # Excluir directorios de migraciones y cache
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
    
    for filename in filenames:
        if not filename.endswith('.py'):
            continue
        # No tocar los scripts de fix
        if filename.startswith('fix_') or filename.startswith('rename_'):
            continue
        
        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, encoding='utf-8', errors='replace') as fh:
                original = fh.read()
        except Exception as e:
            errors.append(f'LEER {filepath}: {e}')
            continue
        
        content = original
        changed = False
        
        for old_name, new_name in RENAME_MAP.items():
            if old_name == new_name:
                continue
            if old_name in content:
                # Solo reemplazar como palabra completa
                new_content = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, content)
                if new_content != content:
                    content = new_content
                    changed = True
        
        if changed:
            try:
                with open(filepath, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                fixed_files.append(filepath.replace('.\\', ''))
            except Exception as e:
                errors.append(f'ESCRIBIR {filepath}: {e}')

print(f'\nArchivos corregidos: {len(fixed_files)}')
for f in fixed_files:
    print(f'  ✓ {f}')

if errors:
    print(f'\nErrores: {len(errors)}')
    for e in errors:
        print(f'  ✗ {e}')

print('\nListo.')
