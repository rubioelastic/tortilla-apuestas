#!/bin/bash

echo "🔧 Reiniciando Nginx Proxy Manager..."

# Reiniciar el contenedor
docker restart nginx-proxy-manager-app-1

echo "⏳ Esperando 15 segundos a que inicie..."
sleep 15

# Verificar estado
echo ""
echo "📊 Estado del contenedor:"
docker ps | grep nginx-proxy-manager

echo ""
echo "🔍 Verificando conectividad..."
curl -I http://localhost:8181 2>&1 | head -3

echo ""
echo "📋 Últimos logs:"
docker logs nginx-proxy-manager-app-1 --tail 20

echo ""
echo "✅ Reinicio completado"
echo "🌐 Intenta acceder a: http://192.168.1.115:8181"
