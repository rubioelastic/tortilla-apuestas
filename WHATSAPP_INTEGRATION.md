# 📱 Integración WhatsApp + Firebase - TortillApuestas

## 🎉 ¡Nueva Funcionalidad Mejorada!

Ahora TortillApuestas puede enviar notificaciones automáticas por WhatsApp cuando:
- ✅ Se crea una nueva apuesta
- ✅ Se finaliza una apuesta

### 🔥 **NUEVO: Sincronización con Firebase**
- ✅ Configuración compartida entre todos los dispositivos
- ✅ Gestión centralizada de participantes y números
- ✅ Persistencia real en la nube
- ✅ Backup automático en localStorage

## 📋 Archivos del Proyecto

- **`index.html`** - Versión original (sin WhatsApp)
- **`index-whatsapp.html`** - ✨ **Nueva versión con WhatsApp + Firebase**
- **`index-firebase-fixed.html`** - Versión Firebase alternativa

## 🚀 Cómo Usar la Nueva Funcionalidad

### 1. Abrir la Nueva Versión
Usa el archivo `index-whatsapp.html` en lugar de `index.html`

### 2. Configurar WhatsApp (Mejorado)
1. Haz clic en el **botón verde de WhatsApp** (esquina inferior derecha)
2. Activa las notificaciones marcando la casilla
3. **Dos formas de gestionar contactos:**

#### 📱 **Números Rápidos** (Pestaña 1)
- Añade números directamente para notificaciones inmediatas
- Formato: `+34XXXXXXXXX` (España), `+1XXXXXXXXXX` (USA), etc.

#### 👥 **Gestionar Participantes** (Pestaña 2)
- Crea participantes con nombre + número de teléfono
- Se guardan en Firebase para futuras apuestas
- Puedes añadir sus números a notificaciones con un clic

4. Haz clic en **"Guardar"** (se sincroniza automáticamente con Firebase)

### 3. ¡Listo! 🎊
Ahora cuando:
- **Crees una nueva apuesta** → Se abrirán pestañas de WhatsApp para notificar
- **Finalices una apuesta** → Se enviará notificación del ganador
- **Cambies de dispositivo** → Tu configuración se mantiene sincronizada

## 📱 Cómo Funciona

### Notificación de Nueva Apuesta
```
🥚 NUEVA APUESTA EN TORTILLAPUESTAS 🥚

📋 Título: ¿Quién ganará la liga?
📝 Descripción: Real Madrid vs Barcelona
👥 Participantes: Javi, RaulG, Paula
📅 Fecha: 2024-12-15

¡Entra en la app para ver los detalles!
https://tu-url-de-la-app.com
```

### Notificación de Apuesta Finalizada
```
🏆 APUESTA FINALIZADA 🏆

📋 Apuesta: ¿Quién ganará la liga?
🎉 Ganador: Javi
🥚 Tortillas a pagar: 2
📝 Resultado: Real Madrid ganó 3-1

¡Javi ha ganado! 🎊
https://tu-url-de-la-app.com
```

## ⚙️ Características Técnicas

### ✅ Ventajas
- **Fácil configuración** - Solo añadir números de teléfono
- **Sin APIs complejas** - Usa WhatsApp Web directamente
- **Gratuito** - No requiere servicios de pago
- **Persistente** - Guarda la configuración en el navegador
- **Confirmación** - Pregunta antes de enviar notificaciones

### ⚠️ Limitaciones
- Requiere **acción manual** - Se abren pestañas que debes enviar
- **Una por una** - Abre una pestaña por cada contacto
- Necesita **WhatsApp Web** activo en el navegador

## 🔧 Configuración Avanzada

### Desactivar Notificaciones Temporalmente
1. Haz clic en el botón WhatsApp
2. Desmarca "Activar notificaciones WhatsApp"
3. Guarda

### Añadir/Quitar Números
- **Añadir**: Escribe el número y haz clic en "+"
- **Quitar**: Haz clic en la "X" junto al número

### Formato de Números Válidos
- ✅ `+34123456789` (España)
- ✅ `+1234567890` (USA)
- ✅ `+5491234567890` (Argentina)
- ❌ `123456789` (sin código de país)
- ❌ `+34 123 456 789` (con espacios)

## 🎯 Casos de Uso

### Para Grupos de Amigos
1. **Configuración inicial**: Una persona configura todos los números
2. **Nuevas apuestas**: Automáticamente notifica a todos
3. **Resultados**: Informa quién debe pagar tortillas

### Para Familias
- Apuestas sobre eventos familiares
- Notificaciones automáticas a todos los miembros
- Seguimiento de "deudas" de tortillas

### Para Compañeros de Trabajo
- Apuestas sobre deportes
- Resultados de predicciones
- Diversión en el equipo

## 🔄 Migración desde Versión Anterior

Si ya usabas `index.html`:

1. **Copia tus datos** (Firebase los mantiene automáticamente)
2. **Cambia a** `index-whatsapp.html`
3. **Configura WhatsApp** (primera vez)
4. **¡Disfruta las notificaciones!**

## 🆘 Solución de Problemas

### "No se abren las pestañas de WhatsApp"
- Verifica que el navegador permita pop-ups
- Comprueba que WhatsApp Web funcione en tu navegador

### "Formato de número incorrecto"
- Usa el formato: `+[código país][número]`
- Sin espacios ni guiones
- Ejemplo: `+34612345678`

### "No se guardan los números"
- Verifica que el navegador permita localStorage
- No uses modo incógnito/privado

### "Las notificaciones no se envían"
- Comprueba que esté activado en la configuración
- Verifica que hay números añadidos
- Confirma cuando aparezca el diálogo

## 🎊 ¡Disfruta de TortillApuestas con WhatsApp!

Ahora tus apuestas de tortilla serán aún más divertidas con notificaciones automáticas. ¡Que gane el mejor y que las tortillas fluyan! 🥚🎉
