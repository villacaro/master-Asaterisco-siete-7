"""
fix_arrejuntao_conflict.py
Renombra Sorteo→SorteoArrejuntao en models_arrejuntao.py
y actualiza admin.py de admin_juego para evitar el conflicto de modelos.
"""
import re

# --- 1. Renombrar en models_arrejuntao.py ---
f1 = 'admin_juego/models_arrejuntao.py'
with open(f1, encoding='utf-8', errors='replace') as fh:
    c = fh.read()

# Renombrar la clase y sus referencias internas
c = re.sub(r'\bclass Sorteo\b', 'class SorteoArrejuntao', c)
c = re.sub(r'\bSorteo\b', 'SorteoArrejuntao', c)

with open(f1, 'w', encoding='utf-8') as fh:
    fh.write(c)
print(f'OK: Sorteo → SorteoArrejuntao en {f1}')

# --- 2. Actualizar admin.py de admin_juego ---
f2 = 'admin_juego/admin.py'
with open(f2, encoding='utf-8', errors='replace') as fh:
    c2 = fh.read()

# Solo reemplazar en el contexto de importación de models_arrejuntao
# Buscamos el bloque de importación de ese módulo
c2 = c2.replace('from admin_juego.models_arrejuntao import (', 
                 'from admin_juego.models_arrejuntao import (')
# Reemplazar Sorteo en el contexto de admin arrejuntao
# Necesitamos ser precisos: solo donde se usa la clase del arrejuntao
c2 = re.sub(r'(\bfrom admin_juego\.models_arrejuntao import[^)]*)\bSorteo\b', 
            lambda m: m.group(0).replace('Sorteo', 'SorteoArrejuntao'), c2)

with open(f2, 'w', encoding='utf-8') as fh:
    fh.write(c2)
print(f'OK: admin.py actualizado en {f2}')
print('\nConflicto resuelto: SorteoArrejuntao != Sorteo (genérico)')
