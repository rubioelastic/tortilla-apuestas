#!/bin/bash

# 🔔 Script para recordatorio semanal de deudas
# Se ejecuta automáticamente cada lunes a las 10:00 AM

# Configuración
API_URL="https://tortilla.rubiocloud.duckdns.org/api/telegram/remind-debts"

# Ejecutar el recordatorio
echo "[$(date)] Ejecutando recordatorio de deudas..."
response=$(curl -s -X POST "$API_URL" -H "Content-Type: application/json")

# Log del resultado
echo "[$(date)] Respuesta: $response"

# Verificar si fue exitoso
if echo "$response" | grep -q '"success":true'; then
    echo "[$(date)] ✅ Recordatorio enviado exitosamente"
else
    echo "[$(date)] ❌ Error al enviar recordatorio"
fi
