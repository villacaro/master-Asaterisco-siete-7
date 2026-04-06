# -*- coding: utf-8 -*-
"""Inserta el widget HTML de Candidatos en el home - versión final con detección automática de EOL."""

FILE = (
    r"c:\Users\villa\OneDrive\Documentos\sistema Parley"
    r"\proyecto master Asterisco Siete (7)"
    r"\admin_AsteriscoSiete-server\admin_AsteriscoSiete7"
    r"\static\dashboard\index.html"
)

with open(FILE, 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8')

# Detect line ending
if '\r\n' in content:
    NL = '\r\n'
    print("Detected Windows line endings (CRLF)")
else:
    NL = '\n'
    print("Detected Unix line endings (LF)")

# Check if widget already injected in HTML (not just in JS string)
# We look for the div with id home-cand-kpis that appears BEFORE the JS section
js_anchor = '_loadHomeCandidatos'
cand_div  = 'id="home-cand-kpis"'

js_idx  = content.find(js_anchor)
div_idx = content.find(cand_div)

print(f"home-cand-kpis first occurrence: index {div_idx}")
print(f"_loadHomeCandidatos function at: index {js_idx}")

if div_idx != -1 and div_idx < js_idx - 100:
    print("✅ Widget HTML already in place (appears before JS function). No action needed.")
else:
    print("Inserting widget HTML into the home template...")

    # Build the search pattern dynamically using detected NL
    # The ending of the home function looks like:
    #  `.join('')}\n        </div>\n      </div>\n    </div>\n  `;\n}
    # We'll find it by looking for the prodsActivos block end more robustly

    # Strategy: find "prodsActivos.map" in the file, then find the NEXT occurrence
    # of `    </div>\n  `;\n}` after it

    pi = content.find("prodsActivos.map(p=>`")
    if pi == -1:
        pi = content.find("prodsActivos.map(p=>")
    print(f"prodsActivos.map at index: {pi}")

    # Find the closing triple after this
    search_from = pi + 100
    # Look for pattern: [NL]    </div>[NL]  `;[NL]}
    dash_bot_close = NL + "    </div>" + NL + "  `;" + NL + "}"

    close_idx = content.find(dash_bot_close, search_from)
    print(f"Closing pattern at: {close_idx}")

    if close_idx == -1:
        # Try alternate: maybe there's extra space or different indent
        for pattern in [
            NL + "    </div>" + NL + "  `;" + NL + "}",
            NL + "    </div>" + NL + "  `;" + NL + "}" + NL,
            "    </div>" + NL + "  `;" + NL + "}",
        ]:
            idx = content.find(pattern, search_from)
            if idx != -1:
                close_idx = idx
                dash_bot_close = pattern
                print(f"Found alternate pattern at {idx}: {repr(pattern[:40])}")
                break

    if close_idx == -1:
        print("❌ Could not find insertion point.")
        # Print context around prodsActivos end
        chunk = content[pi:pi+800]
        # Find </div> sequence
        ei = chunk.rfind("</div>")
        print("End of prodsActivos block:")
        print(repr(chunk[ei-20:ei+200]))
    else:
        print(f"✅ Found closing pattern at index {close_idx}")
        print("Context:", repr(content[close_idx-30:close_idx+80]))

        WIDGET = (NL +
            NL +
            "    <!-- ── CANDIDATOS WIDGET ─────────────────────────────────────────── -->" + NL +
            '    <div class="kpi" style="padding:0;overflow:hidden;margin-top:14px">' + NL +
            '      <div style="padding:16px 20px 12px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">' + NL +
            '        <div style="display:flex;align-items:center;gap:8px">' + NL +
            '          <span style="font-size:18px">🎯</span>' + NL +
            '          <div>' + NL +
            '            <div style="font-size:14px;font-weight:700">Selección de Candidatos</div>' + NL +
            '            <div style="font-size:10px;color:var(--muted)">Análisis de riesgo · tiempo real taquilla → Supabase</div>' + NL +
            '          </div>' + NL +
            '        </div>' + NL +
            '        <button onclick="renderCandidatos()" style="background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;border-radius:8px;padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer">' + NL +
            '          🔎 Ver completo' + NL +
            '        </button>' + NL +
            '      </div>' + NL +
            '      <div id="home-cand-kpis" style="display:flex;flex-wrap:wrap;gap:10px;padding:14px 20px;border-bottom:1px solid var(--border)">' + NL +
            '        <div style="font-size:12px;color:var(--muted);font-style:italic">Cargando análisis...</div>' + NL +
            '      </div>' + NL +
            '      <div id="home-cand-body">' + NL +
            '        <div style="width:32px;height:32px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite;margin:28px auto"></div>' + NL +
            '      </div>' + NL +
            '    </div>'
        )

        # Build the replacement
        # Original: [NL]    </div>[NL]  `;[NL]}
        # New:      [NL]    </div>[WIDGET][NL]  `;[NL]  _loadHomeCandidatos();[NL]}
        NEW_CLOSE = NL + "    </div>" + WIDGET + NL + "  `;" + NL + "  _loadHomeCandidatos();" + NL + "}"

        new_content = content[:close_idx] + NEW_CLOSE + content[close_idx + len(dash_bot_close):]

        with open(FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("✅ Widget HTML + _loadHomeCandidatos() call inserted!")
        print(f"File size: {len(new_content):,} chars")

        # Verify
        with open(FILE, 'r', encoding='utf-8') as f:
            verify = f.read()
        home_kpis_count = verify.count('home-cand-kpis')
        print(f"'home-cand-kpis' occurrences in file: {home_kpis_count}")
        js_pos  = verify.find('_loadHomeCandidatos')
        div_pos = verify.find('home-cand-kpis')
        print(f"Widget div at: {div_pos}, JS function at: {js_pos}")
        if div_pos < js_pos:
            print("✅ Correct order: HTML widget appears before JS function")
        else:
            print("⚠️  Widget div only appears inside JS (not in HTML template)")
