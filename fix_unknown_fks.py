"""
Script que corrige todas las FKs 'UNKNOWN' en los modelos del proyecto.
Analiza el contexto (nombre del campo + nombre de la clase) para determinar
el modelo destino correcto.
"""
import pathlib
import re

base = pathlib.Path(r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7')

# Mapa de correcciones: (archivo_relativo, nombre_campo) -> modelo_destino
# Basado en el análisis de la arquitectura del sistema
CORRECTIONS = {
    # admin_status/models.py
    ('admin_status/models.py', 'status', 'StatusDetail'): 'Status',
    ('admin_status/models.py', 'user', 'StatusDetail'): 'admin_users.Users',
    ('admin_status/models.py', 'status', 'TaquillaStatusDetail'): 'Status',
    ('admin_status/models.py', 'usuariotaquilla', 'TaquillaStatusDetail'): 'admin_comercializacion.UsuariosTaquilla',

    # admin_comercializacion/models.py - campos status -> Status (admin_status)
    # admin_apuestas/models.py
    # admin_juego/models.py
    # admin_finanzas/models.py
    # admin_permisologia/models.py
    # admin_mail/models.py
    # admin_resultados/models.py
    # admin_themes/models.py
    # admin_users/models.py
}

def fix_unknown_in_file(filepath, corrections_for_file):
    """
    Fix UNKNOWN FKs in a single file using regex.
    Each correction is (field_name, class_name) -> target_model
    """
    content = filepath.read_text(encoding='utf-8', errors='replace')
    if "'UNKNOWN'" not in content:
        return False

    modified = False
    # Find all class blocks and fix FKs within each class
    # Pattern: field = models.ForeignKey('UNKNOWN', ...)
    
    for field_name, target in corrections_for_file.items():
        # Pattern to find ForeignKey with UNKNOWN for a specific field name
        pattern = rf"({re.escape(field_name)}\s*=\s*models\.ForeignKey\(\s*)'UNKNOWN'"
        replacement = rf"\g<1>'{target}'"
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            modified = True
            print(f"  Fixed {field_name} -> {target}")

    if modified:
        filepath.write_text(content, encoding='utf-8')
    return modified


# Process each model file
model_corrections = {
    'admin_status/models.py': {
        'status': 'Status',
        'user': 'admin_users.Users',
        'usuariotaquilla': 'admin_comercializacion.UsuariosTaquilla',
    },
    'admin_themes/models.py': {
        'status': 'admin_status.Status',
        'user': 'admin_users.Users',
        'operadora': 'admin_comercializacion.Operadoras',
        'banca': 'admin_comercializacion.Bancas',
        'bloque': 'admin_comercializacion.Bloques',
        'distribuidor': 'admin_comercializacion.Distribuidores',
        'agencia': 'admin_comercializacion.Agencias',
        'taquilla': 'admin_comercializacion.Taquillas',
    },
    'admin_mail/models.py': {
        'status': 'admin_status.Status',
        'operadora': 'admin_comercializacion.Operadoras',
        'banca': 'admin_comercializacion.Bancas',
        'bloque': 'admin_comercializacion.Bloques',
    },
    'admin_permisologia/models.py': {
        'status': 'admin_status.Status',
        'user': 'admin_users.Users',
        'operadora': 'admin_comercializacion.Operadoras',
        'banca': 'admin_comercializacion.Bancas',
        'bloque': 'admin_comercializacion.Bloques',
        'distribuidor': 'admin_comercializacion.Distribuidores',
        'agencia': 'admin_comercializacion.Agencias',
        'taquilla': 'admin_comercializacion.Taquillas',
        'deporte': 'admin_juego.Deportes',
    },
    'admin_users/models.py': {
        'status': 'admin_status.Status',
        'profile': 'admin_permisologia.Profile',
        'comercializadora': 'admin_comercializacion.Operadoras',
    },
    'admin_apuestas/models.py': {
        'status': 'admin_status.Status',
        'taquilla': 'admin_comercializacion.Taquillas',
        'usuariotaquilla': 'admin_comercializacion.UsuariosTaquilla',
        'juego': 'admin_juego.Juego',
        'deporte': 'admin_juego.Deportes',
        'encuentro': 'admin_juego.Encuentro',
        'resultado': 'admin_resultados.Resultados',
        'sistema_juego': 'admin_juego.SistemaJuego',
        'apuesta': 'admin_apuestas.Apuestas',
    },
    'admin_resultados/models.py': {
        'status': 'admin_status.Status',
        'juego': 'admin_juego.Juego',
        'deporte': 'admin_juego.Deportes',
        'encuentro': 'admin_juego.Encuentro',
        'sistema_juego': 'admin_juego.SistemaJuego',
        'temporada': 'admin_juego.Temporadas',
        'resultado': 'admin_resultados.Resultados',
    },
    'admin_finanzas/models.py': {
        'status': 'admin_status.Status',
        'operadora': 'admin_comercializacion.Operadoras',
        'banca': 'admin_comercializacion.Bancas',
        'bloque': 'admin_comercializacion.Bloques',
        'distribuidor': 'admin_comercializacion.Distribuidores',
        'agencia': 'admin_comercializacion.Agencias',
        'taquilla': 'admin_comercializacion.Taquillas',
        'sistema_juego': 'admin_juego.SistemaJuego',
        'juego': 'admin_juego.Juego',
        'comercializadora': 'admin_finanzas.Comercializadora',
        'temporada': 'admin_juego.Temporadas',
    },
    'admin_datamart/models.py': {
        'status': 'admin_status.Status',
        'operadora': 'admin_comercializacion.Operadoras',
        'banca': 'admin_comercializacion.Bancas',
        'bloque': 'admin_comercializacion.Bloques',
        'distribuidor': 'admin_comercializacion.Distribuidores',
        'agencia': 'admin_comercializacion.Agencias',
        'taquilla': 'admin_comercializacion.Taquillas',
        'sistema_juego': 'admin_juego.SistemaJuego',
        'juego': 'admin_juego.Juego',
        'comercializadora': 'admin_finanzas.Comercializadora',
        'temporada': 'admin_juego.Temporadas',
        'deporte': 'admin_juego.Deportes',
        'encuentro': 'admin_juego.Encuentro',
    },
    'admin_comercializacion/models.py': {
        'status': 'admin_status.Status',
        'user': 'admin_users.Users',
        'operadora': 'admin_comercializacion.Operadoras',
        'banca': 'admin_comercializacion.Bancas',
        'bloque': 'admin_comercializacion.Bloques',
        'distribuidor': 'admin_comercializacion.Distribuidores',
        'distribuidores': 'admin_comercializacion.Distribuidores',
        'agencia': 'admin_comercializacion.Agencias',
        'taquilla': 'admin_comercializacion.Taquillas',
        'sistema_juego': 'admin_juego.SistemaJuego',
        'deporte': 'admin_juego.Deportes',
        'juego': 'admin_juego.Juego',
        'estado': 'admin_profiles.Estados',
        'pais': 'admin_profiles.Paises',
        'direccion': 'admin_profiles.Direcciones',
        'comercializadora': 'admin_finanzas.Comercializadora',
        'temporada': 'admin_juego.Temporadas',
        'profile': 'admin_permisologia.Profile',
        'permissions': 'admin_permisologia.Permissions',
    },
    'admin_juego/models.py': {
        'status': 'admin_status.Status',
        'deporte': 'admin_juego.Deportes',
        'sistema_juego': 'admin_juego.SistemaJuego',
        'temporada': 'admin_juego.Temporadas',
        'encuentro': 'admin_juego.Encuentro',
        'juego': 'admin_juego.Juego',
        'operadora': 'admin_comercializacion.Operadoras',
        'banca': 'admin_comercializacion.Bancas',
        'bloque': 'admin_comercializacion.Bloques',
        'distribuidor': 'admin_comercializacion.Distribuidores',
        'agencia': 'admin_comercializacion.Agencias',
        'comercializadora': 'admin_finanzas.Comercializadora',
        'taquilla': 'admin_comercializacion.Taquillas',
        'resultado': 'admin_resultados.Resultados',
    },
    'admin_juego/models_arrejuntao.py': {
        'status': 'admin_status.Status',
        'sistema_juego': 'admin_juego.SistemaJuego',
        'temporada': 'admin_juego.Temporadas',
        'juego': 'admin_juego.Juego',
    },
}

total_fixed = 0
for rel_path, corrections in model_corrections.items():
    filepath = base / rel_path.replace('/', '\\')
    if not filepath.exists():
        print(f"NOT FOUND: {rel_path}")
        continue
    print(f"\nProcessing: {rel_path}")
    if fix_unknown_in_file(filepath, corrections):
        total_fixed += 1
    else:
        print("  (no changes needed)")

print(f"\n=== Fixed {total_fixed} files ===")

# Count remaining UNKNOWN
remaining = 0
for f in sorted(base.rglob('*.py')):
    if '__pycache__' in str(f) or 'migrations' in str(f): continue
    try:
        txt = f.read_text(encoding='utf-8', errors='replace')
        if "'UNKNOWN'" in txt:
            count = txt.count("'UNKNOWN'")
            remaining += count
            print(f"REMAINING {count}x: {f.relative_to(base)}")
    except:
        pass
print(f"Total UNKNOWN remaining in models: {remaining}")
