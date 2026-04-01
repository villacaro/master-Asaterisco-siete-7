"""
fix_candidatos_iframe.py
Elimina la segunda renderCandidatos() (la del iframe) del dashboard index.html
"""
import re

fpath = 'static/dashboard/index.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar posición de las dos ocurrencias
idx1 = content.find('function renderCandidatos()')
idx2 = content.find('function renderCandidatos()', idx1 + 10)

if idx2 < 0:
    print('Solo hay una renderCandidatos — nada que hacer')
    exit(0)

print(f'Primera en: {idx1}, Segunda en: {idx2}')

# Encontrar el bloque completo de la segunda (desde el comentario hasta el cierre de la función)
# Buscar el bloque de comentario que precede a la segunda función
block_start = content.rfind('// ══', 0, idx2)
if block_start < 0:
    block_start = idx2

# Encontrar el cierre: la primera '}' seguida de '\n' que cierra la función
# Buscamos "}\n\n" después del idx2 para que sea el cierre de la función
pos = idx2
depth = 0
i = pos
while i < len(content):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            block_end = i + 1
            break
    i += 1

print(f'Bloque a eliminar: caracteres {block_start} a {block_end}')
print('Contexto inicio:', repr(content[block_start:block_start+80]))
print('Contexto fin:', repr(content[block_end-50:block_end+30]))

# Eliminar el bloque y reemplazar con comentario
new_content = (
    content[:block_start] +
    '\n// [candidatos nativo — ver función arriba]\n' +
    content[block_end:]
)

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verificar que quedó una sola
count = new_content.count('function renderCandidatos()')
print(f'OK — ahora hay {count} ocurrencia(s) de renderCandidatos()')
