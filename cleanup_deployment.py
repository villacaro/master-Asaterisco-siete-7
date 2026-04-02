#!/usr/bin/env python
"""cleanup_deployment.py

Este script ejecuta los utilitarios de limpieza del proyecto y elimina
cualquier referencia a tablespaces (ts_comer, ts_parley) que aparecen en
modelos o migraciones.  Se puede ejecutar antes de generar la imagen de
producción.
"""
import os
import re
import subprocess
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def run_script(path):
    """Ejecuta un script Python y muestra su salida."""
    full_path = os.path.join(PROJECT_ROOT, path)
    if not os.path.exists(full_path):
        print(f"[WARN] {path} no encontrado")
        return
    print(f"[RUN] {path}")
    subprocess.run([sys.executable, full_path], check=False)

def remove_tablespace_refs():
    """Busca y elimina líneas que contengan 'db_tablespace' en todo el árbol.
    Se modifica in‑place.
    """
    pattern = re.compile(r"['\"]?db_tablespace['\"]?\s*[:=]\s*['\"](?:ts_comer|ts_parley|ts_finance)['\"]")
    for root, _, files in os.walk(PROJECT_ROOT):
        for fn in files:
            if fn.endswith('.py'):
                file_path = os.path.join(root, fn)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                new_lines = []
                changed = False
                for line in lines:
                    if pattern.search(line):
                        changed = True
                        continue
                    new_lines.append(line)
                if changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"[MOD] Eliminado tablespace en {file_path}")

if __name__ == '__main__':
    # 1. Ejecutar los scripts de limpieza existentes
    run_script('fix_removed_tags.py')
    # El script find_unresolved_fk.py puede no existir en todas las versiones;
    # si está presente lo ejecutamos.
    run_script('find_unresolved_fk.py')
    # 2. Eliminar referencias a tablespaces
    remove_tablespace_refs()
    print('Limpieza completada.')
