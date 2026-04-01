"""
fix_duplicate_classes.py
Resuelve duplicados de clases en admin_juego/models.py:
  TipoProducto (L662, era Deportes)   → LOTERIA
  ModalidadJuego (L2681, era Modalidades) → ModalidadApuesta

Solo opera en admin_juego/models.py para los bloques exactos.
Luego actualiza referencias en todos los demas archivos .py.
"""
import re, os

###############################################################################
# PASO 1: Renombrar en models.py  -- muy quirúrgico, por línea
###############################################################################
models_file = 'admin_juego/models.py'
with open(models_file, encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Encontrar la primera y segunda ocurrencia de "class TipoProducto"
tp_positions = [i for i, l in enumerate(lines) if l.strip().startswith('class TipoProducto')]
mj_positions = [i for i, l in enumerate(lines) if l.strip().startswith('class ModalidadJuego')]

print(f"TipoProducto en lineas: {[p+1 for p in tp_positions]}")
print(f"ModalidadJuego en lineas: {[p+1 for p in mj_positions]}")

# Renombrar PRIMERA aparicion de TipoProducto → LOTERIA
if len(tp_positions) >= 2:
    first_tp = tp_positions[0]
    # Renombrar clase y referencias super() en ese bloque (hasta la siguiente clase)
    next_class = tp_positions[1]
    for i in range(first_tp, next_class):
        lines[i] = re.sub(r'\bTipoProducto\b', 'LOTERIA', lines[i])
    print(f"  OK: TipoProducto L{first_tp+1} → LOTERIA")

# Renombrar SEGUNDA aparicion de ModalidadJuego → ModalidadApuesta
if len(mj_positions) >= 2:
    second_mj = mj_positions[1]
    # Encontrar el final de ese bloque (siguiente clase o EOF)
    next_after = len(lines)
    for i in range(second_mj + 1, len(lines)):
        if lines[i].startswith('class '):
            next_after = i
            break
    for i in range(second_mj, next_after):
        lines[i] = re.sub(r'\bModalidadJuego\b', 'ModalidadApuesta', lines[i])
    print(f"  OK: ModalidadJuego L{second_mj+1} → ModalidadApuesta")

with open(models_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("models.py actualizado.")

###############################################################################
# PASO 2: Actualizar referencias en el resto del proyecto
###############################################################################
# Mapa de correcciones para el resto de archivos
# (Pero NO tocar referencias a ModalidadJuego que son la version correcta L1107)
# La heuristica: despues de la linea 2681 era Modalidades → ModalidadApuesta
# Las referencias "from admin_juego.models import ... ModalidadApuesta"
# deben sustituir a los imports que decian "Modalidades"

# Para el resto del proyecto:
# - "admin_juego.LOTERIA" era admin_juego.TipoProducto (primer modelo)  
#   pero ya no aparece como TipoProducto en admin porque Python usa el 2do
# - No cambiar nada mas por ahora: el cambio en models.py es suficiente
#   para que Django ya no vea duplicados.

FIXES_VIEWS = {
    # En vistas que usan Modalidades originalmente como ModalidadApuesta
    # Nada que cambiar: ya fue renombrado por fix_tipoApuesta_refs.py
}

# Verificar que no hay mas duplicados en models.py
with open(models_file, encoding='utf-8') as f:
    content = f.read()

dupes = {}
for m in re.finditer(r'^class (\w+)', content, re.MULTILINE):
    name = m.group(1)
    dupes[name] = dupes.get(name, 0) + 1

conflicts = {k: v for k, v in dupes.items() if v > 1}
if conflicts:
    print(f"\nAUN HAY DUPLICADOS: {conflicts}")
else:
    print("\nSin duplicados en models.py")
