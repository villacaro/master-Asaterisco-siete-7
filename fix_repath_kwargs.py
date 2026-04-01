"""
Convierte re_path(regex=..., view=..., name=...) al formato posicional correcto de Django 4+:
re_path(r'...', view, name='...')

También corrige todos los archivos urls.py del proyecto que usen este patrón.
"""
import pathlib
import re

base = pathlib.Path(r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7')

def fix_repath_kwargs(content):
    """
    Convierte bloques:
        re_path(
            regex=r'...',
            view=SomeView.as_view(),
            name='some_name'
        )
    en:
        re_path(r'...', SomeView.as_view(), name='some_name')
    """
    # Pattern: re_path( ... regex=... view=... name=... )
    # This regex captures multiline re_path calls with kwargs
    pattern = re.compile(
        r're_path\(\s*'
        r'regex\s*=\s*(r?[\'"].*?[\'"])\s*,\s*'
        r'view\s*=\s*(.*?)\s*,\s*'
        r'name\s*=\s*(r?[\'"].*?[\'"])\s*'
        r'\)',
        re.DOTALL
    )
    
    def replacer(m):
        regex_val = m.group(1).strip()
        view_val = m.group(2).strip()
        name_val = m.group(3).strip()
        return f"re_path({regex_val}, {view_val}, name={name_val})"
    
    new_content = pattern.sub(replacer, content)
    return new_content

count = 0
for f in sorted(base.rglob('urls.py')):
    if '__pycache__' in str(f): continue
    try:
        txt = f.read_text(encoding='utf-8', errors='replace')
        if 'regex=' not in txt:
            continue
        new = fix_repath_kwargs(txt)
        if new != txt:
            f.write_text(new, encoding='utf-8')
            count += 1
            matches = txt.count('regex=')
            print(f'Fixed {matches} re_path calls in: {f.relative_to(base)}')
    except Exception as e:
        print(f'ERROR {f}: {e}')

print(f'\nTotal files fixed: {count}')
