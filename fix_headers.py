"""
Line-based replacement using content search (file grew by 3 lines from FIX1).
Fixes:
  - Receipt: adds draw time (hora) and proper delete icon with styling
"""
path = r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7\admin_asterisco7\templates\taquilla\index.html'

with open(path, 'rb') as f:
    lines = f.readlines()  # each line includes \r\n

# ─── Find the Object.entries forEach block ──────────────────────
start_idx = None
for i, line in enumerate(lines):
    if b'Object.entries(groups).forEach' in line and b'lotteryName' in line:
        start_idx = i
        break

if start_idx is None:
    print('ERROR: Object.entries block not found')
    exit(1)

print(f'Found Object.entries block at line {start_idx+1} (1-indexed)')

# Print surrounding lines for verification
for j in range(start_idx, min(start_idx+20, len(lines))):
    print(f'  L{j+1}: {repr(lines[j][:100])}')

# ─── Find end of the forEach block (the closing '});') ──────────
end_idx = None
for i in range(start_idx, start_idx + 30):
    if lines[i].strip() == b'});':
        end_idx = i
        break

if end_idx is None:
    print('ERROR: end of forEach block not found')
    exit(1)

print(f'End of block at line {end_idx+1}')

# ─── Build the replacement block ────────────────────────────────
REPLACE = [
    b'            Object.entries(groups).forEach(([lotteryName, bets]) => {\r\n',
    b'                // Suma del grupo\r\n',
    b'                const groupTotal = bets.reduce((s, b) => s + b.amount, 0);\r\n',
    b'                const drawLabel = bets[0] && bets[0].drawLabel ? bets[0].drawLabel : \'\';\r\n',
    b'                const deleteBtn = `<div onclick="removeBetGroup(\'${lotteryName}\')" '
    b'class="w-5 flex justify-center items-center cursor-pointer text-gray-400 '
    b'hover:text-red-600 transition-colors ml-1 flex-shrink-0" title="Quitar apuesta">'
    b'<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
    b'<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" '
    b'd="M6 18L18 6M6 6l12 12"></path></svg></div>`;\r\n',
    b'\r\n',
    b'                // Encabezado de loter\xc3\xada: nombre + hora sorteo + monto + bot\xc3\xb3n eliminar\r\n',
    b'                itemsHtml += `\r\n',
    b'                    <div class="receipt-item-row font-bold mt-2">\r\n',
    b'                        <div class="flex flex-col min-w-0">\r\n',
    b'                            <span class="receipt-lottery-name">${lotteryName}</span>\r\n',
    b'                            ${drawLabel ? `<span style="font-size:0.6rem;color:#2563eb;font-weight:600;line-height:1.3;">'
    b'\xf0\x9f\x95\x90 ${drawLabel}</span>` : \'\'}\r\n',
    b'                        </div>\r\n',
    b'                        <span class="receipt-lottery-amount flex-shrink-0">Bs ${groupTotal.toFixed(2)}</span>\r\n',
    b'                        ${isPreview ? deleteBtn : \'\'}\r\n',
    b'                    </div>`;\r\n',
    b'\r\n',
    b'                // N\xc3\xbameros del grupo: en azul, separados por coma\r\n',
    b"                const nums = bets.map(b => b.number).join(', ');\r\n",
    b'                const perBet = bets[0] ? bets[0].amount : 0;\r\n',
    b'                itemsHtml += `\r\n',
    b'                    <div class="receipt-bet-numbers">${nums} (\xc3\x97 Bs ${perBet.toFixed(2)} &nbsp; ${bets.length} apuesta${bets.length > 1 ? \'s\' : \'\'})</div>`;\r\n',
    b'            });\r\n',
]

# Replace lines start_idx..end_idx (inclusive)
new_lines = lines[:start_idx] + REPLACE + lines[end_idx+1:]
print(f'Replaced {end_idx - start_idx + 1} old lines with {len(REPLACE)} new lines')

with open(path, 'wb') as f:
    f.writelines(new_lines)
print('Saved. Total lines:', len(new_lines))
