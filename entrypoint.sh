#!/bin/bash
# NO usar set -e: los comandos de setup pueden fallar sin detener el servidor

# El workdir en el Dockerfile es /app, y manage.py está en el subdirectorio
cd /app/admin_AsteriscoSiete-server/admin_AsteriscoSiete7

echo "=== Migraciones ==="
python manage.py migrate --no-input

echo "=== Superusuario ==="
python manage.py ensure_superuser || echo "⚠ ensure_superuser warning (continúa)"

echo "=== Setup taquilla inicial (idempotente) ==="
python manage.py setup_taquilla_inicial || echo "⚠ setup_taquilla_inicial warning (continúa)"

echo "=== Reset usuario taquilla (garantiza password hasheado) ==="
python manage.py reset_taquilla_user || echo "⚠ reset_taquilla_user warning"

echo "=== Iniciando Gunicorn en 0.0.0.0:${PORT:-8080} ==="
exec gunicorn admin_AsteriscoSiete7.wsgi:application \
    --bind 0.0.0.0:${PORT:-8080} \
    --workers 2 \
    --timeout 120
