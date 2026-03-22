# 🏆 Hall of Fame / Shame - TortillApuestas

## Descripción

Sistema de estadísticas divertidas que muestra los mejores y peores momentos de los jugadores de TortillApuestas.

## Categorías

### 👑 Rey de las Tortillas
- **Descripción**: Jugador con más victorias totales
- **Métrica**: Cantidad de apuestas ganadas
- **Color**: Amarillo

### 🔥 Racha Ganadora
- **Descripción**: Mayor cantidad de victorias consecutivas actuales
- **Métrica**: Número de apuestas ganadas seguidas
- **Color**: Rojo

### 🎰 Apostador Compulsivo
- **Descripción**: Jugador que más apuestas ha creado
- **Métrica**: Total de apuestas creadas
- **Color**: Púrpura

### ⚡ El Generoso
- **Descripción**: Jugador que paga más rápido sus deudas
- **Métrica**: Promedio de días entre finalización y pago
- **Color**: Verde

### 💸 Peor Pagador
- **Descripción**: Jugador con más tortillas sin pagar
- **Métrica**: Total de tortillas en estado "completed" (no pagadas)
- **Color**: Naranja

### 💀 Racha Perdedora
- **Descripción**: Mayor cantidad de derrotas consecutivas actuales
- **Métrica**: Número de apuestas perdidas seguidas
- **Color**: Gris

## Endpoints Backend

### GET `/api/stats/hall-of-fame`
Obtiene las estadísticas del Hall of Fame.

**Autenticación**: Bearer Token requerido

**Respuesta**:
```json
{
  "king_of_tortillas": {
    "user_id": 1,
    "display_name": "Juan",
    "wins": 15
  },
  "worst_payer": {
    "user_id": 2,
    "display_name": "Pedro",
    "pending_tortillas": 8
  },
  "compulsive_better": {
    "user_id": 3,
    "display_name": "María",
    "bets_created": 23
  },
  "generous_one": {
    "user_id": 4,
    "display_name": "Luis",
    "avg_days_to_pay": 2.5
  },
  "winning_streak": {
    "user_id": 1,
    "display_name": "Juan",
    "streak": 5
  },
  "losing_streak": {
    "user_id": 2,
    "display_name": "Pedro",
    "streak": 3
  }
}
```

### POST `/api/telegram/hall-of-fame`
Envía el Hall of Fame al grupo de Telegram.

**Autenticación**: Bearer Token requerido

**Respuesta**:
```json
{
  "success": true,
  "message": "Hall of Fame enviado a Telegram",
  "data": { /* datos del hall of fame */ }
}
```

## Frontend

### Ubicación
La sección de Hall of Fame se encuentra en la página principal, después del ranking Top 5.

### Funcionalidades
- **Visualización automática**: Se carga al iniciar la app y después del login
- **Actualización manual**: Se actualiza cuando se finaliza o paga una apuesta
- **Envío a Telegram**: Botón "Enviar" para compartir las estadísticas en el grupo

### Diseño
Cada categoría se muestra como una tarjeta con:
- Emoji representativo
- Nombre de la categoría en negrita
- Nombre del jugador y su métrica
- Color distintivo según la categoría

## Integración con Telegram

El mensaje enviado a Telegram tiene el formato:

```
🏆 HALL OF FAME / SHAME 🏆

𝗘𝘀𝘁𝗮𝗱í𝘀𝘁𝗶𝗰𝗮𝘀 𝗱𝗲 𝗧𝗼𝗿𝘁𝗶𝗹𝗹𝗔𝗽𝘂𝗲𝘀𝘁𝗮𝘀

👑 REY DE LAS TORTILLAS
Juan - 15 victorias

🔥 RACHA GANADORA
Juan - 5 victorias consecutivas

🎰 APOSTADOR COMPULSIVO
María - 23 apuestas creadas

⚡ EL GENEROSO
Luis - Paga en 2.5 días promedio

💸 PEOR PAGADOR
Pedro - 8 tortillas pendientes

💀 RACHA PERDEDORA
Pedro - 3 derrotas consecutivas

━━━━━━━━━━━━━━━━
🥞 ¡Que fluyan las tortillas!
🔗 https://tortilla.rubiocloud.duckdns.org
```

## Cálculo de Estadísticas

### Rey de las Tortillas
- Cuenta todas las apuestas donde el usuario eligió la opción ganadora
- Estados considerados: `completed`, `paid`

### Racha Ganadora/Perdedora
- Toma las últimas 20 apuestas completadas del usuario
- Cuenta cuántas victorias/derrotas consecutivas hay desde la más reciente
- Se detiene cuando hay una apuesta del tipo contrario

### Apostador Compulsivo
- Cuenta todas las apuestas creadas por el usuario (independiente del estado)

### El Generoso
- Calcula el promedio de días entre `completed_at` y `paid_at`
- Solo cuenta apuestas donde el usuario perdió y ya pagó (estado `paid`)

### Peor Pagador
- Suma las tortillas de todas las apuestas donde el usuario perdió
- Solo cuenta apuestas en estado `completed` (no pagadas aún)

## Uso

### Desde la Web
1. Inicia sesión en la aplicación
2. La sección de Hall of Fame se carga automáticamente en la página principal
3. Haz clic en el botón "Enviar" para compartir en Telegram

### Manual desde Backend
```bash
# Obtener estadísticas (requiere token)
curl -X GET "http://localhost:8000/api/stats/hall-of-fame" \
  -H "Authorization: Bearer TU_TOKEN"

# Enviar a Telegram (requiere token)
curl -X POST "http://localhost:8000/api/telegram/hall-of-fame" \
  -H "Authorization: Bearer TU_TOKEN"
```

## Archivos Modificados

### Backend
- `backend/schemas.py` - Nuevo schema `HallOfFameResponse`
- `backend/main.py` - Endpoints `/api/stats/hall-of-fame` y `/api/telegram/hall-of-fame`
- `backend/telegram_service.py` - Función `send_hall_of_fame()`

### Frontend
- `frontend/index.html` - Sección HTML del Hall of Fame y funciones JavaScript:
  - `loadHallOfFame()` - Carga las estadísticas
  - `sendHallOfFameToTelegram()` - Envía al grupo

## Ideas Futuras

- **Historial**: Guardar el Hall of Fame mensual para ver evolución
- **Badges**: Otorgar insignias permanentes a quienes ocupan el #1
- **Notificaciones automáticas**: Enviar Hall of Fame cada mes automáticamente
- **Categorías adicionales**:
  - 🎯 El Preciso (mejor ratio de aciertos)
  - 💎 El Millonario (más tortillas ganadas en total)
  - 🤝 El Sociable (participa en más apuestas)
  - ⏰ El Madrugador (crea apuestas más temprano)

## Estado

✅ **Implementado y desplegado en producción** (26 de febrero de 2026)

- Backend: Todos los endpoints funcionando
- Frontend: Visualización completa
- Telegram: Integración operativa
- Base de datos: Sin cambios de esquema necesarios
