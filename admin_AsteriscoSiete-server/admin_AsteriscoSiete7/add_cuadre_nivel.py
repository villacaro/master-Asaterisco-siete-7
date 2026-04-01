"""
add_cuadre_nivel_superior.py
Agrega el reporte "Cuadre con Nivel Superior" al Dashboard:
  1. Botón en sidebar
  2. función renderCuadreNivelSuperior() con datos demo y API
"""

with open('static/dashboard/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1. SIDEBAR: agregar botón después de "⚖️ Liq. Sorteos" ─────────────────
OLD_SIDEBAR = '      <button class="nav-sub-item" style="color:var(--accent2);font-weight:600" onclick="renderLiquidacionesSorteo()">⚖️ Liq. Sorteos</button>\n    </div>'
NEW_SIDEBAR = (
    '      <button class="nav-sub-item" style="color:var(--accent2);font-weight:600" onclick="renderLiquidacionesSorteo()">⚖️ Liq. Sorteos</button>\n'
    '      <button class="nav-sub-item" style="color:var(--accent2);font-weight:600" onclick="renderCuadreNivelSuperior()">🏛️ Cuadre Nivel Superior</button>\n'
    '    </div>'
)
if OLD_SIDEBAR in content:
    content = content.replace(OLD_SIDEBAR, NEW_SIDEBAR)
    print('✅ Sidebar: botón agregado')
else:
    print('⚠️  Sidebar: botón NO agregado — buscar manualmente')

# ─── 2. JAVASCRIPT: función renderCuadreNivelSuperior ───────────────────────
# Insertar justo antes del cierre </script> final (antes de </body>)
JS_FUNC = r'''
// ════════════════════════════════════════════════════════════════
//   MÓDULO CUADRE CON NIVEL SUPERIOR
// ════════════════════════════════════════════════════════════════
const _CNS_DEMO = [
  { fecha:'01/04/2024', dia:'Lunes',     sa:1805436.99, venta:151493.14, premios:101160.00, pct:31901.60, regalia:0, saldo:0, operador:18431.54, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'02/04/2024', dia:'Martes',    sa:1823868.53, venta:62837.63,  premios:158537.83, pct:82110.80, regalia:33931.22, saldo:0, operador:42489.81, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'03/04/2024', dia:'Miércoles', sa:1806358.34, venta:152494.72, premios:108475.00, pct:32513.99, regalia:0, saldo:0, operador:11505.73, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'04/04/2024', dia:'Jueves',    sa:1866358.34, venta:164089.69, premios:76545.00,  pct:35424.90, regalia:0, saldo:0, operador:52099.79, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'05/04/2024', dia:'Viernes',   sa:1929983.85, venta:116429.60, premios:59865.00,  pct:25471.32, regalia:0, saldo:0, operador:31093.28, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'06/04/2024', dia:'Sábado',    sa:1961057.12, venta:27501.70,  premios:30320.00,  pct:6180.63,  regalia:0, saldo:0, operador:-8998.93, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'07/04/2024', dia:'Domingo',   sa:1952058.20, venta:141919.39, premios:82842.50,  pct:30695.32, regalia:0, saldo:0, operador:28381.57, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'08/04/2024', dia:'Lunes',     sa:1980439.77, venta:138124.20, premios:72350.00,  pct:29501.12, regalia:0, saldo:0, operador:36273.08, dep:0, pagos:0, ajuste:0, cargos:0 },
  { fecha:'09/04/2024', dia:'Martes',    sa:2016712.85, venta:0,         premios:0,         pct:0,        regalia:0, saldo:0, operador:0,         dep:0, pagos:0, ajuste:0, cargos:0 },
];

function _cnsCalcSaldoActual(row){
  // SA_actual = SA_anterior + Venta - Premios - Regalia + Operador + Dep - Pagos + Ajuste - Cargos
  return row.sa + row.venta - row.premios - row.regalia + row.operador + row.dep - row.pagos + row.ajuste - row.cargos;
}

function renderCuadreNivelSuperior(){
  currentModule = 'cuadre-nivel'; currentTitle = 'Cuadre con Nivel Superior';
  if(_monitorTimer){ clearInterval(_monitorTimer); _monitorTimer=null; }

  const area = document.getElementById('content-area');
  const now  = new Date();
  const mesActual = now.toISOString().slice(0,7); // YYYY-MM

  area.innerHTML = `
    <div class="page-title">🏛️ Cuadre con Nivel Superior</div>
    <div class="page-sub" style="margin-bottom:16px">Resumen diario de saldos, ventas, premios y movimientos financieros</div>

    <!-- Filtros -->
    <div style="display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;
                background:var(--card);border:1px solid var(--border);
                border-radius:var(--r);padding:14px 18px;margin-bottom:16px">
      <div style="display:flex;flex-direction:column;gap:4px">
        <label style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.5px">Banca / Agencia</label>
        <select id="cns-banca"
                style="background:var(--surface);color:var(--text);border:1px solid var(--border);
                       border-radius:6px;padding:7px 12px;font-size:13px;min-width:160px;cursor:pointer">
          <option value="">Todas</option>
          <option value="1">CARACAS</option>
          <option value="2">MIRANDA</option>
          <option value="3">MARACAIBO</option>
        </select>
      </div>
      <div style="display:flex;flex-direction:column;gap:4px">
        <label style="font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.5px">Mes del Resumen</label>
        <input type="month" id="cns-mes" value="${mesActual}"
               style="background:var(--surface);color:var(--text);border:1px solid var(--border);
                      border-radius:6px;padding:7px 12px;font-size:13px;min-width:160px">
      </div>
      <button onclick="_cnsConsultar()"
              style="background:linear-gradient(135deg,var(--accent),var(--accent2));
                     color:#fff;border:none;border-radius:8px;padding:8px 22px;
                     font-size:13px;font-weight:600;cursor:pointer;align-self:flex-end">
        🔍 Consultar
      </button>
      <button onclick="_cnsExportar()"
              style="background:var(--green);color:#fff;border:none;border-radius:8px;
                     padding:8px 16px;font-size:13px;font-weight:600;cursor:pointer;align-self:flex-end"
              title="Exportar a Excel">
        📊 Excel
      </button>
    </div>

    <!-- Info banca seleccionada -->
    <div id="cns-header-info" style="text-align:center;margin-bottom:14px;font-size:14px;font-weight:700;color:var(--accent2)">
      — Seleccione una banca y haga clic en Consultar —
    </div>

    <!-- Tabla -->
    <div id="cns-tabla" style="border:1px solid var(--border);border-radius:8px;overflow:hidden;overflow-x:auto"></div>
  `;

  // Mostrar datos demo de inmediato
  _cnsData = [..._CNS_DEMO];
  _cnsRender('DEMO (datos de muestra)');
}

let _cnsData = [];

async function _cnsConsultar(){
  const banca = document.getElementById('cns-banca')?.value || '';
  const mes   = document.getElementById('cns-mes')?.value   || '';
  const wrap  = document.getElementById('cns-tabla');
  if(wrap) wrap.innerHTML = '<div style="text-align:center;padding:40px;color:var(--muted)"><div style="width:28px;height:28px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .7s linear infinite;margin:0 auto 12px"></div>Cargando...</div>';

  try {
    const r = await fetch(`/api/cuadre-nivel-superior/?banca=${banca}&mes=${mes}`);
    const d = await r.json();
    if(d.ok && d.rows && d.rows.length){
      _cnsData = d.rows;
      _cnsRender(d.banca_nombre || 'Todos');
    } else {
      _cnsData = [..._CNS_DEMO];
      _cnsRender('DEMO (sin datos para el período)');
    }
  } catch(e){
    _cnsData = [..._CNS_DEMO];
    _cnsRender('DEMO (error de conexión)');
  }
}

function _cnsRender(bancaNombre){
  const wrap = document.getElementById('cns-tabla');
  const info = document.getElementById('cns-header-info');
  const mes  = document.getElementById('cns-mes')?.value || '';
  if(!wrap) return;

  // Actualizar header
  if(info){
    const meses = ['','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
    const [y,m] = mes ? mes.split('-') : ['',''];
    const mesNombre = m ? `${meses[parseInt(m)]} ${y}` : '—';
    info.innerHTML = `<span style="color:var(--muted);font-weight:400">Banca:</span> <span style="color:var(--accent2)">${bancaNombre}</span>&nbsp;&nbsp;&nbsp;<span style="color:var(--muted);font-weight:400">Mes del Resumen:</span> <span style="color:var(--text)">${mesNombre}</span>`;
  }

  const th = (txt, extra='') =>
    `<th style="border:1px solid var(--border);padding:7px 6px;background:#1e2235;
                color:var(--accent2);font-size:10px;font-weight:700;text-align:center;
                white-space:nowrap;${extra}">${txt}</th>`;

  const fBs = v => {
    if(v===null||v===undefined) return '0';
    const n = parseFloat(v);
    if(isNaN(n)) return '0';
    const color = n < 0 ? 'color:var(--red)' : (n > 0 ? '' : 'color:var(--muted)');
    const fmt = Math.abs(n).toLocaleString('es-VE',{minimumFractionDigits:2,maximumFractionDigits:2});
    return `<span style="${color}">${n<0?'-':''}${fmt}</span>`;
  };

  // Calcular saldo actual para cada fila y acumulados
  let totVenta=0, totPremios=0, totPct=0, totReg=0, totOp=0, totDep=0, totPag=0, totAjuste=0, totCargos=0;
  const rows = _cnsData.map((r,i) => {
    const sa2 = _cnsCalcSaldoActual(r);
    totVenta   += r.venta;   totPremios += r.premios; totPct  += r.pct;
    totReg     += r.regalia; totOp      += r.operador; totDep += r.dep;
    totPag     += r.pagos;   totAjuste  += r.ajuste;  totCargos += r.cargos;
    return `<tr style="${i%2===0?'':'background:rgba(255,255,255,.03)'}">
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:center;color:var(--muted);font-size:11px">${i+1}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:center;font-size:12px;white-space:nowrap">${r.fecha}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:center;font-size:12px">${r.dia}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px">${fBs(r.sa)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px;font-weight:600">${fBs(r.venta)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px;color:var(--red)">${fBs(r.premios)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px;color:var(--red)">${fBs(r.pct)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px">${fBs(r.regalia)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px">${fBs(r.saldo)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px;color:${r.operador<0?'var(--red)':'var(--green)'}">${fBs(r.operador)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px">${fBs(r.dep)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px;color:var(--accent)">${fBs(r.pagos)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px;color:var(--accent)">${fBs(r.ajuste)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px">${fBs(r.cargos)}</td>
      <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-size:12px;font-weight:700;color:var(--accent2)">${fBs(sa2)}</td>
    </tr>`;
  }).join('');

  // Fila "Viene mes anterior"
  const saldoInicial = _cnsData.length ? _cnsData[0].sa : 0;
  const saldoFinal   = _cnsData.length ? _cnsCalcSaldoActual(_cnsData[_cnsData.length-1]) : 0;

  wrap.innerHTML = `
    <table id="cns-table-data" style="width:100%;border-collapse:collapse;font-size:12px;background:var(--surface);min-width:1100px">
      <thead>
        <tr>
          ${th('Nro.')}${th('Fecha')}${th('Día de la<br>Semana')}
          ${th('Saldo<br>Anterior')}${th('Venta','color:var(--green)')}
          ${th('Premios','color:var(--red)')}${th('% Banca','color:var(--red)')}
          ${th('Regalía')}${th('Saldo')}${th('Operador')}
          ${th('Depósitos')}${th('Pagos','color:var(--accent)')}
          ${th('Ajuste','color:var(--accent)')}${th('Cargos')}
          ${th('Saldo<br>Actual','color:var(--accent2);font-size:11px;font-weight:800')}
        </tr>
      </thead>
      <tbody>
        <!-- Fila cabecera: Viene mes anterior -->
        <tr style="background:rgba(255,255,255,.06)">
          <td colspan="14" style="border:1px solid var(--border);padding:5px 12px;font-size:11px;font-style:italic;color:var(--muted);text-align:right">Viene mes anterior</td>
          <td style="border:1px solid var(--border);padding:5px 8px;text-align:right;font-weight:700;color:var(--accent2)">${fBs(saldoInicial)}</td>
        </tr>
        ${rows}
        <!-- Fila de totales -->
        <tr style="background:rgba(255,255,255,.08);border-top:2px solid var(--border)">
          <td colspan="3" style="border:1px solid var(--border);padding:6px 12px;font-weight:700;font-size:12px;text-align:right">TOTALES</td>
          <td style="border:1px solid var(--border);padding:6px 8px"></td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700">${fBs(totVenta)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700;color:var(--red)">${fBs(totPremios)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700;color:var(--red)">${fBs(totPct)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700">${fBs(totReg)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px"></td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700">${fBs(totOp)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700">${fBs(totDep)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700;color:var(--accent)">${fBs(totPag)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700;color:var(--accent)">${fBs(totAjuste)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700">${fBs(totCargos)}</td>
          <td style="border:1px solid var(--border);padding:6px 8px;text-align:right;font-weight:700;color:var(--accent2)">${fBs(saldoFinal)}</td>
        </tr>
      </tbody>
    </table>`;
}

function _cnsExportar(){
  const tbl = document.getElementById('cns-table-data');
  if(!tbl){ alert('Sin datos para exportar'); return; }
  let csv = 'Nro.,Fecha,Dia,Saldo Anterior,Venta,Premios,% Banca,Regalia,Saldo,Operador,Depositos,Pagos,Ajuste,Cargos,Saldo Actual\n';
  _cnsData.forEach((r,i)=>{
    const sa2 = _cnsCalcSaldoActual(r);
    csv += `${i+1},${r.fecha},${r.dia},${r.sa},${r.venta},${r.premios},${r.pct},${r.regalia},${r.saldo},${r.operador},${r.dep},${r.pagos},${r.ajuste},${r.cargos},${sa2}\n`;
  });
  const blob = new Blob(['\uFEFF'+csv], {type:'text/csv;charset=utf-8'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `cuadre-nivel-superior-${new Date().toISOString().slice(0,10)}.csv`;
  a.click();
}

'''

# Insertar antes del cierre </script> terminal
SCRIPT_END = '</script>\n</body>'
if SCRIPT_END in content:
    content = content.replace(SCRIPT_END, JS_FUNC + '\n' + SCRIPT_END)
    print('✅ JavaScript: función renderCuadreNivelSuperior() agregada')
else:
    # Intentar variante sin newline
    SCRIPT_END2 = '</script>\n\n</body>'
    if SCRIPT_END2 in content:
        content = content.replace(SCRIPT_END2, JS_FUNC + '\n' + SCRIPT_END2)
        print('✅ JavaScript: función agregada (variante 2)')
    else:
        # Buscar posición del último </script>
        idx = content.rfind('</script>')
        if idx > 0:
            content = content[:idx] + JS_FUNC + '\n' + content[idx:]
            print('✅ JavaScript: función insertada antes del último </script>')
        else:
            print('❌ NO SE ENCONTRÓ </script> — agregar manualmente')

with open('static/dashboard/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Archivo guardado. Tamaño: {len(content):,} bytes')
print(f'Ocurrencias de renderCuadreNivelSuperior: {content.count("renderCuadreNivelSuperior")}')
