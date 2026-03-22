#!/bin/bash

# 🚀 Script de Despliegue Automático - TortillApuestas
# Despliega la aplicación en el servidor con Docker

set -e  # Detener si hay algún error

# ═══════════════════════════════════════════════════════════════
# Configuración
# ═══════════════════════════════════════════════════════════════
SERVER_USER="securedatauser"
SERVER_HOST="192.168.1.115"
SERVER_PORT="22"
SERVER_PATH="/home/$SERVER_USER/tortilla-apuestas"

echo "🐋 TortillApuestas - Despliegue Automático"
echo "=========================================="
echo ""
echo "🎯 Servidor: $SERVER_USER@$SERVER_HOST:$SERVER_PORT"
echo "📁 Destino: $SERVER_PATH"
echo ""

# ═══════════════════════════════════════════════════════════════
# Paso 1: Verificar conexión SSH
# ═══════════════════════════════════════════════════════════════
echo "🔍 Paso 1/6: Verificando conexión SSH..."
if ssh -p $SERVER_PORT -o ConnectTimeout=5 $SERVER_USER@$SERVER_HOST "echo 'OK'" &>/dev/null; then
    echo "✅ Conexión SSH exitosa"
else
    echo "❌ No se puede conectar al servidor"
    echo "Verifica:"
    echo "  - Usuario: $SERVER_USER"
    echo "  - Host: $SERVER_HOST"
    echo "  - Puerto: $SERVER_PORT"
    echo "  - Que tienes permisos SSH"
    exit 1
fi
echo ""

# ═══════════════════════════════════════════════════════════════
# Paso 2: Verificar Docker en servidor
# ═══════════════════════════════════════════════════════════════
echo "🐳 Paso 2/6: Verificando Docker en servidor..."
if ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "docker --version" &>/dev/null; then
    DOCKER_VERSION=$(ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "docker --version")
    echo "✅ Docker instalado: $DOCKER_VERSION"
else
    echo "⚠️  Docker no está instalado en el servidor"
    echo "¿Quieres instalarlo automáticamente? (s/n)"
    read -n 1 INSTALL_DOCKER
    echo ""
    
    if [[ $INSTALL_DOCKER =~ ^[SsYy]$ ]]; then
        echo "📦 Instalando Docker..."
        ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST << 'ENDSSH'
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo bash get-docker.sh
            sudo usermod -aG docker $USER
            rm get-docker.sh
ENDSSH
        echo "✅ Docker instalado. Debes cerrar sesión SSH y volver a entrar para aplicar permisos."
        echo "Ejecuta este script de nuevo después."
        exit 0
    else
        echo "❌ Docker es necesario. Instálalo manualmente:"
        echo "   curl -fsSL https://get.docker.com | sudo bash"
        exit 1
    fi
fi
echo ""

# ═══════════════════════════════════════════════════════════════
# Paso 3: Transferir archivos al servidor
# ═══════════════════════════════════════════════════════════════
echo "📦 Paso 3/6: Transfiriendo archivos al servidor..."

# Crear directorio en servidor si no existe
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "mkdir -p $SERVER_PATH"

# Transferir archivos (excluye archivos innecesarios)
rsync -avz --progress \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude 'venv' \
    --exclude 'env' \
    --exclude '.DS_Store' \
    --exclude 'node_modules' \
    --exclude '.vscode' \
    --exclude '*.log' \
    -e "ssh -p $SERVER_PORT" \
    ./ $SERVER_USER@$SERVER_HOST:$SERVER_PATH/

echo "✅ Archivos transferidos"
echo ""

# ═══════════════════════════════════════════════════════════════
# Paso 4: Configurar .env en servidor
# ═══════════════════════════════════════════════════════════════
echo "⚙️  Paso 4/6: Configurando variables de entorno..."

# Generar SECRET_KEY única
SECRET_KEY=$(openssl rand -hex 32)

ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST << ENDSSH
cd $SERVER_PATH

# Crear .env si no existe
if [ ! -f .env ]; then
    echo "Creando .env..."
    cat > .env << 'EOF'
# Base de datos SQLite
DB_PATH=/app/data/tortilla_apuestas_dev.db

# Seguridad - Generada automáticamente
SECRET_KEY=$SECRET_KEY

# Entorno
ENVIRONMENT=production

# URL del frontend
FRONTEND_URL=http://192.168.1.115
EOF
    echo "✅ .env creado"
else
    echo "✅ .env ya existe (no se modifica)"
fi
ENDSSH

echo "✅ Configuración lista"
echo ""

# ═══════════════════════════════════════════════════════════════
# Paso 5: Detener contenedores anteriores (si existen)
# ═══════════════════════════════════════════════════════════════
echo "🔄 Paso 5/6: Deteniendo contenedores anteriores..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST << ENDSSH
cd $SERVER_PATH
if docker compose ps -q &>/dev/null; then
    echo "Deteniendo contenedores existentes..."
    docker compose down
fi
ENDSSH
echo "✅ Limpieza completada"
echo ""

# ═══════════════════════════════════════════════════════════════
# Paso 6: Construir e iniciar contenedores
# ═══════════════════════════════════════════════════════════════
echo "🚀 Paso 6/6: Construyendo e iniciando contenedores..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST << ENDSSH
cd $SERVER_PATH

# Construir imágenes
echo "Construyendo imágenes Docker..."
docker compose build

# Iniciar servicios
echo "Iniciando servicios..."
docker compose up -d

# Esperar a que los servicios estén listos
echo "Esperando a que los servicios estén listos..."
sleep 5

# Verificar estado
echo ""
echo "Estado de los contenedores:"
docker compose ps

# Verificar logs
echo ""
echo "Últimos logs:"
docker compose logs --tail=10
ENDSSH

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🎉 ¡Despliegue completado exitosamente!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📍 Accesos:"
echo "   Frontend:  http://192.168.1.115:3000"
echo "   Backend:   http://192.168.1.115:8000"
echo "   API Docs:  http://192.168.1.115:8000/docs"
echo ""
echo "🔐 Credenciales de prueba:"
echo "   Usuario: javi"
echo "   Contraseña: tortilla123"
echo ""
echo "📋 Comandos útiles en el servidor:"
echo "   ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST"
echo "   cd $SERVER_PATH"
echo "   docker compose logs -f          # Ver logs"
echo "   docker compose restart          # Reiniciar"
echo "   docker compose down             # Detener"
echo "   docker compose ps               # Ver estado"
echo ""
echo "📊 Hacer backup de la BD:"
echo "   ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST \"docker cp tortilla-api:/app/data/tortilla_apuestas_dev.db ~/backup.db\""
echo ""
