"""
Corrección masiva y definitiva de todos los FK 'UNKNOWN' en los modelos del proyecto.
Usa el contexto (clase.campo) para determinar el modelo destino correcto.
"""
import pathlib
import re

base = pathlib.Path(r'C:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7')

# Mapa completo: (archivo, clase, campo) -> modelo destino
# 'self' significa autorreferencia al mismo modelo
CORRECTIONS = {
    # admin_finanzas/models.py
    ('admin_finanzas/models.py', 'Banco'): {
        'banco': 'admin_finanzas.Banco',  # autorreferencia
    },
    ('admin_finanzas/models.py', 'Movimiento'): {
        'banco': 'admin_finanzas.Banco',
        'tipo': 'admin_finanzas.TipoMovimiento',
    },
    ('admin_finanzas/models.py', 'ResumenAdministrativo'): {
        'dia': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
    },

    # admin_apuestas/models.py
    ('admin_apuestas/models.py', 'Tickets'): {
        'user': 'admin_comercializacion.UsuariosTaquilla',
        'ticket_type': 'admin_juego.Jugadas',
    },
    ('admin_apuestas/models.py', 'TicketsDetail'): {
        'jugada': 'admin_juego.Jugadas',
        'ticket': 'admin_apuestas.Tickets',
    },
    ('admin_apuestas/models.py', 'TicketStatus'): {
        'ticket': 'admin_apuestas.Tickets',
    },
    ('admin_apuestas/models.py', 'TicketsDetailStatus'): {
        'detalle_ticket': 'admin_apuestas.TicketsDetail',
    },

    # admin_comercializacion/models.py
    ('admin_comercializacion/models.py', 'DataDefault'): {
        'user_type': 'admin_permisologia.Profile',
    },
    ('admin_comercializacion/models.py', 'Porcentajes'): {
        'tipo': 'admin_comercializacion.TipoPorcentajes',
    },
    ('admin_comercializacion/models.py', 'DefaultPreferences'): {
        'group': 'admin_permisologia.Profile',
        'typepreference': 'admin_comercializacion.TypePreferences',
    },
    ('admin_comercializacion/models.py', 'Preferences'): {
        'typepreference': 'admin_comercializacion.TypePreferences',
        'comercializacion': 'admin_finanzas.Comercializadora',
    },

    # admin_permisologia/models.py
    ('admin_permisologia/models.py', 'Menu'): {
        'menu_suc': 'admin_permisologia.Menu',  # autorreferencia
    },
    ('admin_permisologia/models.py', 'PermissionsSales'): {
        'grupo': 'admin_juego.Grupo',
        'modalidad': 'admin_juego.Modalidades',
        'comercializadora': 'admin_finanzas.Comercializadora',
    },
    ('admin_permisologia/models.py', 'PermissionsSalesRestrictions'): {
        'comercializadora': 'admin_finanzas.Comercializadora',
    },

    # admin_resultados/models.py
    ('admin_resultados/models.py', 'Resultados'): {
        'sistema': 'admin_juego.SistemaJuego',
    },
    ('admin_resultados/models.py', 'ResultadosRestric'): {
        'grupo': 'admin_juego.Grupo',
        'modalidad': 'admin_juego.Modalidades',
    },
    ('admin_resultados/models.py', 'Anotaciones'): {
        'grupo': 'admin_juego.Grupo',
    },
    ('admin_resultados/models.py', 'AnotacionesDetail'): {
        'anotacion': 'admin_resultados.Anotaciones',
        'encuentro_detail': 'admin_juego.EncuentrosDetail',
        'condicion': 'admin_juego.Condiciones',
    },

    # admin_themes/models.py
    ('admin_themes/models.py', 'Color'): {
        'theme': 'admin_themes.Theme',
    },

    # admin_users/models.py
    ('admin_users/models.py', 'UserSession'): {
        'user_ref': 'admin_users.Users',
        'comercializadora_session': 'admin_finanzas.Comercializadora',
    },

    # admin_mail/models.py
    ('admin_mail/models.py', 'Message'): {
        'from_comercializadora': 'admin_finanzas.Comercializadora',
    },
    ('admin_mail/models.py', 'MessageSend'): {
        'message': 'admin_mail.Message',
    },
    ('admin_mail/models.py', 'MessageComer'): {
        'comercializadora': 'admin_finanzas.Comercializadora',
        'message': 'admin_mail.Message',
    },

    # admin_juego/models.py
    ('admin_juego/models.py', 'SistemaJuego'): {
        'theme': 'admin_themes.Theme',
        'company': 'admin_finanzas.Comercializadora',
    },
    ('admin_juego/models.py', 'Temporadas'): {
        'torneo': 'admin_juego.Torneo',
    },
    ('admin_juego/models.py', 'EquiposLigas'): {
        'liga': 'admin_juego.Liga',
        'equipo': 'admin_juego.Equipo',
    },
    ('admin_juego/models.py', 'Jugador'): {
        'tipo': 'admin_juego.TipoJugador',
    },
    ('admin_juego/models.py', 'EquiposTemporadas'): {
        'equipo': 'admin_juego.Equipo',
    },
    ('admin_juego/models.py', 'Jornadas'): {
        'temporadas': 'admin_juego.Temporadas',
    },
    ('admin_juego/models.py', 'Encuentro'): {
        'sistema': 'admin_juego.SistemaJuego',
    },
    ('admin_juego/models.py', 'EquiposGrupos'): {
        'equipo': 'admin_juego.Equipo',
        'grupo': 'admin_juego.Grupo',
    },
    ('admin_juego/models.py', 'Encuentros'): {
        'jornada': 'admin_juego.Jornadas',
        'grupo': 'admin_juego.Grupo',
    },
    ('admin_juego/models.py', 'EncuentrosDetail'): {
        'equipos_temporadas': 'admin_juego.EquiposTemporadas',
        'jugador': 'admin_juego.Jugador',
    },
    ('admin_juego/models.py', 'Deportes_Grupos'): {
        'grupo': 'admin_juego.Grupo',
    },
    ('admin_juego/models.py', 'Modalidades_Grupos'): {
        'modalidad': 'admin_juego.Modalidades',
        'grupo': 'admin_juego.Grupo',
    },
    ('admin_juego/models.py', 'EncuentrosModalidades'): {
        'deporte_grupo': 'admin_juego.Deportes_Grupos',
        'modalidad_grupo': 'admin_juego.Modalidades_Grupos',
        'sistema': 'admin_juego.SistemaJuego',
        'origen': 'admin_juego.Encuentro',
    },
    ('admin_juego/models.py', 'Condiciones'): {
        'modalidad': 'admin_juego.Modalidades',
    },
    ('admin_juego/models.py', 'JugadasInformativas'): {
        'encuentros_modalidad': 'admin_juego.EncuentrosModalidades',
        'condicion': 'admin_juego.Condiciones',
        'sistema': 'admin_juego.SistemaJuego',
        'origen': 'admin_juego.Encuentro',
    },
    ('admin_juego/models.py', 'Jugadas'): {
        'encuentros_modalidad': 'admin_juego.EncuentrosModalidades',
        'condicion': 'admin_juego.Condiciones',
        'sistema': 'admin_juego.SistemaJuego',
        'origen': 'admin_juego.Encuentro',
    },
    ('admin_juego/models.py', 'RestriccionesReferencias'): {
        'grupo': 'admin_juego.Grupo',
        'modalidad': 'admin_juego.Modalidades',
        'condicion': 'admin_juego.Condiciones',
    },

    # admin_juego/models_arrejuntao.py
    ('admin_juego/models_arrejuntao.py', 'PlantillaJugada'): {
        'producto': 'admin_juego.ProductoLoteria',
    },
    ('admin_juego/models_arrejuntao.py', 'Ticket'): {
        'producto': 'admin_juego.ProductoLoteria',
        'vendedor': 'admin_comercializacion.UsuariosTaquilla',
    },
    ('admin_juego/models_arrejuntao.py', 'ApuestaDetalle'): {
        'ticket': 'admin_juego.Ticket',
        'animalito': 'admin_juego.Animalito',
    },
    ('admin_juego/models_arrejuntao.py', 'ResultadoSorteo'): {
        'producto': 'admin_juego.ProductoLoteria',
    },
    ('admin_juego/models_arrejuntao.py', 'AnimalFigura'): {
        'grupo': 'admin_juego.GrupoAnimales',
    },
    ('admin_juego/models_arrejuntao.py', 'ProductoLoteria'): {
        'loteria': 'admin_juego.Loteria',
    },
    ('admin_juego/models_arrejuntao.py', 'SorteoProducto'): {
        'grupo_animales': 'admin_juego.GrupoAnimales',
    },
    ('admin_juego/models_arrejuntao.py', 'Sorteo'): {
        'producto': 'admin_juego.SorteoProducto',
    },

    # admin_datamart/models.py
    ('admin_datamart/models.py', 'Hecho1_VentasCadenasJuegos'): {
        'tiempo': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
        'juegos': 'admin_datamart.DimensionJuegos',
    },
    ('admin_datamart/models.py', 'Hecho2_VentasCadenasAbstract'): {
        'tiempo': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
    },
    ('admin_datamart/models.py', 'Hecho4_VentasCadenasLinea'): {
        'tiempo': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
    },
    ('admin_datamart/models.py', 'Hecho6_ComisionesCadenaJuego'): {
        'tiempo': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
        'juegos': 'admin_datamart.DimensionJuegos',
    },
    ('admin_datamart/models.py', 'Hecho7_ComisionesQuedaCadena'): {
        'tiempo': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
    },
    ('admin_datamart/models.py', 'Hecho8_VentasMonitorLinea'): {
        'tiempo': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
        'juegos': 'admin_datamart.DimensionJuegos',
    },
    ('admin_datamart/models.py', 'Hecho9_VentasSaldosCadena'): {
        'tiempo': 'admin_datamart.DimensionTiempo',
        'comercializacion': 'admin_finanzas.Comercializadora',
    },
}


def fix_file(filepath, file_corrections):
    """Fix UNKNOWN FKs in a file using class-aware context."""
    content = filepath.read_text(encoding='utf-8', errors='replace')
    if "'UNKNOWN'" not in content:
        return False

    modified = False
    lines = content.splitlines(keepends=True)
    current_class = None

    for i, line in enumerate(lines):
        # Track current class
        m = re.match(r'class (\w+)', line)
        if m:
            current_class = m.group(1)

        if "'UNKNOWN'" not in line:
            continue

        # Find field name by looking backwards
        field_name = None
        for j in range(i, max(0, i-5), -1):
            m2 = re.match(r'\s*(\w+)\s*=\s*models\.(?:ForeignKey|ManyToManyField|OneToOneField)', lines[j])
            if m2:
                field_name = m2.group(1)
                break

        if not field_name or not current_class:
            continue

        # Look up correction
        key = (file_corrections, current_class)
        target = None
        for (fpath, cls), corrections in CORRECTIONS.items():
            if fpath == file_corrections and cls == current_class:
                target = corrections.get(field_name)
                break

        if target:
            lines[i] = lines[i].replace("'UNKNOWN'", f"'{target}'", 1)
            modified = True
            print(f"  [{current_class}.{field_name}] -> {target}")

    if modified:
        filepath.write_text(''.join(lines), encoding='utf-8')
    return modified


total = 0
for rel_path in set(fp for (fp, _) in CORRECTIONS.keys()):
    filepath = base / rel_path.replace('/', '\\')
    if not filepath.exists():
        print(f"NOT FOUND: {rel_path}")
        continue
    print(f"\n=== {rel_path} ===")
    if fix_file(filepath, rel_path):
        total += 1
    else:
        print("  (no changes)")

print(f"\n=== Total files modified: {total} ===")

# Count remaining
remaining = sum(
    f.read_text(encoding='utf-8', errors='replace').count("'UNKNOWN'")
    for f in base.rglob('*.py')
    if '__pycache__' not in str(f) and 'migrations' not in str(f) and f.exists()
)
print(f"UNKNOWN remaining in non-migration Python files: {remaining}")
