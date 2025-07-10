# 📊 Integrar TortillApuestas con Google Sheets

## ¿Por qué Google Sheets?
- **Datos compartidos**: Todos los dispositivos ven las mismas apuestas
- **Sincronización automática**: Los cambios se reflejan en tiempo real
- **Acceso desde cualquier lugar**: Puedes ver/editar desde cualquier dispositivo
- **Backup automático**: Google guarda todo automáticamente
- **Gratuito**: No cuesta nada

## Paso 1: Crear Google Sheet
1. Ve a [sheets.google.com](https://sheets.google.com)
2. Crea una nueva hoja de cálculo
3. Nómbrala "TortillApuestas-Datos"
4. Crea estas pestañas:
   - **Apuestas** (para apuestas activas)
   - **Historial** (para apuestas finalizadas)

### Estructura de la pestaña "Apuestas":
```
A1: ID | B1: Titulo | C1: Descripcion | D1: Participantes | E1: Fecha | F1: Estado | G1: Ganador | H1: Resultado | I1: Tortillas
```

### Estructura de la pestaña "Historial":
```
A1: ID | B1: Titulo | C1: Descripcion | D1: Participantes | E1: Fecha | F1: Ganador | G1: Resultado | H1: Tortillas
```

## Paso 2: Configurar Google Apps Script
1. En tu Google Sheet, ve a **Extensiones > Apps Script**
2. Borra el código por defecto
3. Pega este código:

```javascript
function doGet(e) {
  const action = e.parameter.action;
  
  if (action === 'getApuestas') {
    return getApuestas();
  } else if (action === 'getHistorial') {
    return getHistorial();
  }
  
  return ContentService.createTextOutput('Error: Acción no válida');
}

function doPost(e) {
  try {
    const action = e.parameter.action;
    let data;
    
    // Intentar obtener datos de diferentes formas
    if (e.parameter.data) {
      data = JSON.parse(e.parameter.data);
    } else if (e.postData && e.postData.contents) {
      const postData = JSON.parse(e.postData.contents);
      data = postData.data ? JSON.parse(postData.data) : postData;
    }
    
    Logger.log('Action: ' + action);
    Logger.log('Data: ' + JSON.stringify(data));
    
    if (action === 'addApuesta') {
      return addApuesta(data);
    } else if (action === 'updateApuesta') {
      return updateApuesta(data);
    } else if (action === 'moveToHistorial') {
      return moveToHistorial(data);
    } else if (action === 'deleteApuesta') {
      return deleteApuesta(data);
    }
    
    return ContentService.createTextOutput('Error: Acción no válida - ' + action);
  } catch (error) {
    Logger.log('Error en doPost: ' + error.toString());
    return ContentService.createTextOutput('Error: ' + error.toString());
  }
}

function getApuestas() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Apuestas');
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const rows = data.slice(1);
  
  const apuestas = rows.map(row => {
    const obj = {};
    headers.forEach((header, index) => {
      obj[header.toLowerCase()] = row[index];
    });
    return obj;
  });
  
  return ContentService.createTextOutput(JSON.stringify(apuestas))
    .setMimeType(ContentService.MimeType.JSON);
}

function getHistorial() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Historial');
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const rows = data.slice(1);
  
  const historial = rows.map(row => {
    const obj = {};
    headers.forEach((header, index) => {
      obj[header.toLowerCase()] = row[index];
    });
    return obj;
  });
  
  return ContentService.createTextOutput(JSON.stringify(historial))
    .setMimeType(ContentService.MimeType.JSON);
}

function addApuesta(apuesta) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Apuestas');
  sheet.appendRow([
    apuesta.id,
    apuesta.titulo,
    apuesta.descripcion,
    apuesta.participantes.join(', '),
    apuesta.fecha,
    apuesta.estado,
    apuesta.ganador || '',
    apuesta.resultado || '',
    apuesta.tortillas || ''
  ]);
  
  return ContentService.createTextOutput('Apuesta añadida correctamente');
}

function updateApuesta(apuesta) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Apuestas');
  const data = sheet.getDataRange().getValues();
  
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] == apuesta.id) {
      sheet.getRange(i + 1, 1, 1, 9).setValues([[
        apuesta.id,
        apuesta.titulo,
        apuesta.descripcion,
        apuesta.participantes.join(', '),
        apuesta.fecha,
        apuesta.estado,
        apuesta.ganador || '',
        apuesta.resultado || '',
        apuesta.tortillas || ''
      ]]);
      break;
    }
  }
  
  return ContentService.createTextOutput('Apuesta actualizada correctamente');
}

function moveToHistorial(apuesta) {
  // Añadir al historial
  const historialSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Historial');
  historialSheet.appendRow([
    apuesta.id,
    apuesta.titulo,
    apuesta.descripcion,
    apuesta.participantes.join(', '),
    apuesta.fecha,
    apuesta.ganador,
    apuesta.resultado,
    apuesta.tortillas
  ]);
  
  return ContentService.createTextOutput('Apuesta movida al historial');
}

function deleteApuesta(data) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Apuestas');
  const dataRange = sheet.getDataRange().getValues();
  
  for (let i = 1; i < dataRange.length; i++) {
    if (dataRange[i][0] == data.id) {
      sheet.deleteRow(i + 1);
      break;
    }
  }
  
  return ContentService.createTextOutput('Apuesta eliminada correctamente');
}
```

4. Guarda el proyecto con el nombre "TortillApuestas-API"
5. Ve a **Implementar > Nueva implementación**
6. Selecciona tipo: **Aplicación web**
7. Ejecutar como: **Yo**
8. Acceso: **Cualquier persona**
9. Haz clic en **Implementar**
10. **¡IMPORTANTE!** Copia la URL que te da (algo como: `https://script.google.com/macros/s/ABC123.../exec`)


La implementación se ha actualizado correctamente.
Versión 2 del 10 jul 2025, 15:55
ID de implementación
AKfycby_qgx7r2R-kPvWwckNst5PGdZ7V14FQ2exevZQlNAY4p3PlOW3uLi6mbgbfcNKYp0h5g
Aplicación web
URL
https://script.google.com/macros/s/AKfycby_qgx7r2R-kPvWwckNst5PGdZ7V14FQ2exevZQlNAY4p3PlOW3uLi6mbgbfcNKYp0h5g/exec





## Paso 3: Actualizar tu aplicación HTML

Ahora necesito crear una versión de tu `index.html` que use Google Sheets en lugar de localStorage.

¿Quieres que:
1. **Reemplace completamente** localStorage por Google Sheets
2. **Mantenga ambos** (localStorage como backup y Google Sheets como principal)
3. **Añada un botón** para sincronizar entre localStorage y Google Sheets

## Ventajas de Google Sheets:
✅ **Datos compartidos** entre todos los dispositivos
✅ **Sincronización automática**
✅ **Backup en la nube**
✅ **Acceso desde cualquier lugar**
✅ **Edición manual** si es necesario

## Desventajas:
❌ **Requiere conexión a internet**
❌ **Configuración inicial más compleja**
❌ **Dependes de Google**

## Próximos pasos:
1. Configura el Google Sheet y Apps Script
2. Dame la URL de tu script
3. Te creo la versión actualizada del HTML
4. ¡Tendrás datos sincronizados entre todos los dispositivos!

¿Qué opción prefieres para la integración?
