"""
Script que extrae el contexto real de cada FK 'UNKNOWN' para identificar correctamente
el nombre del campo y su modelo destino.
"""
import pathlib, re

base = pathlib.Path(r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7')

target_files = [
    'admin_finanzas/models.py',
    'admin_apuestas/models.py',
    'admin_comercializacion/models.py',
    'admin_permisologia/models.py',
    'admin_resultados/models.py',
    'admin_themes/models.py',
    'admin_users/models.py',
    'admin_mail/models.py',
    'admin_juego/models.py',
    'admin_juego/models_arrejuntao.py',
    'admin_datamart/models.py',
]

for rel in target_files:
    f = base / rel.replace('/', '\\')
    if not f.exists(): continue
    txt = f.read_text(encoding='utf-8', errors='replace')
    lines = txt.splitlines()
    print(f'\n=== {rel} ===')
    for i, line in enumerate(lines):
        if "'UNKNOWN'" in line:
            # Look back to find the field name
            field_name = '???'
            for j in range(i-1, max(0, i-5), -1):
                m = re.match(r'\s*(\w+)\s*=\s*models\.(?:ForeignKey|ManyToManyField|OneToOneField)', lines[j])
                if m:
                    field_name = m.group(1)
                    break
            # Also check class context
            class_name = '???'
            for j in range(i-1, max(0, i-50), -1):
                m = re.match(r'class (\w+)', lines[j])
                if m:
                    class_name = m.group(1)
                    break
            print(f'  [{class_name}.{field_name}] line {i+1}: {lines[i].strip()}')
