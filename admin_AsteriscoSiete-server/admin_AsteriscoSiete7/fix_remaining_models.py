"""
fix_remaining_models.py
Corrige todos los modelos faltantes que quedan en el proyecto.
Mapeo final basado en los modelos reales en admin_juego/models.py.
"""
import os, re

# Mapeo definitivo de nombres incorrectos → nombres correctos (los que existen en models.py)
FIXES = {
    'EquiposTemporadas':    'ModalidadPeriodo',
    'EquiposLigas':         'ModalidadProducto',
    'EquiposGrupos':        'ModalidadGrupo',
    'GruposJuego':          'GruposApuesta',
    'GruposApuestas':       'GruposApuesta',      # plural erróneo
    'SorteoModalidades':    'SorteoModalidades',  # ya existe, no cambiar
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
        content = orig
        for old, new in FIXES.items():
            if old == new:
                continue
            content = re.sub(r'\b' + re.escape(old) + r'\b', new, content)
        if content != orig:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            fixed.append(fp.replace('.\\', ''))

print(f'Corregidos: {len(fixed)} archivos')
for f in fixed:
    print(f'  {f}')
