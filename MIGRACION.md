# 📦 Guía de Migración: Firebase → Servidor Privado

Esta guía te ayudará a migrar todos tus datos desde el proyecto original en Firebase al nuevo servidor privado con SQLite.

## 📋 Tabla de Contenidos

1. [Preparación](#preparación)
2. [Limpiar datos de prueba](#limpiar-datos-de-prueba)
3. [Obtener credenciales de Firebase](#obtener-credenciales-de-firebase)
4. [Ejecutar migración](#ejecutar-migración)
5. [Verificar datos migrados](#verificar-datos-migrados)
6. [Solución de problemas](#solución-de-problemas)

---

## 🛠️ Preparación

### Requisitos previos

- Python 3.8 o superior
- Acceso a tu proyecto Firebase
- Permisos de administrador en Firebase Console

### Instalar dependencias

```bash
cd backend
pip install firebase-admin
```

---

## 🧹 Limpiar datos de prueba

Antes de migrar, limpia todos los datos de prueba actuales:

```bash
cd backend
python3 clean_test_data.py
```

El script te pedirá confirmación antes de eliminar:
- ✅ Todas las apuestas de prueba
- ✅ Todos los usuarios de prueba
- ✅ Todas las participaciones de prueba

**⚠️ IMPORTANTE**: Esta operación no se puede deshacer. Asegúrate de que no hay datos importantes.

---

## 🔑 Obtener credenciales de Firebase

### Paso 1: Acceder a Firebase Console

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Inicia sesión con tu cuenta de Google
3. Selecciona el proyecto **"tortilla-apuestas"**

### Paso 2: Generar clave privada

1. Click en el ⚙️ (configuración) → **Project Settings**
2. Ve a la pestaña **Service Accounts**
3. Selecciona **Python** como lenguaje
4. Click en **"Generate new private key"**
5. Confirma en el diálogo
6. Se descargará un archivo JSON (ej: `tortilla-apuestas-firebase-adminsdk-xxxxx.json`)

### Paso 3: Guardar credenciales

Mueve el archivo descargado a la carpeta `backend`:

```bash
mv ~/Downloads/tortilla-apuestas-*.json backend/firebase-credentials.json
```

**🔒 SEGURIDAD**: Este archivo contiene credenciales sensibles. NO lo subas a GitHub.

---

## 🚀 Ejecutar migración

### Comando de migración

```bash
cd backend
python3 migrate_from_firebase.py firebase-credentials.json
```

### Proceso paso a paso

El script hará lo siguiente:

1. **Conectar a Firebase** ✅
   - Validará las credenciales
   - Accederá a las colecciones

2. **Obtener datos** 📥
   - Apuestas activas
   - Historial de apuestas
   - Lista de participantes

3. **Extraer usuarios** 👥
   - Identificará todos los nombres únicos
   - Mostrará cuántos usuarios se crearán

4. **Confirmar migración** ⚠️
   - Te pedirá confirmación antes de continuar
   - Puedes cancelar en este punto

5. **Crear usuarios** 🔨
   - Creará un usuario por cada nombre único
   - Username: nombre en minúsculas sin espacios
   - Full name: nombre original

6. **Migrar apuestas** 🔄
   - Apuestas activas → status = 'active'
   - Historial → status = 'closed'
   - Creará participaciones automáticamente

7. **Mostrar resumen** 📊
   - Total de usuarios migrados
   - Total de apuestas migradas
   - Apuestas activas vs finalizadas

### Ejemplo de salida

```
============================================================
🚀 MIGRACIÓN FIREBASE → SQLITE
============================================================
✅ Conectado a Firebase
✅ Conectado a SQLite: tortilla_apuestas_dev.db

📥 Obteniendo datos de Firebase...
  ✓ Apuestas: 15
  ✓ Historial: 23
  ✓ Participantes: 8

👥 Usuarios únicos encontrados: 8

⚠️  Se migrarán 38 apuestas desde Firebase.
¿Continuar? (sí/no): sí

🔨 Creando usuarios...
  ✓ Usuarios creados: 8
  ✓ Usuarios mapeados: 8

🔄 Migrando apuestas...
  ✓ Apuestas activas migradas: 15
  ✓ Historial migrado: 23
  ✓ Total migrado: 38

============================================================
📊 RESUMEN DE MIGRACIÓN
============================================================
  Usuarios en SQLite: 8
  Apuestas totales: 38
    → Activas: 15
    → Finalizadas: 23
  Participaciones: 112
============================================================

✅ Migración completada exitosamente!

💡 Próximos pasos:
  1. Verifica los datos en http://localhost:3000
  2. Haz login con cualquiera de los usuarios migrados
  3. Si todo está correcto, puedes desactivar Firebase
```

---

## ✅ Verificar datos migrados

### 1. Iniciar servidores

```bash
# Terminal 1 - Backend
cd backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
python3 serve.py
```

### 2. Acceder a la aplicación

Abre http://localhost:3000 en tu navegador.

### 3. Verificar usuarios

```bash
cd backend
sqlite3 tortilla_apuestas_dev.db "SELECT id, username, full_name FROM users;"
```

### 4. Verificar apuestas

```bash
sqlite3 tortilla_apuestas_dev.db "SELECT id, title, status FROM bets LIMIT 10;"
```

### 5. Login y comprobación

1. Haz login con tu nombre de usuario (en minúsculas, sin espacios)
2. La contraseña por defecto es: `tortilla123`
3. Verifica que:
   - ✅ Ves tus apuestas activas
   - ✅ El historial muestra apuestas finalizadas
   - ✅ Los participantes son correctos
   - ✅ Las estadísticas son correctas

---

## 🚨 Solución de problemas

### Error: "firebase-admin not installed"

```bash
pip install firebase-admin
```

### Error: "No se encuentra el archivo"

Verifica que el archivo de credenciales esté en la ubicación correcta:

```bash
ls -la backend/firebase-credentials.json
```

### Error: "Permission denied"

El archivo de credenciales no tiene permisos de lectura:

```bash
chmod 644 backend/firebase-credentials.json
```

### Error: "Failed to parse service account"

El archivo JSON de credenciales está corrupto o es incorrecto:
1. Descarga nuevamente las credenciales desde Firebase Console
2. Asegúrate de descargar la clave de **Service Account**, no la configuración web

### Las apuestas no tienen opciones

El proyecto Firebase original no tenía opciones explícitas. El script:
- Crea opciones genéricas para apuestas activas
- Para historial con ganador, crea: "Gana [nombre]" por cada participante

Puedes editar las opciones manualmente después de la migración.

### Contraseñas de usuarios

Todos los usuarios migrados tienen la contraseña por defecto: `tortilla123`

Cada usuario debe cambiarla al iniciar sesión por primera vez.

---

## 📁 Estructura de datos migrada

### Firebase → SQLite

| Firebase | SQLite | Notas |
|----------|--------|-------|
| `apuestas.titulo` | `bets.title` | Directo |
| `apuestas.descripcion` | `bets.description` | Directo |
| `apuestas.estado` | `bets.status` | `activa` → `active`, `finalizada` → `closed` |
| `apuestas.participantes[]` | `bet_participants` | Array → tabla relacionada |
| `apuestas.ganador` | `bets.winning_option` | Mapeado a opción |
| `apuestas.tortillas` | `bets.tortillas_count` | Directo |
| `apuestas.resultado` | `bets.notes` | Directo |
| `participants.name` | `users.username` + `users.full_name` | Normalizado |

---

## 🔄 ¿Necesitas re-migrar?

Si algo salió mal:

1. Limpia los datos:
   ```bash
   cd backend
   python3 clean_test_data.py
   ```

2. Ejecuta la migración otra vez:
   ```bash
   python3 migrate_from_firebase.py firebase-credentials.json
   ```

---

## 📞 Soporte

Si tienes problemas durante la migración:

1. Revisa los logs del script
2. Verifica las credenciales de Firebase
3. Comprueba que la base de datos SQLite no esté corrupta
4. Intenta limpiar y re-migrar

---

## ✨ Después de la migración

Una vez verificado que todo funciona correctamente:

1. ✅ **Backup de Firebase** (opcional)
   - Exporta los datos desde Firestore
   - Guárdalos por seguridad

2. ✅ **Desactivar Firebase** (opcional)
   - Si ya no lo necesitas, puedes desactivar el proyecto
   - Esto evitará cargos futuros

3. ✅ **Configurar backups locales**
   - Crea backups periódicos de `tortilla_apuestas_dev.db`
   - Considera usar git para versionado

4. ✅ **Actualizar usuarios**
   - Recuérdales cambiar sus contraseñas
   - Envía las nuevas instrucciones de acceso

---

**¡Migración completada!** 🎉

Tu aplicación ahora funciona completamente en tu servidor privado, sin depender de Firebase.
