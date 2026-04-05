#!/bin/bash
set -e

# El workdir en el Dockerfile es /app, y manage.py está en el subdirectorio
cd /app/admin_AsteriscoSiete-server/admin_AsteriscoSiete7

echo "=== Migraciones ==="
python manage.py migrate --no-input

echo "=== Superusuario ==="
python manage.py ensure_superuser

echo "=== Setup taquilla inicial (idempotente) ==="
python manage.py setup_taquilla_inicial

echo "=== Reset usuario taquilla (garantiza password hasheado) ==="
python manage.py reset_taquilla_user

echo "=== Iniciando Gunicorn en 0.0.0.0:${PORT:-8080} ==="
exec gunicorn admin_AsteriscoSiete7.wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers 2 \
    --timeout 120
