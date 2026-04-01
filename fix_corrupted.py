"""
fix_urls_smart.py
Analiza cada urls.py con errores y corrige el tipo especifico de bracket mismatch:
- Cierra parentesis de Menu.register() y Permissions.register() que quedaron como `]`
- Cierra la lista urlpatterns que quedo como `)`
Usa seguimiento de pila de brackets.
"""
import ast
import os
import re
import glob

BASE = r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7'

def fix_brackets(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    new_lines = []
    changed = False
    # Stack of ('char', line_index) - track what we opened
    stack = []

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        new_line = line

        # Count opens and closes in this line
        # But we need to know if a standalone ] or ) is mismatched
        
        # Check for standalone ] or ) (closing bracket by itself on a line)
        if re.match(r'^\s*[\]\)]\s*$', stripped):
            closing = stripped.strip()
            
            if stack:
                expected_open, open_line = stack[-1]
                
                # If we have a ] but the open was (, we need )
                if closing == ']' and expected_open == '(':
                    new_line = line.replace(']', ')', 1)
                    changed = True
                    stack.pop()
                # If we have a ) but the open was [, we need ]
                elif closing == ')' and expected_open == '[':
                    new_line = line.replace(')', ']', 1)
                    changed = True
                    stack.pop()
                else:
                    stack.pop()
            new_lines.append(new_line)
            continue

        # Track opens in non-standalone lines
        for char in stripped:
            if char in ('(', '['):
                stack.append((char, i))
            elif char in (')', ']'):
                if stack:
                    stack.pop()

        new_lines.append(line)

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    return changed


fixed = []
still_broken = []

for path in glob.glob(BASE + r'\**\urls.py', recursive=True):
    try:
        src = open(path, encoding='utf-8', errors='replace').read()
        try:
            ast.parse(src)
            continue
        except SyntaxError:
            pass

        # Try up to 5 passes (some files have multiple errors)
        for _ in range(10):
            fix_brackets(path)
            src = open(path, encoding='utf-8', errors='replace').read()
            try:
                ast.parse(src)
                fixed.append(os.path.relpath(path, BASE))
                break
            except SyntaxError:
                pass
        else:
            e_msg = ''
            try:
                ast.parse(open(path, encoding='utf-8', errors='replace').read())
            except SyntaxError as e:
                e_msg = f':{e.lineno} - {e.msg}'
            still_broken.append(f'{os.path.relpath(path, BASE)}{e_msg}')

    except Exception as e:
        still_broken.append(f'{path}: ERROR {e}')

print(f'Fixed: {len(fixed)}')
for p in fixed:
    print(' OK:', p)
print(f'Still broken: {len(still_broken)}')
for p in still_broken:
    print(' BROKEN:', p)
