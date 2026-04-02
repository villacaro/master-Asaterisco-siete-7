"""
find_extra.py — encuentra la línea HTML exact del `});` sobrante
"""
import re

TMPL = 'templates/arrejuntao/dashboard.html'
with open(TMPL, 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if not m:
    print("ERROR: no script block found")
    exit(1)

js = m.group(1)
script_start_pos = m.start(1)

lines_js = js.split('\n')
balance = 0
bad_js_line = None
for i, line in enumerate(lines_js):
    balance += line.count('{') - line.count('}')
    if balance < 0:
        bad_js_line = i
        break

if bad_js_line is None:
    print("No imbalanced line found"); exit()

# Now find the HTML line number
js_prefix = '\n'.join(lines_js[:bad_js_line+1])
pos_in_file = script_start_pos + len(js_prefix)
html_lines = content[:pos_in_file].split('\n')
html_line_no = len(html_lines)

print(f"JS line {bad_js_line+1} → HTML line {html_line_no}")
print(f"Contenido: {repr(lines_js[bad_js_line])}")

# Show surrounding HTML lines
all_lines = content.split('\n')
for j in range(max(0, html_line_no-5), min(len(all_lines), html_line_no+3)):
    marker = " >>> " if j == html_line_no-1 else "     "
    print(f"{marker}{j+1}: {all_lines[j]}")
