"""
fix_admin_imports.py
Corrige el bloque de importación de models_arrejuntao en admin_juego/admin.py
para usar los nombres exactos de las clases que realmente existen.
"""

f = 'admin_juego/admin.py'
with open(f, encoding='utf-8', errors='replace') as fh:
    c = fh.read()

# Reemplazar nombres incorrectos en el import
c = c.replace('LiquidacionSorteoArrejuntao', 'LiquidacionSorteo')
c = c.replace('ResultadoSorteoArrejuntao', 'ResultadoSorteo')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print('OK: importaciones corregidas en admin.py')
print('  LiquidacionSorteoArrejuntao → LiquidacionSorteo')
print('  ResultadoSorteoArrejuntao   → ResultadoSorteo')
