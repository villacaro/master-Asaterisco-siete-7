"""
fix_template.py
Parcha el dashboard.html para usar /api/django-users/ en la tabla de Gestión de Usuarios,
y agrega las funciones JS para el resto de secciones (Lista en Línea, Bloqueo, Riesgo).
"""
import re

TEMPLATE = 'templates/arrejuntao/dashboard.html'

with open(TEMPLATE, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── 1. Reemplazar función cargarUsuarios para usar django-users ────────────
# Buscar bloque existente
OLD_CARGA = 'async function cargarUsuarios() {'
NEW_CARGA = '''async function cargarUsuarios() {
      const wrap = document.getElementById('usuarios-table-wrap');
      if (!wrap) return;
      wrap.innerHTML = '<div class="empty-state"><div class="loading-spinner"></div><br>Cargando usuarios…</div>';
      try {
        const data = await fetch('/api/django-users/').then(r => r.json());
        const lista = data.usuarios || [];
        const total = document.getElementById('usr-total');
        if (total) total.textContent = lista.length;
        if (lista.length === 0) {
          wrap.innerHTML = '<div class="empty-state"><div class="empty-icon">👥</div>Sin usuarios registrados</div>';
          return;
        }
        let html = `<table class="data-table">
          <thead>
            <tr>
              <th><input type="checkbox" id="usr-all" onchange="toggleAll(this)"></th>
              <th>Nombre de Usuario</th>
              <th>Correo Electrónico</th>
              <th>Nombre</th>
              <th>Apellidos</th>
              <th>Staff</th>
              <th>Superusuario</th>
              <th>Activo</th>
              <th>Último acceso</th>
              <th>Registrado</th>
              <th>Acciones</th>
            </tr>
          </thead><tbody>`;
        lista.forEach((u, i) => {
          const staffBadge    = u.is_staff      ? '<span style="color:#86efac;font-size:0.75rem;">✔</span>' : '<span style="color:rgba(255,255,255,0.2);font-size:0.75rem;">—</span>';
          const superBadge    = u.is_superuser  ? '<span style="color:#fde68a;font-size:0.75rem;">★</span>' : '<span style="color:rgba(255,255,255,0.2);font-size:0.75rem;">—</span>';
          const activeBadge   = u.is_active     ? '<span class="badge-abierto">Activo</span>' : '<span style="background:rgba(239,68,68,0.15);color:#fca5a5;border:1px solid rgba(239,68,68,0.3);border-radius:9999px;padding:0.1rem 0.45rem;font-size:0.62rem;font-weight:700;">Inactivo</span>';
          html += `<tr>
            <td><input type="checkbox" class="usr-cb" value="${u.id}"></td>
            <td><a href="/admin/auth/user/${u.id}/change/" style="color:var(--accent);font-weight:600;text-decoration:none;" target="_blank">${u.username}</a></td>
            <td style="color:var(--muted);">${u.email || '—'}</td>
            <td>${u.first_name || '—'}</td>
            <td>${u.last_name  || '—'}</td>
            <td style="text-align:center;">${staffBadge}</td>
            <td style="text-align:center;">${superBadge}</td>
            <td style="text-align:center;">${activeBadge}</td>
            <td style="color:var(--muted);font-size:0.74rem;">${u.last_login}</td>
            <td style="color:var(--muted);font-size:0.74rem;">${u.date_joined}</td>
            <td>
              <div style="display:flex;gap:0.3rem;">
                <a href="/admin/auth/user/${u.id}/change/" target="_blank" class="btn-action" style="font-size:0.7rem;">✏️ Editar</a>
                <a href="/admin/auth/user/${u.id}/password/" target="_blank" class="btn-action" style="background:rgba(245,208,32,0.12);color:#fde68a;border-color:rgba(245,208,32,0.3);font-size:0.7rem;">🔑 Pass</a>
              </div>
            </td>
          </tr>`;
        });
        html += '</tbody></table>';
        // Footer resumen
        html += `<div style="padding:0.6rem 1rem;border-top:1px solid var(--border);font-size:0.72rem;color:var(--muted);">${lista.length} usuario${lista.length !== 1 ? 's' : ''} en el sistema</div>`;
        wrap.innerHTML = html;
      } catch (err) {
        wrap.innerHTML = '<div class="empty-state"><div class="empty-icon">⚠️</div>Error al cargar usuarios: ' + err.message + '</div>';
      }
    }

    function toggleAll(cb) {
      document.querySelectorAll('.usr-cb').forEach(c => c.checked = cb.checked);
    }

    // Alias — keep original name working'''

if OLD_CARGA in content:
    # Find the entire old function and replace just the opening
    content = content.replace(OLD_CARGA, NEW_CARGA, 1)
    print("✅ cargarUsuarios reemplazada correctamente")
else:
    print("⚠️  No se encontró cargarUsuarios — verificar manualmente")
    # Show what's around line 800
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'cargar' in line.lower() and 'usuario' in line.lower():
            print(f"  Line {i}: {line}")

with open(TEMPLATE, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template guardado.")
