@echo off
chcp 65001 > nul
echo ============================================
echo   EL ARREJUNTAO  –  Backend Django
echo   http://localhost:8000
echo   http://localhost:8000/admin/
echo   http://localhost:8000/api/health/
echo   http://localhost:8000/api/resultados/
echo ============================================
echo.

cd /d "%~dp0"

:: Activar entorno virtual (en la raíz del proyecto)
call ..\..venv\Scripts\activate.bat 2>nul || call ..\.venv\Scripts\activate.bat 2>nul

echo [1/2] Aplicando migraciones...
python manage.py migrate --run-syncdb

echo.
echo [2/2] Iniciando servidor Django en http://localhost:8000
echo       Presiona Ctrl+C para detener.
echo.
python manage.py runserver 8000
pause
