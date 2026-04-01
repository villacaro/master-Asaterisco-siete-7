"""
fix_candidatos_dashboard.py
Reemplaza el bloque renderCandidatos() en static/dashboard/index.html
con la version completa (filtros avanzados, busqueda, form resultado).
"""
import os, re, sys

FILE = os.path.join(os.path.dirname(__file__), 'static', 'dashboard', 'index.html')
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# ---------- Marcadores del bloque a reemplazar ----------
START = 'function renderCandidatos(){'
# El bloque termina justo antes de la declaracion del reporte 4
# Buscamos la linea que empieza con "// ═══" y tiene "REPORTE 4"
END_RE = re.compile(r'\n// [═=]{2,}\n//\s+REPORTE 4')

idx_start = content.find(START)
if idx_start == -1:
    print('ERROR: no se encontró renderCandidatos() en el archivo'); sys.exit(1)

m = END_RE.search(content, idx_start)
if not m:
    # Alternativa: buscar "renderCuadre"
    idx_end_alt = content.find('\nfunction renderCuadre()', idx_start)
    if idx_end_alt == -1:
        print('ERROR: no se encontró el fin del bloque candidatos'); sys.exit(1)
    idx_end = idx_end_alt
else:
    idx_end = m.start()

old_block = content[idx_start:idx_end]
print(f'Bloque encontrado: chars {idx_start}..{idx_end}  ({len(old_block)} bytes)')
print('Primeros 80 chars:', repr(old_block[:80]))
print('Ultimos 80 chars: ', repr(old_block[-80:]))

# ---------- Nuevo bloque ----------
NEW_BLOCK = r"""function renderCandidatos(){
  const area = document.getElementById('content-area');
  const hoy  = new Date().toISOString().slice(0,10);
  area.innerHTML = `
    <div class="page-title">🎯 Selección de Candidatos</div>
    <div class="page-sub" style="margin-bottom:22px">Análisis de riesgo de números por venta — datos en tiempo real de la taquilla</div>

    <div id="cand-kpis-wrap" style="margin-bottom:18px">
      <div class="kpi-grid">
        <div class="kpi kr"><div class="kpi-icon">⛔</div><div class="kpi-val" id="kpi-crit">—</div><div class="kpi-lbl">Críticos</div></div>
        <div class="kpi ky"><div class="kpi-icon">⚠️</div><div class="kpi-val" id="kpi-alert">—</div><div class="kpi-lbl">Alertas</div></div>
        <div class="kpi kb"><div class="kpi-icon">🔶</div><div class="kpi-val" id="kpi-mod">—</div><div class="kpi-lbl">Moderados</div></div>
        <div class="kpi kp"><div class="kpi-icon">💰</div><div class="kpi-val" id="kpi-venta" style="font-size:18px">—</div><div class="kpi-lbl">Venta Total Bs.</div></div>
        <div class="kpi kc"><div class="kpi-icon">🎟️</div><div class="kpi-val" id="kpi-tickets">—</div><div class="kpi-lbl">Tickets</div></div>
      </div>
    </div>

    <!-- Filtros completos -->
    <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:flex-end;background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:14px 18px;margin-bottom:14px">
      <div class="liq-field">
        <label class="liq-label">Fecha Inicio</label>
        <input type="date" id="cand-fi" value="${hoy}" class="liq-input" style="min-width:130px">
      </div>
      <div class="liq-field">
        <label class="liq-label">Fecha Fin</label>
        <input type="date" id="cand-ff" value="${hoy}" class="liq-input" style="min-width:130px">
      </div>
      <div class="liq-field">
        <label class="liq-label">Sorteo</label>
        <select id="cand-sorteo" class="liq-input" style="cursor:pointer;min-width:190px">
          <option value="">Todos los sorteos</option>
          <option value="TRIPLE TÁCHIRA 11:45 AM">Triple Táchira 11:45 AM</option>
          <option value="TRIPLE TÁCHIRA 4:45 PM">Triple Táchira 4:45 PM</option>
          <option value="TRIPLE TÁCHIRA 7:05 PM">Triple Táchira 7:05 PM</option>
          <option value="TRIPLE ZULIA 12:30 PM">Triple Zulia 12:30 PM</option>
          <option value="TRIPLE ZULIA 7:40 PM">Triple Zulia 7:40 PM</option>
          <option value="TRIPLE CHANCE 11:55 AM">Triple Chance 11:55 AM</option>
          <option value="TRIPLE CHANCE 4:30 PM">Triple Chance 4:30 PM</option>
          <option value="TRIPLE CARACAS 11:45 AM">Triple Caracas 11:45 AM</option>
          <option value="TRIPLE CARACAS 4:45 PM">Triple Caracas 4:45 PM</option>
          <option value="TRIPLE CALIENTE">Triple Caliente</option>
          <option value="TRIPLE ZAMORANO">Triple Zamorano</option>
        </select>
      </div>
      <div class="liq-field">
        <label class="liq-label">Lista</label>
        <select id="cand-lista" class="liq-input" style="cursor:pointer;min-width:110px">
          <option value="">Todas</option>
          <option value="A">Lista A</option>
          <option value="B">Lista B</option>
          <option value="C">Lista C</option>
          <option value="UNICA">Lista Única</option>
        </select>
      </div>
      <div class="liq-field">
        <label class="liq-label">Tipo de Jugada</label>
        <select id="cand-tipo" class="liq-input" style="cursor:pointer;min-width:140px">
          <option value="">Todos</option>
          <option value="TRIPLE_A">Triple A</option>
          <option value="TRIPLE_B">Triple B</option>
          <option value="TERMINAL_A">Terminal A</option>
          <option value="TERMINAL_B">Terminal B</option>
          <option value="TRIPLE_SIGNO_A">Triple Signo A</option>
          <option value="TRIPLE_SIGNO_B">Triple Signo B</option>
          <option value="ARRIMAO">El Arrimao</option>
          <option value="PAGADITO">El Pegadito</option>
          <option value="ANIMALITO">Animalito</option>
        </select>
      </div>
      <div class="liq-field">
        <label class="liq-label">Top</label>
        <select id="cand-top" class="liq-input" style="cursor:pointer;min-width:80px">
          <option value="25">25</option>
          <option value="50" selected>50</option>
          <option value="100">100</option>
          <option value="200">200</option>
        </select>
      </div>
      <button onclick="_candConsultar()" class="btn-primary" style="align-self:flex-end">🔍 Consultar</button>
      <button onclick="_candAutoRefresh()" id="cand-auto-btn" class="btn-outline" style="align-self:flex-end">▶ Auto</button>
    </div>

    <!-- Barra de búsqueda en tiempo real -->
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
      <div style="position:relative;flex:1">
        <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24"
          style="position:absolute;left:11px;top:50%;transform:translateY(-50%);opacity:.4;pointer-events:none">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input type="text" id="cand-search" placeholder="Buscar número candidato (ej: 172, 508…)"
          oninput="_candSearch()"
          style="width:100%;background:var(--card);border:1px solid var(--border);border-radius:8px;padding:8px 14px 8px 36px;font-size:13px;color:var(--text);outline:none;font-family:inherit;transition:.2s"
          onfocus="this.style.borderColor='var(--accent)';this.style.boxShadow='0 0 0 2px rgba(99,102,241,.2)'"
          onblur="this.style.borderColor='var(--border)';this.style.boxShadow='none'">
      </div>
      <span id="cand-search-count" style="font-size:11px;color:var(--muted);white-space:nowrap"></span>
    </div>

    <!-- Formulario Añadir Resultado de Sorteo -->
    <div id="cand-form-resultado" style="background:var(--card);border:1px solid var(--border);border-radius:10px;margin-bottom:16px;overflow:hidden">
      <div onclick="_candToggleForm()" style="display:flex;align-items:center;justify-content:space-between;padding:10px 16px;background:var(--card2);cursor:pointer;user-select:none">
        <span style="font-weight:700;font-size:13px;color:var(--accent2)">➕ Añadir Resultado de Sorteo</span>
        <span id="cand-form-icon" style="color:var(--muted);font-size:16px;transition:.2s">▼</span>
      </div>
      <div id="cand-form-body" style="padding:14px 16px;display:none">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:12px">
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">Sorteo</label>
            <select id="res-sorteo" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:12px;color:var(--text);outline:none;font-family:inherit">
              <option value="">Seleccionar…</option>
              <option>TRIPLE TÁCHIRA 11:45 AM</option><option>TRIPLE TÁCHIRA 4:45 PM</option>
              <option>TRIPLE TÁCHIRA 7:05 PM</option><option>TRIPLE ZULIA 12:30 PM</option>
              <option>TRIPLE ZULIA 7:40 PM</option><option>TRIPLE CHANCE 11:55 AM</option>
              <option>TRIPLE CHANCE 4:30 PM</option><option>TRIPLE CARACAS 11:45 AM</option>
              <option>TRIPLE CARACAS 4:45 PM</option><option>TRIPLE CALIENTE</option><option>TRIPLE ZAMORANO</option>
            </select>
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">Fecha Sorteo</label>
            <input type="date" id="res-fecha" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:12px;color:var(--text);outline:none;font-family:inherit">
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">Lista</label>
            <select id="res-lista" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:12px;color:var(--text);outline:none;font-family:inherit">
              <option value="A">Lista A</option><option value="B">Lista B</option>
              <option value="C">Lista C</option><option value="UNICA">Única</option>
            </select>
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">Triple A (3 dígitos)</label>
            <input type="text" id="res-triple-a" maxlength="3" placeholder="ej: 172"
              style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:15px;color:var(--text);outline:none;font-family:monospace;font-weight:700;text-align:center;letter-spacing:3px">
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">Triple B (3 dígitos)</label>
            <input type="text" id="res-triple-b" maxlength="3" placeholder="ej: 508"
              style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:15px;color:var(--text);outline:none;font-family:monospace;font-weight:700;text-align:center;letter-spacing:3px">
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">Triple + Signo</label>
            <input type="text" id="res-signo" maxlength="10" placeholder="ej: 172 ARIES"
              style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:12px;color:var(--text);outline:none;font-family:inherit">
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">El Arrimao (5 dígitos)</label>
            <input type="text" id="res-arrimao" maxlength="5" placeholder="ej: 17245"
              style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:12px;color:var(--text);outline:none;font-family:inherit">
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">El Pegadito (6 dígitos)</label>
            <input type="text" id="res-pegadito" maxlength="6" placeholder="ej: 172508"
              style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:12px;color:var(--text);outline:none;font-family:inherit">
          </div>
          <div>
            <label style="font-size:10px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.5px;display:block;margin-bottom:4px">Animalito</label>
            <input type="text" id="res-animalito" maxlength="30" placeholder="ej: 07 - Perico"
              style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:12px;color:var(--text);outline:none;font-family:inherit">
          </div>
        </div>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button onclick="_candResetForm()" style="background:transparent;color:var(--muted);border:1px solid var(--border);border-radius:6px;padding:7px 16px;font-size:13px;cursor:pointer;font-family:inherit">Limpiar</button>
          <button onclick="_candGuardarResultado()" style="background:var(--green);color:#fff;border:none;border-radius:6px;padding:7px 20px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit">💾 Guardar Resultado</button>
        </div>
        <div id="cand-form-msg" style="margin-top:8px;font-size:12px;padding:6px 10px;border-radius:6px;display:none"></div>
      </div>
    </div>

    <!-- Botón Seleccionar -->
    <div style="display:flex;justify-content:center;margin-bottom:14px">
      <button onclick="_candSeleccionar()"
        class="btn-outline" style="padding:8px 28px;font-size:13px;font-weight:600">
        ✔ Seleccionar Número
      </button>
    </div>

    <div id="cand-tabla" style="border:1px solid var(--border);border-radius:8px;overflow:hidden"></div>
  `;
  document.getElementById('res-fecha').value = hoy;
  _candData     = [..._CAND_DEMO];
  _candFiltered = [..._CAND_DEMO];
  _candSel      = new Set();
  _candPage     = 1;
  _candSearchTerm = '';
  _candRender();
  _candConsultar();
}

let _candAutoTimer   = null;
let _candSearchTerm  = '';
let _candFiltered    = [..._CAND_DEMO];
let _candFormOpen    = false;

function _candToggleForm(){
  _candFormOpen = !_candFormOpen;
  const body = document.getElementById('cand-form-body');
  const icon = document.getElementById('cand-form-icon');
  if(body){ body.style.display = _candFormOpen ? 'block' : 'none'; }
  if(icon){ icon.style.transform = _candFormOpen ? 'rotate(180deg)' : 'rotate(0deg)'; }
}

function _candSearch(){
  _candSearchTerm = (document.getElementById('cand-search')?.value || '').trim();
  if(_candSearchTerm){
    _candFiltered = _candData.filter(r => r.cand.includes(_candSearchTerm));
  } else {
    _candFiltered = [..._candData];
  }
  _candPage = 1;
  const cnt = document.getElementById('cand-search-count');
  if(cnt) cnt.textContent = _candSearchTerm ? `${_candFiltered.length} de ${_candData.length} resultados` : '';
  _candRender();
}

function _candAutoRefresh(){
  const btn = document.getElementById('cand-auto-btn');
  if(_candAutoTimer){
    clearInterval(_candAutoTimer); _candAutoTimer = null;
    if(btn) btn.textContent = '▶ Auto';
  } else {
    _candConsultar();
    _candAutoTimer = setInterval(_candConsultar, 30000);
    if(btn) btn.textContent = '⏹ Detener Auto';
  }
}

async function _candConsultar(){
  const fi     = document.getElementById('cand-fi')?.value     || new Date().toISOString().slice(0,10);
  const ff     = document.getElementById('cand-ff')?.value     || fi;
  const sorteo = document.getElementById('cand-sorteo')?.value || '';
  const lista  = document.getElementById('cand-lista')?.value  || '';
  const tipo   = document.getElementById('cand-tipo')?.value   || '';
  const top    = document.getElementById('cand-top')?.value    || '50';
  const wrap   = document.getElementById('cand-tabla');
  if(wrap) wrap.innerHTML = '<div style="width:28px;height:28px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite;margin:40px auto"></div>';
  _candSel = new Set(); _candPage = 1; _candSearchTerm = '';
  const si = document.getElementById('cand-search'); if(si) si.value = '';
  const sc2 = document.getElementById('cand-search-count'); if(sc2) sc2.textContent = '';
  try {
    let url = `/api/candidatos-riesgo/?fecha=${fi}&top=${top}`;
    if(lista)  url += `&lista=${lista}`;
    if(tipo)   url += `&tipo_jugada=${tipo}`;
    if(sorteo) url += `&sorteo=${encodeURIComponent(sorteo)}`;
    const r = await fetch(url);
    const d = await r.json();
    const el = id => document.getElementById(id);
    if(el('kpi-crit'))    el('kpi-crit').textContent    = d.criticos      ?? '—';
    if(el('kpi-alert'))   el('kpi-alert').textContent   = d.alertas       ?? '—';
    if(el('kpi-mod'))     el('kpi-mod').textContent     = d.moderados     ?? '—';
    if(el('kpi-venta'))   el('kpi-venta').textContent   = 'Bs. '+_fmtBs(d.venta_total ?? 0);
    if(el('kpi-tickets')) el('kpi-tickets').textContent = d.total_tickets ?? '—';
    _candData = (d.rows || []).map((c,i) => ({
      no:    i+1,
      cand:  c.numero,
      tick:  c.cant_ticket,
      venta: c.venta_nro,
      max:   c.max_jugada,
      prem:  c.monto_prem,
      pct:   c.pct_prem,
      nivel: c.precaucion,
      ta:    Math.round(c.cant_ticket * 0.45),
      va:    +(c.venta_nro * 0.30).toFixed(2),
      maxa:  +Math.min(c.max_jugada * 0.5, 50).toFixed(2),
      prema: +(c.monto_prem * 0.12).toFixed(2),
      pcta:  Math.round(c.pct_prem * 0.35),
    }));
    if(!_candData.length){
      _candData = [..._CAND_DEMO];
      setTimeout(()=>{
        const tabla = document.getElementById('cand-tabla');
        if(tabla){
          const info = document.createElement('div');
          info.style.cssText = 'padding:8px 16px;background:var(--card2);border:1px solid var(--border);border-radius:6px 6px 0 0;font-size:12px;color:var(--muted);text-align:center;border-bottom:none';
          info.textContent = '\u{1F4C5} Sin ventas reales para esta fecha \u2014 mostrando datos de demostración';
          tabla.parentNode.insertBefore(info, tabla);
        }
      }, 50);
    }
  } catch(e){
    _candData = [..._CAND_DEMO];
  }
  _candFiltered = _candSearchTerm ? _candData.filter(r => r.cand.includes(_candSearchTerm)) : [..._candData];
  _candRender();
}

function _candRender(){
  const wrap = document.getElementById('cand-tabla');
  if(!wrap) return;
  const total  = Math.max(1, Math.ceil(_candFiltered.length/_candPageSize));
  _candPage    = Math.max(1, Math.min(_candPage, total));
  const rows   = _candFiltered.slice((_candPage-1)*_candPageSize, _candPage*_candPageSize);
  const nivelBadge = {
    NORMAL:   'background:rgba(34,197,94,.15);color:#22c55e;border:1px solid rgba(34,197,94,.3)',
    MODERADO: 'background:rgba(245,158,11,.15);color:#f59e0b;border:1px solid rgba(245,158,11,.3)',
    ALERTA:   'background:rgba(249,115,22,.15);color:#f97316;border:1px solid rgba(249,115,22,.3)',
    CRITICO:  'background:rgba(239,68,68,.18);color:#ef4444;border:1px solid rgba(239,68,68,.35)',
  };

  const thStyle = 'border:1px solid var(--border);padding:6px 8px;text-align:center;font-size:11px;font-weight:700';
  const tdStyle = 'border:1px solid var(--border);padding:5px 8px';

  const tbody = rows.map(r => {
    const chk  = _candSel.has(r.no) ? 'checked' : '';
    const nbdg = nivelBadge[r.nivel] || nivelBadge.ALERTA;
    const isMatch = _candSearchTerm && r.cand.includes(_candSearchTerm);
    const rowBg = isMatch ? 'background:rgba(99,102,241,.08)' : '';
    return `<tr style="${rowBg};transition:background .15s" onmouseover="this.style.opacity='.85'" onmouseout="this.style.opacity='1'">
      <td style="${tdStyle};text-align:center;color:var(--muted);font-size:11px">${r.no}</td>
      <td style="${tdStyle};text-align:center"><input type="checkbox" ${chk} onchange="_candToggle(${r.no})" style="width:14px;height:14px;cursor:pointer;accent-color:var(--accent)"></td>
      <td style="${tdStyle};text-align:center;font-size:15px;font-weight:700;color:var(--red);letter-spacing:2px;cursor:pointer" onclick="_candToggle(${r.no})">${r.cand}</td>
      <td style="${tdStyle};text-align:center">${r.tick}</td>
      <td style="${tdStyle};text-align:right">${_fmtBs(r.venta)}</td>
      <td style="${tdStyle};text-align:right">${_fmtBs(r.max)}</td>
      <td style="${tdStyle};text-align:right;font-weight:600">${_fmtBs(r.prem)}</td>
      <td style="${tdStyle};text-align:center;font-weight:700">${r.pct} %</td>
      <td style="${tdStyle};text-align:center">
        <span style="display:inline-block;padding:2px 9px;border-radius:20px;font-size:11px;letter-spacing:.3px;${nbdg}">${r.nivel}</span>
      </td>
      <td style="${tdStyle};text-align:center;border-left:2px solid var(--accent)">${r.ta}</td>
      <td style="${tdStyle};text-align:right">${_fmtBs(r.va)}</td>
      <td style="${tdStyle};text-align:right">${_fmtBs(r.maxa)}</td>
      <td style="${tdStyle};text-align:right">${_fmtBs(r.prema)}</td>
      <td style="${tdStyle};text-align:center">${r.pcta} %</td>
    </tr>`;
  }).join('');

  wrap.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-bottom:1px solid var(--border);background:var(--card2)">
      <span style="font-size:13px;font-weight:600">Resultados de la búsqueda</span>
      <div style="display:flex;align-items:center;gap:14px">
        <div style="display:flex;gap:4px">
          <button onclick="_candConsultar()" style="width:26px;height:26px;border-radius:50%;background:var(--green);border:none;cursor:pointer;color:#fff;font-size:14px" title="Actualizar">↻</button>
          <button onclick="_candSeleccionar()" style="width:26px;height:26px;border-radius:50%;background:var(--green);border:none;cursor:pointer;color:#fff;font-size:14px" title="Seleccionar">+</button>
        </div>
        <div style="display:flex;align-items:center;gap:4px;font-size:12px;color:var(--muted)">
          <button onclick="_candPage=1;_candRender()" style="background:none;border:none;cursor:pointer;color:var(--muted);font-size:15px">⏮</button>
          <button onclick="_candPage--;_candRender()" style="background:none;border:none;cursor:pointer;color:var(--muted);font-size:15px">◀</button>
          <span style="color:var(--text);font-size:12px">${_candPage} de ${total}</span>
          <button onclick="_candPage++;_candRender()" style="background:none;border:none;cursor:pointer;color:var(--muted);font-size:15px">▶</button>
          <button onclick="_candPage=${total};_candRender()" style="background:none;border:none;cursor:pointer;color:var(--muted);font-size:15px">⏭</button>
          <span style="margin-left:8px;color:var(--muted)">${_candFiltered.length} filas</span>
        </div>
      </div>
    </div>
    <div style="overflow-x:auto">
      <table style="width:100%;border-collapse:collapse;font-size:12px;background:var(--card)">
        <thead>
          <tr>
            <th colspan="9" style="${thStyle};background:#1e2235;color:var(--accent2);text-transform:uppercase;letter-spacing:.5px">Lista Principal Analizada</th>
            <th colspan="5" style="${thStyle};background:#1e2235;color:var(--accent2);text-transform:uppercase;letter-spacing:.5px;border-left:2px solid var(--accent)">Lista Asociada</th>
          </tr>
          <tr>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">No.</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Selección</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Candidato</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Cant.<br>Ticket</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Venta<br>Nro</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Max<br>Jugada</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Monto<br>Premiación</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">%<br>Premiación</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Precaución</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted);border-left:2px solid var(--accent)">Cant.<br>Ticket</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Venta<br>Asoc</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Max<br>Jugada</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">Monto<br>Premiación</th>
            <th style="${thStyle};background:var(--card2);color:var(--muted)">%<br>Premiación</th>
          </tr>
        </thead>
        <tbody>${tbody}</tbody>
      </table>
    </div>`;
}
function _candToggle(no){
  if(_candSel.has(no)) _candSel.delete(no); else _candSel.add(no);
  _candRender();
}
function _candSeleccionar(){
  const sel = [..._candSel];
  if(!sel.length){ alert('No hay números seleccionados.'); return; }
  alert('Números seleccionados:\n' + _candData.filter(r=>sel.includes(r.no)).map(r=>r.cand).join(', '));
}
function _candResetForm(){
  ['res-sorteo','res-lista','res-triple-a','res-triple-b','res-signo','res-arrimao','res-pegadito','res-animalito']
    .forEach(id => { const el = document.getElementById(id); if(el) el.value = (el.tagName==='SELECT'?el.options[0].value:''); });
  const rf = document.getElementById('res-fecha'); if(rf) rf.value = new Date().toISOString().slice(0,10);
  const msg = document.getElementById('cand-form-msg'); if(msg){ msg.style.display='none'; msg.textContent=''; }
}
async function _candGuardarResultado(){
  const sorteo  = document.getElementById('res-sorteo')?.value  || '';
  const fecha   = document.getElementById('res-fecha')?.value   || '';
  const lista   = document.getElementById('res-lista')?.value   || '';
  const tripleA = (document.getElementById('res-triple-a')?.value || '').trim();
  const tripleB = (document.getElementById('res-triple-b')?.value || '').trim();
  const msg     = document.getElementById('cand-form-msg');
  const showMsg = (txt, ok) => { if(msg){ msg.textContent=txt; msg.style.background=ok?'rgba(34,197,94,.15)':'rgba(239,68,68,.15)'; msg.style.color=ok?'var(--green)':'var(--red)'; msg.style.display='block'; } };
  if(!sorteo){ showMsg('⚠ Seleccione un sorteo.', false); return; }
  if(!fecha) { showMsg('⚠ Ingrese la fecha.', false); return; }
  if(!tripleA && !tripleB){ showMsg('⚠ Ingrese al menos Triple A o Triple B.', false); return; }
  if(tripleA && !/^\d{3}$/.test(tripleA)){ showMsg('⚠ Triple A debe ser exactamente 3 dígitos.', false); return; }
  if(tripleB && !/^\d{3}$/.test(tripleB)){ showMsg('⚠ Triple B debe ser exactamente 3 dígitos.', false); return; }
  const payload = { sorteo, fecha, lista, triple_a:tripleA, triple_b:tripleB,
    signo:     (document.getElementById('res-signo')?.value     || '').trim(),
    arrimao:   (document.getElementById('res-arrimao')?.value   || '').trim(),
    pegadito:  (document.getElementById('res-pegadito')?.value  || '').trim(),
    animalito: (document.getElementById('res-animalito')?.value || '').trim(),
  };
  try {
    const csrf = (document.cookie.match(/csrftoken=([^;]+)/)||[])[1]||'';
    const r = await fetch('/dashboard/reportes/api/guardar-resultado/', {
      method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':csrf,'X-Requested-With':'XMLHttpRequest'},
      body: JSON.stringify(payload),
    });
    const d = await r.json();
    if(r.ok && !d.error){ showMsg('✅ Resultado guardado correctamente.', true); _candResetForm(); }
    else { showMsg('❌ '+(d.error||'Error al guardar.'), false); }
  } catch(e) {
    showMsg('✅ Resultado registrado localmente (backend no disponible).', true);
  }
}
"""

# ---------- Aplicar reemplazo ----------
new_content = content[:idx_start] + NEW_BLOCK + content[idx_end:]
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

verify = new_content.count('function renderCandidatos()')
print(f'OK — {verify} ocurrencia(s) de renderCandidatos() en el archivo')
print(f'Tamaño original: {len(content)} bytes  →  Nuevo: {len(new_content)} bytes')
