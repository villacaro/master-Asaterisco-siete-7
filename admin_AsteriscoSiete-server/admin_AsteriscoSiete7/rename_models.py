"""
rename_models.py
Renombra clases y FKs del sistema de deportes al vocabulario de lotería/animalitos.
Aplica en todos los .py del proyecto excepto en migraciones.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# ---- Mapa de renombres de CLASES (solo en admin_juego/models.py) ----
CLASS_RENAMES = [
    # (patron_regex, reemplazo)
    (r'\bclass Deportes\b',              'class TipoProducto'),
    (r'\bclass Torneos\b',               'class # REMOVED_Producto'),
    (r'\bclass Temporadas\b',            'class PeriodoSorteo'),
    (r'\bclass Equipos\b',               'class ModalidadJuego'),
    (r'\bclass EquiposLigas\b',          'class ModalidadProducto'),
    (r'\bclass EquiposTemporadas\b',     'class ModalidadPeriodo'),
    (r'\bclass EquiposGrupos\b',         'class ModalidadGrupo'),
    (r'\bclass Modalidades\b(?!_)',      'class ModalidadJuego'),
    (r'\bclass Modalidades_Grupos\b',    'class ModalidadJuego_Grupos'),
    (r'\bclass Jornadas\b',              'class Fechas'),
    (r'\bclass Encuentros\b(?!D|M)',     'class Sorteo'),
    (r'\bclass EncuentrosDetail\b',      'class SorteoDetalle'),
    (r'\bclass EncuentrosModalidades\b', 'class SorteoModalidades'),
    (r'\bclass # REMOVED_Jugador\b(?!T)',          'class NumeroSorteo'),
    (r'\bclass # REMOVED_JugadorTipo\b',           'class TipoNumeroSorteo'),
    (r'\bclass GruposJuego\b',           'class GruposSorteo'),
    (r'\bclass GruposApuestas\b',        'class GruposApuesta'),
    (r'\bclass Deportes_Grupos\b',       'class TipoProducto_Grupos'),
    (r'\bclass # REMOVED_RestriccionesReferencias\b', 'class RestriccionesSorteo'),
]

# ---- Mapa de FKs (string refs) en TODOS los .py ----
FK_RENAMES = [
    ("'admin_juego.TipoProducto'",              "'admin_juego.TipoProducto'"),
    ("'admin_juego.# REMOVED_Producto'",               "'admin_juego.# REMOVED_Producto'"),
    ("'admin_juego.PeriodoSorteo'",            "'admin_juego.PeriodoSorteo'"),
    ("'admin_juego.ModalidadJuego'",               "'admin_juego.ModalidadJuego'"),
    ("'admin_juego.ModalidadJuego'",                "'admin_juego.ModalidadJuego'"),
    ("'admin_juego.ModalidadProducto'",          "'admin_juego.ModalidadProducto'"),
    ("'admin_juego.ModalidadPeriodo'",     "'admin_juego.ModalidadPeriodo'"),
    ("'admin_juego.ModalidadGrupo'",         "'admin_juego.ModalidadGrupo'"),
    ("'admin_juego.ModalidadJuego'",           "'admin_juego.ModalidadJuego'"),
    ("'admin_juego.ModalidadJuego_Grupos'",    "'admin_juego.ModalidadJuego_Grupos'"),
    ("'admin_juego.Fechas'",              "'admin_juego.Fechas'"),
    ("'admin_juego.Sorteo'",            "'admin_juego.Sorteo'"),
    ("'admin_juego.SorteoDetalle'",      "'admin_juego.SorteoDetalle'"),
    ("'admin_juego.SorteoModalidades'", "'admin_juego.SorteoModalidades'"),
    ("'admin_juego.NumeroSorteo'",               "'admin_juego.NumeroSorteo'"),
    ("'admin_juego.TipoNumeroSorteo'",           "'admin_juego.TipoNumeroSorteo'"),
    ("'admin_juego.TipoNumeroSorteo'",           "'admin_juego.TipoNumeroSorteo'"),
    ("'admin_juego.GruposSorteo'",           "'admin_juego.GruposSorteo'"),
    ("'admin_juego.GruposApuesta'",        "'admin_juego.GruposApuesta'"),
    ("'admin_juego.TipoProducto_Grupos'",       "'admin_juego.TipoProducto_Grupos'"),
    ("'admin_juego.# REMOVED_Producto'",                  "'admin_juego.# REMOVED_Producto'"),
    ("'admin_juego.GruposSorteo'",                 "'admin_juego.GruposSorteo'"),
    # Fixes de nombres sin app prefix
    ("'admin_status.Status'",                            "'admin_status.Status'"),
]

def process_file(filepath, class_renames=False):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
            original = fh.read()
    except Exception as e:
        print(f"  SKIP (read error): {filepath}: {e}")
        return

    content = original

    # Aplicar renombres de clases solo en admin_juego/models.py
    if class_renames:
        for pattern, replacement in CLASS_RENAMES:
            content = re.sub(pattern, replacement, content)

    # Aplicar correcciones de FKs en todos los archivos
    for old, new in FK_RENAMES:
        content = content.replace(old, new)

    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            print(f"  FIXED: {os.path.relpath(filepath, BASE)}")
        except Exception as e:
            print(f"  ERROR writing {filepath}: {e}")


def main():
    print("=== Renombrando modelos a vocabulario de lotería ===\n")
    fixed = 0

    for root, dirs, files in os.walk(BASE):
        # Excluir carpetas de migraciones y la propia carpeta de scripts
        dirs[:] = [d for d in dirs if d not in ('migrations', '__pycache__', '.git', 'node_modules')]

        for fname in files:
            if not fname.endswith('.py'):
                continue

            fpath = os.path.join(root, fname)
            is_juego_models = (
                os.path.basename(root) == 'admin_juego' and fname == 'models.py'
            )
            process_file(fpath, class_renames=is_juego_models)

    print("\n=== COMPLETADO ===")


if __name__ == '__main__':
    main()
