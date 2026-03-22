#!/bin/bash

# 🐋 Script de inicio rápido - TortillApuestas Docker
# Este script facilita el primer inicio de la aplicación con Docker

set -e  # Detener en caso de error

echo "🐋 TortillApuestas - Configuración Docker"
echo "========================================"
echo ""

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    echo "📥 Instala Docker Desktop desde: https://docs.docker.com/desktop/install/mac-install/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

echo "✅ Docker está instalado"
echo ""

# Verificar archivo .env
if [ ! -f .env ]; then
    echo "📄 Creando archivo .env desde .env.example..."
    cp .env.example .env
    
    # Generar SECRET_KEY aleatoria
    if command -v openssl &> /dev/null; then
        SECRET_KEY=$(openssl rand -hex 32)
        # Reemplazar en .env (compatible con Mac)
        sed -i '' "s/your-super-secret-key-change-this-please-1234567890abc/$SECRET_KEY/" .env
        echo "🔑 SECRET_KEY generada automáticamente"
    else
        echo "⚠️  Recuerda cambiar SECRET_KEY en .env manualmente"
    fi
    echo ""
else
    echo "✅ Archivo .env ya existe"
    echo ""
fi

# Verificar si la base de datos existe
if [ -f backend/tortilla_apuestas_dev.db ]; then
    echo "✅ Base de datos SQLite encontrada"
    echo "📊 Datos: $(stat -f%z backend/tortilla_apuestas_dev.db 2>/dev/null || stat -c%s backend/tortilla_apuestas_dev.db) bytes"
    echo ""
else
    echo "⚠️  No se encontró base de datos existente"
    echo "ℹ️  Se creará una nueva al iniciar"
    echo ""
fi

# Preguntar si quiere iniciar
read -p "¿Quieres iniciar los contenedores ahora? (s/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[SsYy]$ ]]; then
    echo ""
    echo "🚀 Construyendo imágenes..."
    docker-compose build
    
    echo ""
    echo "🏃 Iniciando contenedores..."
    docker-compose up -d
    
    echo ""
    echo "⏳ Esperando que los servicios estén listos..."
    sleep 5
    
    echo ""
    echo "✅ ¡Aplicación iniciada!"
    echo ""
    echo "📍 Accesos:"
    echo "   Frontend:  http://localhost:3000"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📋 Comandos útiles:"
    echo "   Ver logs:     docker-compose logs -f"
    echo "   Detener:      docker-compose down"
    echo "   Reiniciar:    docker-compose restart"
    echo ""
    echo "🎉 ¡Disfruta de TortillApuestas!"
else
    echo ""
    echo "ℹ️  Puedes iniciar manualmente con: docker-compose up -d"
fi
