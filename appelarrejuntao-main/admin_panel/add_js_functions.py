"""
add_js_functions.py
Agrega funciones JS al final del <script> del dashboard (antes de </script>)
para: consultarListaLinea, agregarRiesgo, limpiarCR, aplicarBloqueo, renderBV, initDatos
"""
TEMPLATE = 'templates/arrejuntao/dashboard.html'

NEW_JS = """
    // ── LISTA EN LÍNEA ──────────────────────────────────────────────────────
    function consultarListaLinea() {
      const wrap = document.getElementById('ll-grid-wrap');
      if (!wrap) return;
      wrap.innerHTML = '<div class="empty-state"><div class="loading-spinner"></div><br>Generando grilla…</div>';
      const sorteoSel = document.getElementById('ll-sorteo')?.value || 'Todos';
      const modSel    = document.getElementById('ll-modalidad')?.value || 'Triple A';
      const hoy       = new Date().toLocaleDateString('es-VE', {day:'2-digit',month:'long',year:'numeric'});
      const fechaEl   = document.getElementById('ll-num-date');
      if (fechaEl) fechaEl.textContent = hoy;
      const lSorteo = document.getElementById('ll-sorteo-label');
      const lModal  = document.getElementById('ll-modal-label');
      if (lSorteo) lSorteo.textContent = sorteoSel || 'Todos';
      if (lModal)  lModal.textContent  = modSel;
      setTimeout(() => {
        const COLS = 10, PER = 100;
        let html = '<table class="num-grid-table" style="width:100%;"><thead><tr>';
        for (let c = 0; c < COLS; c++) {
          const last = c === COLS - 1;
          html += `<th class="ng-p">P</th><th class="ng-num">NUM</th><th class="${last ? 'ng-amt' : 'ng-amt g-sep'}">MONTO</th>`;
        }
        html += '</tr></thead><tbody>';
        for (let row = 0; row < PER; row++) {
          html += '<tr>';
          for (let col = 0; col < COLS; col++) {
            const num = col * PER + row;
            const ns  = String(num).padStart(3, '0');
            const last = col === COLS - 1;
            html += `<td class="ng-p">${row + 1}</td><td class="ng-num">${ns}</td><td class="ng-amt zero${last ? '' : ' g-sep'}">—</td>`;
          }
          html += '</tr>';
        }
        html += '</tbody></table>';
        wrap.innerHTML = html;
        const ca = document.getElementById('ll-con-apuesta');
        const mt = document.getElementById('ll-monto-total');
        if (ca) ca.textContent = '0';
        if (mt) mt.textContent = '0,00';
      }, 400);
    }

    // ── CONTROL DE RIESGO ───────────────────────────────────────────────────
    let crRiesgo = [];

    function agregarRiesgo() {
      const num    = document.getElementById('cr-num')?.value.trim();
      const monto  = parseFloat(document.getElementById('cr-monto')?.value) || 0;
      const riesgo = parseFloat(document.getElementById('cr-riesgo')?.value) || 0;
      const lista  = document.getElementById('cr-lista')?.value || 'Principal';
      if (!num) { alert('Ingresa un número (1-3 dígitos).'); return; }
      crRiesgo.push({ num, monto, riesgo, lista });
      renderCR();
      ['cr-num','cr-monto','cr-riesgo'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
      });
    }

    function renderCR() {
      const tbody = document.getElementById('cr-tbody');
      if (!tbody) return;
      if (crRiesgo.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:2rem;color:var(--muted);font-size:0.8rem;">Sin registros — agrega un número arriba</td></tr>';
        return;
      }
      tbody.innerHTML = crRiesgo.map((r, i) => `
        <tr>
          <td><input type="checkbox"></td>
          <td style="font-family:monospace;font-weight:700;color:var(--accent);">${String(r.num).padStart(3,'0')}</td>
          <td style="color:var(--amber);">${r.monto.toFixed(2)} Bs</td>
          <td style="color:#fca5a5;">${r.riesgo.toFixed(2)} Bs</td>
          <td>${r.riesgo > 0 && r.monto / r.riesgo > 0.8 ? '<span style="color:#fca5a5;font-size:0.72rem;">⚠️ Alto</span>' : '<span style="color:#86efac;font-size:0.72rem;">OK</span>'}</td>
          <td style="color:var(--muted);font-size:0.74rem;">${r.lista}</td>
          <td>
            <button class="btn-action btn-danger" style="font-size:0.7rem;" onclick="crRiesgo.splice(${i},1);renderCR();">🗑</button>
          </td>
        </tr>`).join('');
    }

    function limpiarCR() {
      crRiesgo = [];
      renderCR();
    }

    // ── BLOQUEO DE VENTAS ───────────────────────────────────────────────────
    let bvBloqueos = [];

    function aplicarBloqueo() {
      const modal  = document.getElementById('bv-modalidad')?.value || '';
      const sorteo = document.getElementById('bv-sorteo')?.value    || '';
      const tipo   = document.getElementById('bv-tipo')?.value       || '';
      const numero = document.getElementById('bv-numero')?.value.trim() || '';
      const motivo = document.getElementById('bv-motivo')?.value.trim() || '—';
      if (!numero) { alert('Ingresa el número a bloquear.'); return; }
      const fecha = new Date().toLocaleDateString('es-VE', {day:'2-digit',month:'2-digit',year:'numeric'});
      bvBloqueos.push({ modal, sorteo, tipo, numero, motivo, fecha, activo: true });
      renderBV();
      ['bv-numero','bv-motivo'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
      });
    }

    function renderBV() {
      const tbody = document.getElementById('bv-tbody');
      const count = document.getElementById('bv-count');
      if (!tbody) return;
      if (count) count.textContent = bvBloqueos.length + ' Bloqueo' + (bvBloqueos.length !== 1 ? 's' : '');
      if (bvBloqueos.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;padding:2rem;color:var(--muted);font-size:0.8rem;">Sin bloqueos activos</td></tr>';
        return;
      }
      tbody.innerHTML = bvBloqueos.map((b, i) => `
        <tr>
          <td style="font-weight:600;">${b.modal}</td>
          <td><span style="background:rgba(59,130,246,0.15);color:#93c5fd;border:1px solid rgba(59,130,246,0.3);border-radius:9999px;padding:0.1rem 0.4rem;font-size:0.65rem;">${b.tipo}</span></td>
          <td style="color:var(--muted);">${b.sorteo}</td>
          <td style="font-family:monospace;font-weight:700;color:var(--accent);">${b.numero}</td>
          <td style="color:var(--muted);font-size:0.74rem;">${b.motivo}</td>
          <td style="color:var(--muted);font-size:0.74rem;">${b.fecha}</td>
          <td>
            <div style="display:flex;gap:0.3rem;">
              <button class="${b.activo ? 'toggle-on' : 'toggle-off'}" onclick="bvBloqueos[${i}].activo=!bvBloqueos[${i}].activo;renderBV();">${b.activo ? 'On' : 'Off'}</button>
              <button class="btn-action" style="font-size:0.7rem;">✏️</button>
              <button class="btn-action btn-danger" style="font-size:0.7rem;" onclick="bvBloqueos.splice(${i},1);renderBV();">🗑</button>
            </div>
          </td>
        </tr>`).join('');
    }
"""

with open(TEMPLATE, 'r', encoding='utf-8') as f:
    content = f.read()

# Inject before closing </script>
MARKER = '    // Inicializar IP al cargar'
if MARKER in content:
    content = content.replace(MARKER, NEW_JS + '\n    // Inicializar IP al cargar', 1)
    print("✅ Funciones JS inyectadas antes de inicializar IP")
else:
    # Try another marker
    MARKER2 = '    detectarIP()'
    if MARKER2 in content:
        content = content.replace(MARKER2, NEW_JS + '\n    detectarIP()', 1)
        print("✅ Funciones JS inyectadas antes de detectarIP()")
    else:
        # Last resort: inject before </script>
        content = content.replace('</script>', NEW_JS + '\n  </script>', 1)
        print("✅ Funciones JS inyectadas antes de </script>")

with open(TEMPLATE, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template guardado OK.")
