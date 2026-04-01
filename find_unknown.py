import pathlib, re

base = pathlib.Path(r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7')

for f in sorted(base.rglob('*.py')):
    if '__pycache__' in str(f): continue
    try:
        txt = f.read_text(encoding='utf-8', errors='replace')
        if "'UNKNOWN'" in txt:
            count = txt.count("'UNKNOWN'")
            print(f'{count}x {f.relative_to(base)}')
    except:
        pass
