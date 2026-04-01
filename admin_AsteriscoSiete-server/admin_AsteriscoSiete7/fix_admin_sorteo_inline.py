"""
fix_admin_sorteo_inline.py
Corrige la referencia 'model = Sorteo' en el inline de admin_juego/admin.py
para usar SorteoArrejuntao que es la clase correcta de models_arrejuntao.
"""

f = 'admin_juego/admin.py'
with open(f, encoding='utf-8', errors='replace') as fh:
    c = fh.read()

# En el inline SorteoInline, model = Sorteo debe ser SorteoArrejuntao
c = c.replace('model  = Sorteo', 'model  = SorteoArrejuntao')
c = c.replace('model = Sorteo',  'model = SorteoArrejuntao')

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(c)
print('OK: model = Sorteo → model = SorteoArrejuntao en admin.py')
