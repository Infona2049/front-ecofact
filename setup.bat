@echo off
echo ========================================
echo   CONFIGURACION AUTOMATICA - ECOFACT
echo ========================================
echo.

echo [1/6] Creando entorno virtual...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: No se pudo crear el entorno virtual
    echo Verifica que Python este instalado
    pause
    exit /b 1
)

echo [2/6] Activando entorno virtual...
call venv\Scripts\activate.bat

echo [3/6] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo [4/6] Configurando variables de entorno...
if not exist .env (
    copy .env.example .env
    echo Archivo .env creado con configuracion de Neon
) else (
    echo Archivo .env ya existe
)

echo [5/6] Ejecutando migraciones...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron ejecutar las migraciones
    pause
    exit /b 1
)

echo [6/6] Configuracion completada!
echo.
echo ========================================
echo   CONFIGURACION EXITOSA
echo ========================================
echo.
echo Usuarios disponibles:
echo - Admin: admin@ecofact.com / admin123
echo - Vendedor: vendedor@ecofact.com / vendedor123
echo - Cliente: cliente@ecofact.com / cliente123
echo.
echo Para crear mas usuarios admin/vendedor:
echo - Ve a http://localhost:8001/admin/
echo - Usuario: superadmin@ecofact.com
echo - Pass: superadmin123
echo.
echo Para iniciar el servidor ejecuta:
echo python manage.py runserver 8001
echo.
pause