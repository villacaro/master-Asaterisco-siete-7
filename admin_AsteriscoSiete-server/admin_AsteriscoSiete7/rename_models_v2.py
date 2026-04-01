"""
rename_models_v2.py  
Corrige TODAS las referencias a nombres viejos dentro del código Python
(no solo FKs string ni definiciones de clase), incluyendo código interno.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

JUEGO_MODELS = os.path.join(BASE, 'admin_juego', 'models.py')

# Mapa: nombre viejo → nombre nuevo (para referencias en código Python)
CODE_RENAMES = [
    # Orden importa: más específico primero
    ('EncuentrosModalidades',   'SorteoModalidades'),
    ('EncuentrosDetail',        'SorteoDetalle'),
    ('Encuentros',              'Sorteo'),
    ('Deportes_Grupos',         'TipoProducto_Grupos'),
    ('Modalidades_Grupos',      'ModalidadJuego_Grupos'),
    ('Modalidades',             'ModalidadJuego'),
    ('Deportes',                'TipoProducto'),
    ('Torneos',                 '# REMOVED_Producto'),
    ('Temporadas',              'PeriodoSorteo'),
    ('EquiposTemporadas',       'ModalidadPeriodo'),
    ('EquiposGrupos',           'ModalidadGrupo'),
    ('EquiposLigas',            'ModalidadProducto'),
    ('Equipos',                 'ModalidadJuego'),
    ('# REMOVED_JugadorTipo',             'TipoNumeroSorteo'),
    ('# REMOVED_Jugador',                 'NumeroSorteo'),
    ('GruposApuestas',          'GruposApuesta'),
    ('GruposJuego',             'GruposSorteo'),
    ('Jornadas',                'Fechas'),
    ('# REMOVED_RestriccionesReferencias','RestriccionesSorteo'),
]

def rename_in_code(content, renames):
    """Reemplaza referencias de nombre en código Python (word boundaries)."""
    for old, new in renames:
        # Word boundary para no reemplazar subcadenas
        content = re.sub(r'\b' + re.escape(old) + r'\b', new, content)
    return content


def process_file(filepath, apply_code_renames=True):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
            original = fh.read()
    except Exception as e:
        print(f"  SKIP (read error): {filepath}: {e}")
        return

    content = original
    if apply_code_renames:
        content = rename_in_code(content, CODE_RENAMES)

    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            rel = os.path.relpath(filepath, BASE)
            print(f"  FIXED: {rel}")
        except Exception as e:
            print(f"  ERROR writing {filepath}: {e}")


def main():
    print("=== Corrigiendo referencias internas en admin_juego/models.py ===\n")

    # Solo aplicar renombres de código en admin_juego/models.py
    # (otros archivos solo tienen FKs strings, ya corregidas antes)
    process_file(JUEGO_MODELS, apply_code_renames=True)

    print("\n=== COMPLETADO ===")


if __name__ == '__main__':
    main()
