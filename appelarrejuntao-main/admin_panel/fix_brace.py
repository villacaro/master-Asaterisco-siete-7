"""
fix_brace.py — Encuentra y elimina la llave extra en el JS del dashboard.
"""
import re

TMPL = 'templates/arrejuntao/dashboard.html'

with open(TMPL, 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if not m:
    print("ERROR: no se encontró <script> block")
    exit(1)

js = m.group(1)
lines = js.split('\n')

# Rastrear balance de llaves línea por línea para encontrar el problema
balance = 0
problem_lines = []
for i, line in enumerate(lines):
    opens  = line.count('{')
    closes = line.count('}')
    balance += opens - closes
    # Marcar líneas donde balance va negativo momentáneamente (extra close)
    if balance < 0:
        problem_lines.append((i+1, balance, line))
        print(f"⚠️  Línea {i+1}: balance={balance}: {repr(line[:80])}")
        balance = 0  # reset para seguir buscando

print(f"\nTotal: {len(problem_lines)} líneas problemáticas")

if problem_lines:
    # La primera línea problemática tiene la llave extra
    bad_line_no = problem_lines[0][0] - 1  # 0-indexed
    bad_line = lines[bad_line_no]
    print(f"\nLínea a reparar (#{bad_line_no+1}):")
    print(repr(bad_line))

    # Contexto
    for j in range(max(0,bad_line_no-5), min(len(lines), bad_line_no+5)):
        marker = " >>> " if j == bad_line_no else "     "
        print(f"{marker}{j+1}: {lines[j]}")
