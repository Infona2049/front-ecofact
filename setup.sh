#!/bin/bash

echo "========================================"
echo "   CONFIGURACION AUTOMATICA - ECOFACT"
echo "========================================"
echo ""

echo "[1/6] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    echo "Verifica que Python3 este instalado"
    exit 1
fi

echo "[2/6] Activando entorno virtual..."
source venv/bin/activate

echo "[3/6] Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo "[4/6] Configurando variables de entorno..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Archivo .env creado con configuracion de Neon"
else
    echo "Archivo .env ya existe"
fi

echo "[5/6] Ejecutando migraciones..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron ejecutar las migraciones"
    exit 1
fi

echo "[6/6] Configuracion completada!"
echo ""
echo "========================================"
echo "   CONFIGURACION EXITOSA"
echo "========================================"
echo ""
echo "Usuarios disponibles:"
echo "- Admin: admin@ecofact.com / admin123"
echo "- Vendedor: vendedor@ecofact.com / vendedor123"
echo "- Cliente: cliente@ecofact.com / cliente123"
echo ""
echo "Para crear mas usuarios admin/vendedor:"
echo "- Ve a http://localhost:8001/admin/"
echo "- Usuario: superadmin@ecofact.com"
echo "- Pass: superadmin123"
echo ""
echo "Para iniciar el servidor ejecuta:"
echo "python manage.py runserver 8001"
echo ""