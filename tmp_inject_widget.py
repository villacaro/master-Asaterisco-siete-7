# -*- coding: utf-8 -*-
"""
Inserta el widget de Selección de Candidatos en el home del dashboard.
Se ejecuta una sola vez y luego puede eliminarse.
"""

HTML_FILE = (
    r"c:\Users\villa\OneDrive\Documentos\sistema Parley"
    r"\proyecto master Asterisco Siete (7)"
    r"\admin_AsteriscoSiete-server\admin_AsteriscoSiete7"
    r"\static\dashboard\index.html"
)

GUARD = "home-cand-kpis"   # Evita doble inserción

WIDGET_HTML = """
    <!-- ── CANDIDATOS WIDGET ──────────────────────────────── -->
    <div class="kpi" style="padding:0;overflow:hidden;margin-top:14px">
      <div style="padding:16px 20px 12px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:18px">&#127919;</span>
          <div>
            <div style="font-size:14px;font-weight:700">Selecci&#243;n de Candidatos</div>
            <div style="font-size:10px;color:var(--muted)">An&#225;lisis de riesgo &#183; tiempo real taquilla</div>
          </div>
        </div>
        <button onclick="renderCandidatos()" style="background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;border-radius:8px;padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer">
          &#128269; Ver completo
        </button>
      </div>
      <div id="home-cand-kpis" style="display:flex;flex-wrap:wrap;gap:10px;padding:14px 20px;border-bottom:1px solid var(--border)">
        <div style="font-size:12px;color:var(--muted);font-style:italic">Cargando an&#225;lisis...</div>
      </div>
      <div id="home-cand-body">
        <div style="width:32px;height:32px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite;margin:28px auto"></div>
      </div>
    </div>
"""

JS_FUNCTION = """
// ─── CANDIDATOS HOME LOADER ───────────────────────────────────────────────────
async function _loadHomeCandidatos(){
  const kpisEl = document.getElementById('home-cand-kpis');
  const bodyEl = document.getElementById('home-cand-body');
  if(!kpisEl || !bodyEl) return;
  try{
    const hoy = new Date().toISOString().slice(0,10);
    const r   = await fetch(`/api/candidatos-riesgo/?fecha=${hoy}&top=20`);
    const d   = await r.json();
    if(!d.ok) throw new Error(d.error || 'Sin datos');

    const rows      = d.rows || [];
    const criticos  = d.criticos  || 0;
    const alertas   = d.alertas   || 0;
    const moderate  = d.moderados || 0;
    const ventaTotal= d.venta_total || 0;
    const tickets   = d.total_tickets || 0;

    kpisEl.innerHTML = `
      <div style="display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;background:var(--card2);border:1px solid var(--border)">
        <span style="font-size:18px">&#9940;</span>
        <div><div style="font-size:22px;font-weight:800;color:var(--red);line-height:1">${criticos}</div><div style="font-size:9px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)">Cr&#237;ticos</div></div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;background:var(--card2);border:1px solid var(--border)">
        <span style="font-size:18px">&#9888;&#65039;</span>
        <div><div style="font-size:22px;font-weight:800;color:var(--orange);line-height:1">${alertas}</div><div style="font-size:9px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)">Alertas</div></div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;background:var(--card2);border:1px solid var(--border)">
        <span style="font-size:18px">&#128310;</span>
        <div><div style="font-size:22px;font-weight:800;color:#f5c518;line-height:1">${moderate}</div><div style="font-size:9px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)">Moderados</div></div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;background:var(--card2);border:1px solid var(--border)">
        <span style="font-size:18px">&#128176;</span>
        <div><div style="font-size:18px;font-weight:800;color:var(--green);line-height:1">Bs. ${_fmtBs(ventaTotal)}</div><div style="font-size:9px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)">Venta total</div></div>
      </div>
      <div style="display:flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;background:var(--card2);border:1px solid var(--border)">
        <span style="font-size:18px">&#127915;</span>
        <div><div style="font-size:22px;font-weight:800;color:var(--accent2);line-height:1">${tickets}</div><div style="font-size:9px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted)">Tickets</div></div>
      </div>
    `;

    if(!rows.length){
      bodyEl.innerHTML = `<div style="text-align:center;padding:36px;color:var(--muted)">
        <div style="font-size:40px;margin-bottom:10px">&#128203;</div>
        <div style="font-size:13px">Sin apuestas para hoy</div>
        <div style="font-size:11px;margin-top:4px">No hay boletos registrados en la taquilla para los filtros seleccionados.</div>
      </div>`;
      return;
    }

    const maxPrem = Math.max(...rows.map(c=>parseFloat(c.monto_prem)||0)) || 1;
    bodyEl.innerHTML = `
      <div class="table-wrap" style="max-height:320px;overflow-y:auto;overflow-x:auto">
        <table class="data-table" style="font-size:12px">
          <thead><tr>
            <th style="width:36px">No.</th>
            <th>N&#250;mero</th>
            <th style="text-align:center">Tickets</th>
            <th style="text-align:right">Venta Bs.</th>
            <th style="text-align:right">Max Jugada</th>
            <th style="text-align:right">Premiaci&#243;n</th>
            <th style="text-align:center">%</th>
            <th style="text-align:center">Nivel</th>
          </tr></thead>
          <tbody>
            ${rows.map((c,i)=>{
              const nivel = c.precaucion||'OK';
              const nivelHtml =
                nivel==='CR\\u00cdTICO'  ? '<span style="color:var(--red);font-weight:700">&#128308; CR&#205;TICO</span>' :
                nivel==='ALERTA'        ? '<span style="color:var(--orange);font-weight:700">&#129000; ALERTA</span>'   :
                nivel==='MODERADO'      ? '<span style="color:#f5c518;font-weight:600">&#128993; MODERADO</span>'       :
                                          '<span style="color:var(--green)">&#128994; NORMAL</span>';
              const clrNum =
                nivel==='CR\\u00cdTICO'  ? 'color:var(--red);font-weight:800;font-size:15px'  :
                nivel==='ALERTA'        ? 'color:var(--orange);font-weight:700'               :
                nivel==='MODERADO'      ? 'color:#f5c518;font-weight:600'                     : '';
              const prem = parseFloat(c.monto_prem)||0;
              const pct  = c.pct_prem || 0;
              return `<tr>
                <td style="color:var(--muted);font-size:11px">${i+1}</td>
                <td style="font-weight:800;font-size:15px;${clrNum}">${escHtml(String(c.numero||'?'))}</td>
                <td style="text-align:center;font-weight:600">${c.cant_ticket||0}</td>
                <td style="text-align:right">Bs. ${_fmtBs(c.venta_nro)}</td>
                <td style="text-align:right;color:var(--muted)">${_fmtBs(c.max_jugada)}</td>
                <td style="text-align:right;font-weight:700;color:${pct>=35?'var(--red)':pct>=20?'var(--orange)':'var(--text)'}">${_fmtBs(prem)}</td>
                <td style="text-align:center;font-size:11px;color:var(--muted)">${pct} %</td>
                <td style="text-align:center">${nivelHtml}</td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
      <div style="padding:10px 20px;border-top:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
        <span style="font-size:11px;color:var(--muted)">Top ${rows.length} candidatos &middot; ${new Date().toLocaleTimeString('es-VE')}</span>
        <button onclick="renderCandidatos()" style="background:var(--accent-bg);color:var(--accent);border:1px solid var(--accent);border-radius:7px;padding:5px 14px;font-size:11px;font-weight:600;cursor:pointer">
          Ver an&#225;lisis completo &#8594;
        </button>
      </div>
    `;
  }catch(e){
    if(kpisEl) kpisEl.innerHTML = '<div style="font-size:11px;color:var(--muted);font-style:italic">Sin datos de candidatos para hoy</div>';
    if(bodyEl) bodyEl.innerHTML = `<div style="text-align:center;padding:24px;color:var(--muted);font-size:12px">No hay datos de riesgo disponibles</div>`;
  }
}
"""

JS_CALL = "_loadHomeCandidatos();"

# ── Anchor tokens in the file ────────────────────────────────────────────────
# We look for the closing of the dash-bot-row (line ~1923) followed by
# the template literal close (`; on the next non-empty line)
# Then we inject the widget between those two lines.

TEMPLATE_CLOSE = "  `;"      # the closing of area.innerHTML = `...`;

# We also need to call _loadHomeCandidatos() right after the close,
# before the function's closing brace.

FUNC_ANCHOR = "// ════════════════════════════════════════════════\n//   CRUD INLINE FORM"

# ─── Read file ───────────────────────────────────────────────────────────────
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if GUARD in content:
    print("⚠️  Widget already present — skipping HTML injection.")
else:
    # Find the last occurrence of TEMPLATE_CLOSE (the home function's template end)
    # There may be several `; in the file — we want the one at ~line 1924
    # Strategy: find the line index of TEMPLATE_CLOSE that's preceded by "    </div>"
    lines = content.split('\n')
    insert_idx = None
    for i, line in enumerate(lines):
        if line.rstrip('\r') == '  `':
            # Check previous non-empty line is "    </div>"
            for j in range(i-1, max(i-5, 0), -1):
                prev = lines[j].rstrip('\r')
                if prev:
                    if prev == '    </div>':
                        insert_idx = i
                    break
            if insert_idx:
                break

    if insert_idx is None:
        # Fallback: insert before the first `; after the prodsActivos section
        for i, line in enumerate(lines):
            if 'prodsActivos' in line and i > 1900:
                # Find the `; after this block
                for j in range(i, min(i+30, len(lines))):
                    if lines[j].rstrip('\r').strip() == '`':
                        insert_idx = j
                        break
                if insert_idx:
                    break

    if insert_idx is None:
        print("❌ Could not find insertion point. Dumping lines 1918-1930:")
        for i in range(1917, 1930):
            print(f"  {i+1}: {repr(lines[i])}")
    else:
        print(f"✅ Inserting widget before line {insert_idx+1}: {repr(lines[insert_idx][:50])}")
        lines.insert(insert_idx, WIDGET_HTML)
        content = '\n'.join(lines)

        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Widget HTML inserted.")

# ─── Insert JS function + call ───────────────────────────────────────────────
with open(HTML_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

if '_loadHomeCandidatos' in content:
    print("⚠️  JS function already present — skipping JS injection.")
else:
    # Insert the function before the CRUD section
    if FUNC_ANCHOR in content:
        content = content.replace(FUNC_ANCHOR, JS_FUNCTION + '\n\n' + FUNC_ANCHOR, 1)
        print("✅ JS function inserted before CRUD section.")
    else:
        # Fallback: append before </script>
        content = content.replace('</script>', JS_FUNCTION + '\n</script>', 1)
        print("✅ JS function inserted before </script>.")

    # Also add the call in the home render function, right after area.innerHTML = ...;
    # The pattern is: `;\n} (closing of renderDashStats-like function)
    # We already handled this by calling it from the widget loader side,
    # but we also need to call it when the home renders.
    # Find the widget HTML we just inserted and add the call after the template close
    call_anchor = GUARD  # the widget is already in content
    if JS_CALL not in content:
        # Add call after the template literal close that follows our widget
        # Pattern: after "home-cand-body" div, find the `; and add call after the }
        old_pattern = "  `;\n}"
        new_pattern = "  `;\n  // Auto-load candidatos widget\n  " + JS_CALL + "\n}"
        if old_pattern in content:
            # Replace only the first occurrence after our widget
            idx = content.find(GUARD)
            part_before = content[:idx]
            part_after  = content[idx:]
            part_after = part_after.replace(old_pattern, new_pattern, 1)
            content = part_before + part_after
            print("✅ JS call inserted after template close.")

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ JS saved.")

print("\n─── Done ───")
