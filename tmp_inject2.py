# -*- coding: utf-8 -*-
"""Inserta el widget HTML de Candidatos en el home del dashboard."""

FILE = (
    r"c:\Users\villa\OneDrive\Documentos\sistema Parley"
    r"\proyecto master Asterisco Siete (7)"
    r"\admin_AsteriscoSiete-server\admin_AsteriscoSiete7"
    r"\static\dashboard\index.html"
)

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── Find the exact closing sequence of the home function ─────────────────────
# The home function ends with:
#   [closing </div> of dash-bot-row]
#   [closing `; of area.innerHTML template]
#   [} closing the JS function]
# We look for the prodsActivos block end followed by the template close

SEARCH = "`.join('')}\n        </div>\n      </div>\n    </div>\n  `;\n}"

print("Searching for pattern...")
idx = content.find(SEARCH)

if idx == -1:
    # Try with \r\n
    SEARCH_CRLF = "`.join('')}\r\n        </div>\r\n      </div>\r\n    </div>\r\n  `;\r\n}"
    idx = content.find(SEARCH_CRLF)
    if idx != -1:
        SEARCH = SEARCH_CRLF
        print("Found with CRLF line endings")

if idx == -1:
    # Find "prodsActivos" and get nearby area
    pi = content.find("prodsActivos.map(p=>")
    print(f"prodsActivos.map found at: {pi}")
    chunk = content[pi:pi+600]
    print("Chunk after prodsActivos.map:")
    print(repr(chunk))
else:
    print(f"Found at index {idx}")
    print("Context:", repr(content[idx-50:idx+60]))

    WIDGET_HTML = """

    <!-- ── CANDIDATOS WIDGET ─────────────────────────────────────────── -->
    <div class="kpi" style="padding:0;overflow:hidden;margin-top:14px">
      <div style="padding:16px 20px 12px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:18px">🎯</span>
          <div>
            <div style="font-size:14px;font-weight:700">Selección de Candidatos</div>
            <div style="font-size:10px;color:var(--muted)">Análisis de riesgo · tiempo real taquilla → Supabase</div>
          </div>
        </div>
        <button onclick="renderCandidatos()" style="background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;border-radius:8px;padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer">
          🔎 Ver completo
        </button>
      </div>
      <div id="home-cand-kpis" style="display:flex;flex-wrap:wrap;gap:10px;padding:14px 20px;border-bottom:1px solid var(--border)">
        <div style="font-size:12px;color:var(--muted);font-style:italic">Cargando análisis...</div>
      </div>
      <div id="home-cand-body">
        <div style="width:32px;height:32px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite;margin:28px auto"></div>
      </div>
    </div>"""

    REPLACEMENT = SEARCH.replace(
        "    </div>\n  `;\n}",
        "    </div>\n" + WIDGET_HTML + "\n  `;\n  _loadHomeCandidatos();\n}"
    )

    new_content = content[:idx] + REPLACEMENT + content[idx + len(SEARCH):]

    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ Widget HTML + JS call inserted successfully!")
    print(f"File size: {len(new_content)} chars")
