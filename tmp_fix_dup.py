# Elimina la llamada duplicada a _loadHomeCandidatos() en línea 4773
file = r'c:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7\static\dashboard\index.html'
with open(file,'r',encoding='utf-8') as f:
    lines = f.readlines()

# Find all call occurrences (not function definitions)
call_lines = [i for i,l in enumerate(lines) if '_loadHomeCandidatos();' in l and 'async function' not in l]
print(f"Found {len(call_lines)} call(s) at line(s): {[i+1 for i in call_lines]}")

if len(call_lines) > 1:
    # Keep only the first (line ~3893), remove the rest
    for idx in call_lines[1:]:
        print(f"Removing duplicate call at line {idx+1}: {repr(lines[idx].strip())}")
        lines[idx] = ''  # blank out the line

    with open(file,'w',encoding='utf-8') as f:
        f.writelines(lines)
    print("Done. Duplicate removed.")
else:
    print("Only one call found — nothing to remove.")
