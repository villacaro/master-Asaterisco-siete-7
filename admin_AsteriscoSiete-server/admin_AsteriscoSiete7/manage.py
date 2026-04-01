#!/usr/bin/env python
import os
import sys


def _detect_local_settings():
    """
    Usa settings_local.py automáticamente cuando se corre en Windows
    o cuando psycopg2/psycopg no están disponibles (entorno de desarrollo).
    En producción (Linux + PostgreSQL) usa settings.py normal.
    """
    # Permite override explícito desde el entorno
    if os.environ.get("DJANGO_SETTINGS_MODULE"):
        return

    # En Windows o sin PostgreSQL: usar settings locales (SQLite)
    is_windows = sys.platform.startswith("win")
    try:
        import psycopg2  # noqa
        has_pg = True
    except ImportError:
        try:
            import psycopg  # noqa
            has_pg = True
        except ImportError:
            has_pg = False

    if is_windows or not has_pg:
        os.environ["DJANGO_SETTINGS_MODULE"] = "admin_asterisco7.settings_local"
    else:
        os.environ["DJANGO_SETTINGS_MODULE"] = "admin_asterisco7.settings"


if __name__ == "__main__":
    _detect_local_settings()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
