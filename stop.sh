#!/bin/bash

# 🛑 STOP - Esto detiene todos los servicios sin perder datos

echo "🛑 Deteniendo TortillApuestas..."
docker-compose down

echo ""
echo "✅ Servicios detenidos"
echo ""
echo "Para reiniciar:"
echo "  docker-compose up -d"
echo ""
echo "Para ver que sigue activo:"
echo "  docker volume ls"
