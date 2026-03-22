#!/bin/bash

# 🔧 Script de Inicialización - TortillApuestas
# Este script configura todo automáticamente

set -e  # Exit si hay error

echo "🚀 Inicializando TortillApuestas..."

# 1. Crear .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  Edita .env con tus valores antes de continuar"
fi

# 2. Crear volúmenes
echo "🗄️ Creando volúmenes de datos..."
docker volume create tortilla_db_data 2>/dev/null || true

# 3. Construir imágenes
echo "🏗️  Construyendo imágenes Docker..."
docker-compose build

# 4. Iniciar servicios
echo "▶️  Iniciando servicios..."
docker-compose up -d

# 5. Esperar a que BD esté lista
echo "⏳ Esperando que la base de datos esté lista..."
sleep 10

# 6. Ver estado
echo ""
echo "✅ Estado de servicios:"
docker-compose ps

echo ""
echo "🌐 URLs de acceso:"
echo "   Frontend: http://localhost:3000"
echo "   APIs: http://localhost:8000/docs"
echo "   BD: localhost:5432"
echo ""
echo "📖 Ver logs:"
echo "   docker-compose logs -f api"
echo "   docker-compose logs -f db"
echo "   docker-compose logs -f frontend"
echo ""
echo "🎉 ¡Listo! TortillApuestas está iniciando..."
