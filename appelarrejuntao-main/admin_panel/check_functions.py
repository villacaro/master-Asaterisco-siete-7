"""
check_functions.py — verifica qué funciones JS existen en el template
"""
TMPL = 'templates/arrejuntao/dashboard.html'
with open(TMPL, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fns = ['consultarListaLinea', 'initFechas', 'aplicarBloqueo', 'renderBV', 'agregarRiesgo', 'limpiarCR', 'cargarDashboard', 'cargarSorteos']
for fn in fns:
    found = [(i+1, l.strip()) for i, l in enumerate(lines) if f'function {fn}' in l]
    if found:
        print(f"✅ {fn}: línea {found[0][0]}")
    else:
        print(f"❌ {fn}: NO ENCONTRADA")
