#!/bin/bash

# Script para actualizar el estado de la apuesta del City en el servidor remoto

echo "🔄 Actualizando estado de apuesta en servidor remoto..."
echo ""

# Ejecutar comando en el contenedor del backend en el servidor remoto
ssh -p 22 securedatauser@192.168.1.115 << 'ENDSSH'
cd /home/securedatauser/tortilla-apuestas
echo "📊 Verificando contenedores..."
docker compose ps | grep tortilla-api
echo ""
echo "🔄 Actualizando estado de la apuesta usando Python..."
docker exec tortilla-api python3 -c "
import sqlite3
# Usar la ruta correcta que usa el backend
conn = sqlite3.connect('/app/data/tortilla_apuestas_dev.db')
c = conn.cursor()
print('📊 Estado actual:')
c.execute('SELECT id, title, status, winning_option FROM bets WHERE id = 1')
result = c.fetchone()
print(f'  ID: {result[0]}')
print(f'  Título: {result[1]}')
print(f'  Estado: {result[2]}')
print(f'  Ganador: {result[3]}')
print()
print('🔄 Actualizando a estado completed...')
c.execute('UPDATE bets SET status = ? WHERE id = ?', ('completed', 1))
conn.commit()
print('✅ Estado actualizado:')
c.execute('SELECT id, title, status, winning_option FROM bets WHERE id = 1')
result = c.fetchone()
print(f'  ID: {result[0]}')
print(f'  Título: {result[1]}')
print(f'  Estado: {result[2]}')
print(f'  Ganador: {result[3]}')
conn.close()
"
ENDSSH

echo ""
echo "✅ Cambio completado. Refresca la app en el navegador."
