"""
fix_admin_sorteo_all.py
Reemplaza TODAS las referencias a 'Sorteo' (de models_arrejuntao) en admin.py
con 'SorteoArrejuntao'. Solo en el contexto del archivo admin.py.
"""
import re

f = 'admin_juego/admin.py'
with open(f, encoding='utf-8', errors='replace') as fh:
    c = fh.read()

# Reemplazar todas las referencias a Sorteo que NO sean SorteoArrejuntao
# ni parte de otro nombre compuesto
c = re.sub(r'\bSorteo\b(?!Arrejuntao)', 'SorteoArrejuntao', c)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print('OK: Todas las refs Sorteo → SorteoArrejuntao en admin.py')
