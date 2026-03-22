# 🔔 Recordatorios Semanales de Deudas - TortillApuestas

## ¿Qué hace?

Envía un mensaje automático **cada lunes a las 10:00 AM** al grupo de Telegram con:
- Lista de todas las apuestas pendientes de pago
- Quién debe tortillas en cada apuesta
- Cuántas tortillas debe cada uno

---

## Instalación del Cron Job

### En el servidor

1. **Copiar el script al servidor:**
```bash
scp backend/cron_remind_debts.sh servidor-tortilla:/home/securedatauser/tortilla-apuestas/backend/
```

2. **Dar permisos de ejecución:**
```bash
ssh servidor-tortilla
chmod +x /home/securedatauser/tortilla-apuestas/backend/cron_remind_debts.sh
```

3. **Editar el crontab:**
```bash
crontab -e
```

4. **Agregar esta línea** (lunes a las 10:00 AM):
```
0 10 * * 1 /home/securedatauser/tortilla-apuestas/backend/cron_remind_debts.sh >> /home/securedatauser/tortilla-apuestas/logs/remind_debts.log 2>&1
```

5. **Crear el directorio de logs:**
```bash
mkdir -p /home/securedatauser/tortilla-apuestas/logs
```

6. **Guardar y salir** (en vim: `:wq`, en nano: `Ctrl+X` luego `Y`)

---

## Configuración del Horario

El formato de crontab es: `minuto hora día_mes mes día_semana`

**Ejemplos:**

| Horario | Crontab |
|---------|---------|
| Lunes 10:00 AM | `0 10 * * 1` |
| Viernes 18:00 | `0 18 * * 5` |
| Domingo 12:00 | `0 12 * * 0` |
| Cada día 9:00 AM | `0 9 * * *` |
| Dos veces por semana (Mar y Vie 10 AM) | `0 10 * * 2,5` |

---

## Prueba Manual

Para probar sin esperar al lunes:

```bash
# Desde el servidor
ssh servidor-tortilla
cd /home/securedatauser/tortilla-apuestas/backend
./cron_remind_debts.sh
```

O desde la API directamente:
```bash
curl -X POST https://tortilla.rubiocloud.duckdns.org/api/telegram/remind-debts
```

O desde el navegador:
- Ve a https://tortilla.rubiocloud.duckdns.org/docs
- Busca `POST /api/telegram/remind-debts`
- Click en "Try it out" → "Execute"

---

## Verificar que el Cron está Funcionando

**Ver el crontab actual:**
```bash
crontab -l
```

**Ver logs de recordatorios:**
```bash
tail -f /home/securedatauser/tortilla-apuestas/logs/remind_debts.log
```

**Ver logs del sistema de cron:**
```bash
grep CRON /var/log/syslog | tail -20
```

---

## Desactivar Temporalmente

Si quieres pausar los recordatorios sin borrar el cron:

```bash
crontab -e
```

Comenta la línea agregando `#` al inicio:
```
# 0 10 * * 1 /home/securedatauser/tortilla-apuestas/backend/cron_remind_debts.sh >> /home/securedatauser/tortilla-apuestas/logs/remind_debts.log 2>&1
```

---

## Ejemplo de Mensaje que Envía

```
⏰ RECORDATORIO SEMANAL - TORTILLAS PENDIENTES

📊 Hay 2 apuesta(s) sin pagar:

━━━━━━━━━━━━━━━━━━━━
🎯 España gana el mundial
💰 Tortillas: 5
😢 Deben pagar: Juan, Pedro
📅 Finalizada: 15/02/2026

━━━━━━━━━━━━━━━━━━━━
🎯 Llueve el sábado
💰 Tortillas: 2
😢 Deben pagar: María
📅 Finalizada: 18/02/2026

━━━━━━━━━━━━━━━━━━━━
🥞 ¡A pagar las tortillas, amigos!
🔗 https://tortilla.rubiocloud.duckdns.org
```

---

## Solución de Problemas

**El cron no se ejecuta:**
1. Verificar que el script tiene permisos: `ls -l cron_remind_debts.sh`
2. Verificar que el crontab está activo: `service cron status`
3. Revisar logs: `cat /home/securedatauser/tortilla-apuestas/logs/remind_debts.log`

**El script da error:**
- Asegurarse de que curl está instalado: `which curl`
- Verificar que la API está corriendo: `docker ps | grep tortilla-api`
- Probar el endpoint manualmente con curl

---

## Personalización

Puedes modificar el horario, frecuencia o el mensaje editando:
- **Horario:** Cambiar el crontab
- **Mensaje:** Editar `backend/main.py` en la función `remind_pending_debts()`
- **URL API:** Editar `backend/cron_remind_debts.sh`
