"""
fix_tipoApuesta_refs.py
TipoApuesta no existe en models.py — el modelo correcto es ModalidadJuego.
También TipoProducto_Grupos → existe, ModalidadJuego_Grupos → existe.
Corrige todos los archivos del proyecto que tengan esas referencias.
"""
import os, re

# Correcciones finales de nombres
FIXES = {
    'TipoApuesta':        'ModalidadJuego',
    'TipoApuesta_Grupos': 'ModalidadJuego_Grupos',
}

ROOT = '.'
SKIP = {'migrations', '__pycache__', '.git'}
fixed = []

for dirp, dirnames, files in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith('.')]
    for fn in files:
        if not fn.endswith('.py') or fn.startswith('fix_'):
            continue
        fp = os.path.join(dirp, fn)
        try:
            with open(fp, encoding='utf-8', errors='replace') as fh:
                orig = fh.read()
        except:
            continue
        content = orig
        for old, new in FIXES.items():
            content = re.sub(r'\b' + re.escape(old) + r'\b', new, content)
        if content != orig:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            fixed.append(fp.replace('.\\', ''))

print(f'Corregidos: {len(fixed)} archivos')
for f in fixed:
    print(f'  {f}')
