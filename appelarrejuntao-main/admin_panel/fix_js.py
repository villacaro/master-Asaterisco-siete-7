"""
fix_js.py — Repara el JS roto en dashboard.html
Busca la función cargarUsuarios duplicada/rota y la reemplaza por una versión limpia.
"""
import re

TMPL = 'templates/arrejuntao/dashboard.html'

with open(TMPL, 'r', encoding='utf-8') as f:
    html = f.read()

# Encontrar el bloque JS completo (entre <script> y </script>)
m = re.search(r'(<script>)(.*?)(</script>)', html, re.DOTALL)
if not m:
    print("ERROR: no se encontró <script>")
    exit(1)

script_block = m.group(2)

# Mostrar todos los sitios donde hay 'cargarUsuarios' para diagnóstico
ocurrencias = [(i, script_block[max(0,i-30):i+80]) for i in range(len(script_block)) if script_block[i:i+15] == 'cargarUsuarios']
print(f"Ocurrencias de cargarUsuarios: {len(ocurrencias)}")
for pos, ctx in ocurrencias:
    print(f"  pos {pos}: {repr(ctx)}")

# Verificar si hay errores de balanceo de llaves al final del script
open_b  = script_block.count('{')
close_b = script_block.count('}')
print(f"Llaves abiertas: {open_b}, cerradas: {close_b}, diferencia: {open_b - close_b}")
