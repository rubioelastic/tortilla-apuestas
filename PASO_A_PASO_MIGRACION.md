# 🚀 Migración Firebase → SQLite - Paso a Paso

## ✅ Prerequisito: Base de datos limpia
Ya completado ✓ (0 apuestas, 0 usuarios, 0 participantes)

---

## 📝 PASO 1: Obtener credenciales de Firebase

### 1.1 Abrir Firebase Console
```
https://console.firebase.google.com/
```

### 1.2 Iniciar sesión
- Usa tu cuenta de Google (la que tiene acceso al proyecto)

### 1.3 Seleccionar proyecto
- Click en **"tortilla-apuestas"**

### 1.4 Ir a configuración
- Click en el **icono de engranaje ⚙️** (arriba a la izquierda)
- Click en **"Project Settings"** (Configuración del proyecto)

### 1.5 Abrir Service Accounts
- En la parte superior, busca la pestaña **"Service accounts"**
- Click en esa pestaña

### 1.6 Generar clave
- En la sección "Firebase Admin SDK"
- Verás código de Python como ejemplo
- Debajo hay un botón: **"Generate new private key"**
- Click en ese botón

### 1.7 Confirmar descarga
- Aparecerá un diálogo de advertencia
- Click en **"Generate key"**
- Se descargará un archivo JSON (algo como `tortilla-apuestas-firebase-adminsdk-xxxxx-1234567890.json`)

### 1.8 Mover el archivo
```bash
# Abre una terminal y ejecuta:
mv ~/Downloads/tortilla-apuestas-*.json ~/Documents/tortilla-apuestas/backend/firebase-credentials.json
```

**✅ Checkpoint**: Verifica que el archivo existe:
```bash
ls -la ~/Documents/tortilla-apuestas/backend/firebase-credentials.json
```
Deberías ver algo como: `-rw-r--r--  1 rubioja  staff  2431 Feb 22 ...`

---

## 📦 PASO 2: Instalar dependencias de Python

### 2.1 Abrir terminal en la carpeta backend
```bash
cd ~/Documents/tortilla-apuestas/backend
```

### 2.2 Instalar firebase-admin
```bash
pip install firebase-admin
```

**✅ Checkpoint**: Deberías ver algo como:
```
Collecting firebase-admin
  Downloading firebase_admin-6.x.x-py3-none-any.whl
Installing collected packages: ...
Successfully installed firebase-admin-6.x.x ...
```

---

## 🔄 PASO 3: Ejecutar migración

### 3.1 Ejecutar el script
```bash
python3 migrate_from_firebase.py firebase-credentials.json
```

### 3.2 Revisar la información
El script mostrará:
```
============================================================
🚀 MIGRACIÓN FIREBASE → SQLITE
============================================================
✅ Conectado a Firebase
✅ Conectado a SQLite: tortilla_apuestas_dev.db

📥 Obteniendo datos de Firebase...
  ✓ Apuestas: X
  ✓ Historial: Y
  ✓ Participantes: Z

👥 Usuarios únicos encontrados: N
```

### 3.3 Confirmar migración
Te preguntará:
```
⚠️  Se migrarán XX apuestas desde Firebase.
¿Continuar? (sí/no):
```

**Escribe:** `sí` y presiona Enter

### 3.4 Esperar a que termine
Verás:
```
🔨 Creando usuarios...
  ✓ Usuarios creados: N
  ✓ Usuarios mapeados: N

🔄 Migrando apuestas...
  ✓ Apuestas activas migradas: X
  ✓ Historial migrado: Y
  ✓ Total migrado: Z

============================================================
📊 RESUMEN DE MIGRACIÓN
============================================================
  Usuarios en SQLite: N
  Apuestas totales: Z
    → Activas: X
    → Finalizadas: Y
  Participaciones: P
============================================================

✅ Migración completada exitosamente!
```

---

## ✅ PASO 4: Verificar migración

### 4.1 Verificar base de datos
```bash
sqlite3 tortilla_apuestas_dev.db "SELECT COUNT(*) FROM users;"
sqlite3 tortilla_apuestas_dev.db "SELECT COUNT(*) FROM bets;"
```

Debería mostrar números > 0

### 4.2 Ver usuarios migrados
```bash
sqlite3 tortilla_apuestas_dev.db "SELECT username, full_name FROM users;"
```

Deberías ver la lista de usuarios de tus apuestas

### 4.3 Ver algunas apuestas
```bash
sqlite3 tortilla_apuestas_dev.db "SELECT id, title, status FROM bets LIMIT 5;"
```

---

## 🌐 PASO 5: Probar en el navegador

### 5.1 Iniciar servidores (si no están corriendo)

**Terminal 1 - Backend:**
```bash
cd ~/Documents/tortilla-apuestas/backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd ~/Documents/tortilla-apuestas/frontend
python3 serve.py
```

### 5.2 Abrir navegador
```
http://localhost:3000
```

### 5.3 Hacer login
- Usuario: nombre de alguno de tus participantes (en minúsculas, sin espacios)
  - Ejemplo: Si tienes "Juan Pérez" → usuario es `juan_perez`
- Contraseña: `tortilla123` (contraseña por defecto)

### 5.4 Verificar datos
- ✅ Tab "Apuestas Activas": Deberías ver tus apuestas activas
- ✅ Tab "Historial": Deberías ver apuestas finalizadas
- ✅ Panel derecho: Estadísticas correctas
- ✅ Ranking: Usuarios con sus tortillas

---

## ⚠️ Solución de problemas

### Error: "firebase-admin not installed"
```bash
pip install firebase-admin
```

### Error: "No such file"
El archivo de credenciales no está en la ubicación correcta:
```bash
ls -la backend/firebase-credentials.json
```
Si no existe, repite el PASO 1.8

### Error: "Permission denied"
```bash
chmod 644 backend/firebase-credentials.json
python3 migrate_from_firebase.py firebase-credentials.json
```

### Error: "Failed to parse service account"
El archivo JSON está corrupto. Repite el PASO 1 completo.

### Los usuarios no pueden hacer login
La contraseña por defecto es: `tortilla123`

Cada usuario puede cambiarla después de su primer login.

### Las opciones de las apuestas son genéricas
Firebase no tenía opciones explícitas, por eso el script crea:
- Apuestas activas: "Opción A", "Opción B", etc.
- Historial con ganador: "Gana [nombre]"

Puedes editarlas manualmente después.

---

## 🎉 ¡Migración completada!

Tu aplicación ahora funciona 100% local sin Firebase.

### Próximos pasos recomendados:

1. **Backup de la base de datos**
   ```bash
   cp backend/tortilla_apuestas_dev.db backend/tortilla_apuestas_backup_$(date +%Y%m%d).db
   ```

2. **Avisar a usuarios**
   - Nueva URL: http://tu-ip:3000
   - Usuario: su nombre sin espacios en minúsculas
   - Contraseña inicial: tortilla123
   - Pídeles que cambien su contraseña

3. **Configurar backups automáticos**
   - Usa cron para hacer backups diarios de la base de datos

4. **(Opcional) Desactivar Firebase**
   - Si ya no lo necesitas, puedes desactivar el proyecto para evitar costos

---

## 📞 ¿Necesitas ayuda?

Si algo no funciona:
1. Lee el mensaje de error completo
2. Busca en la sección "Solución de problemas"
3. Revisa los logs del script
4. Verifica que ejecutaste todos los pasos en orden

**Archivo con más detalles técnicos:** [MIGRACION.md](MIGRACION.md)
