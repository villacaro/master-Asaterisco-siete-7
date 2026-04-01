"""
rebrand.py - Reemplaza todas las referencias de branding antiguo:
  banklot / BanklotSports / banklot_sports -> Asterisco Siete
  sportparley / SportParley -> Unicornn
Solo en archivos de texto (.py, .txt, .rst, .cfg, .sh, .json, .md, .html)
NO modifica nombres de carpetas ni archivos binarios.
"""
import os
import re

BASE = r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7'

EXTENSIONS = {'.py', '.txt', '.rst', '.cfg', '.sh', '.json', '.md', '.html', '.yml'}

# Reemplazos ordenados de mas especifico a mas general (case-insensitive con preservacion)
REPLACEMENTS = [
    # banklot variants
    (r'BanklotSports',   'Asterisco Siete'),
    (r'banklot_sports',  'asterisco_siete'),
    (r'banklot-sports',  'asterisco-siete'),
    (r'Banklot Sports',  'Asterisco Siete'),
    (r'banklot sports',  'asterisco siete'),
    (r'Banklot',         'Asterisco Siete'),
    (r'banklot',         'asterisco_siete'),
    # sportparley variants
    (r'SportParley',     'Unicornn'),
    (r'sport_parley',    'unicornn'),
    (r'sport-parley',    'unicornn'),
    (r'Sport Parley',    'Unicornn'),
    (r'sportparley',     'unicornn'),
]

fixed = []

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'migrations')]
    for fname in files:
        ext = os.path.splitext(fname)[1].lower()
        if ext not in EXTENSIONS:
            continue
        path = os.path.join(root, fname)
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            original = content
            for pattern, replacement in REPLACEMENTS:
                content = re.sub(pattern, replacement, content)

            if content != original:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed.append(os.path.relpath(path, BASE))
        except Exception as e:
            print(f'ERROR {path}: {e}')

print(f'Rebranded {len(fixed)} files:')
for p in fixed:
    print(' -', p)
