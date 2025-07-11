# 🔥 Configurar Firebase para TortillApuestas

## ¿Por qué Firebase?
- ✅ **Datos compartidos** entre todos los dispositivos (móvil, ordenador, tablet)
- ✅ **Sincronización en tiempo real** - Los cambios se ven instantáneamente
- ✅ **Sin problemas de CORS** - Funciona desde cualquier navegador
- ✅ **Gratuito** - Plan gratuito muy generoso
- ✅ **Fácil de configurar** - Solo 5 minutos

## Paso 1: Crear Proyecto Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com)
2. Haz clic en **"Crear un proyecto"**
3. Nombre del proyecto: `tortilla-apuestas` (o el que prefieras)
4. **Desactiva** Google Analytics (no lo necesitamos)
5. Haz clic en **"Crear proyecto"**

## Paso 2: Configurar Firestore Database

1. En el panel izquierdo, haz clic en **"Firestore Database"**
2. Haz clic en **"Crear base de datos"**
3. Selecciona **"Comenzar en modo de prueba"** (permite lectura/escritura por 30 días)
4. Elige la ubicación más cercana (ej: `europe-west3` para España)
5. Haz clic en **"Listo"**

## Paso 3: Obtener Configuración Web

1. En el panel principal, haz clic en el ícono **"Web"** (`</>`)
2. Nombre de la app: `TortillApuestas`
3. **NO** marques "Firebase Hosting"
4. Haz clic en **"Registrar app"**
5. **COPIA** el objeto `firebaseConfig` que aparece:

```javascript
const firebaseConfig = {
  apiKey: "tu-api-key-aqui",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto-id",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789",
  appId: "tu-app-id"
};
```

## Paso 4: Actualizar el Código

1. Abre el archivo `index-firebase.html`
2. Busca esta sección (línea ~15):

```javascript
// Configuración de Firebase (usando base de datos demo)
const firebaseConfig = {
  apiKey: "demo-key",
  authDomain: "demo-project.firebaseapp.com",
  projectId: "demo-project",
  storageBucket: "demo-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "demo-app-id"
};
```

3. **REEMPLAZA** con tu configuración real:

```javascript
// Configuración de Firebase (TU CONFIGURACIÓN REAL)
const firebaseConfig = {
  apiKey: "tu-api-key-aqui",
  authDomain: "tu-proyecto.firebaseapp.com",
  projectId: "tu-proyecto-id",
  storageBucket: "tu-proyecto.appspot.com",
  messagingSenderId: "123456789",
  appId: "tu-app-id"
};
```

## Paso 5: Configurar Reglas de Seguridad

1. En Firebase Console, ve a **"Firestore Database"**
2. Haz clic en la pestaña **"Reglas"**
3. Reemplaza las reglas con esto:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Permitir lectura y escritura a todos por ahora
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

4. Haz clic en **"Publicar"**

⚠️ **Nota de Seguridad:** Estas reglas permiten acceso completo. Para producción, deberías implementar autenticación.

## Paso 6: ¡Probar la Aplicación!

1. Abre `index-firebase.html` en tu navegador
2. El modal de configuración ya no debería aparecer
3. El indicador debería mostrar "Sincronizado" en verde
4. ¡Crea una apuesta y ábrela en otro dispositivo!

## 🎉 ¡Listo!

Ahora tu aplicación TortillApuestas:
- ✅ Comparte datos entre **todos tus dispositivos**
- ✅ Se **sincroniza en tiempo real**
- ✅ **Guarda todo** en la nube
- ✅ Funciona desde **cualquier navegador**

## Solución de Problemas

### Error: "Firebase project not found"
- Verifica que el `projectId` en la configuración sea correcto
- Asegúrate de que el proyecto existe en Firebase Console

### Error: "Permission denied"
- Verifica que las reglas de Firestore permitan lectura/escritura
- Asegúrate de estar en "modo de prueba"

### No se sincronizan los datos
- Verifica tu conexión a internet
- Abre la consola del navegador para ver errores
- Asegúrate de que Firestore esté habilitado

### Datos no aparecen en otros dispositivos
- Espera unos segundos (la sincronización puede tardar)
- Refresca la página en el otro dispositivo
- Verifica que ambos dispositivos usen la misma configuración Firebase

## Próximos Pasos (Opcional)

### Añadir Autenticación
Para mayor seguridad, puedes añadir autenticación de usuarios:
1. En Firebase Console, ve a **"Authentication"**
2. Habilita proveedores (Google, Email, etc.)
3. Actualiza las reglas de Firestore para requerir autenticación

### Hosting en Firebase
Para compartir fácilmente la app:
1. Instala Firebase CLI: `npm install -g firebase-tools`
2. En tu carpeta del proyecto: `firebase init hosting`
3. Despliega: `firebase deploy`

¡Disfruta de tu aplicación de apuestas con tortilla! 🥚🎉
