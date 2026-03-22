# 🌐 Configuración de Nginx Proxy Manager para TortillApuestas

## 📋 Requisitos Previos
- ✅ Aplicación desplegada en el servidor (192.168.1.115)
- ✅ Nginx Proxy Manager corriendo en puerto 8181
- ✅ Dominio configurado: tortilla.rubiocloud.duckdns.org
- ✅ Puertos 80 y 443 abiertos en el router

---

## 🔑 Paso 1: Acceder a Nginx Proxy Manager

1. **Abre tu navegador** y ve a:
   ```
   http://192.168.1.115:8181
   ```

2. **Credenciales por defecto** (primera vez):
   ```
   Email: admin@example.com
   Password: changeme
   ```

3. **Cambia las credenciales** cuando te lo solicite por seguridad.

---

## 🌟 Paso 2: Configurar Proxy Host para FRONTEND

### A. Crear el Proxy Host

1. Haz clic en **"Proxy Hosts"** en el menú superior
2. Haz clic en el botón **"Add Proxy Host"**

### B. Pestaña "Details"

Rellena los siguientes campos:

```
Domain Names: tortilla.rubiocloud.duckdns.org
Scheme: http
Forward Hostname/IP: tortilla-frontend
Forward Port: 3000

☑️ Cache Assets
☑️ Block Common Exploits
☑️ Websockets Support
```

**Importante:** Usa `tortilla-frontend` como hostname porque están en la misma red Docker.

### C. Pestaña "SSL"

```
☑️ Request a new SSL Certificate with Let's Encrypt

Email Address for Let's Encrypt: [tu email real]

☑️ Force SSL
☑️ HTTP/2 Support
☑️ HSTS Enabled
☑️ HSTS Subdomains

☑️ I Agree to the Let's Encrypt Terms of Service
```

3. Haz clic en **"Save"**

⏳ **Espera 30-60 segundos** mientras Let's Encrypt genera el certificado SSL.

✅ Verás un mensaje verde de éxito cuando esté listo.

---

## 🔧 Paso 3: Configurar Proxy Host para BACKEND API

### A. Crear el Segundo Proxy Host

1. Haz clic en **"Add Proxy Host"** nuevamente

### B. Pestaña "Details"

```
Domain Names: api.tortilla.rubiocloud.duckdns.org
Scheme: http
Forward Hostname/IP: tortilla-api
Forward Port: 8000

☑️ Block Common Exploits
☑️ Websockets Support
```

### C. Pestaña "SSL"

```
☑️ Request a new SSL Certificate with Let's Encrypt

Email Address for Let's Encrypt: [tu email real]

☑️ Force SSL
☑️ HTTP/2 Support
☑️ HSTS Enabled

☑️ I Agree to the Let's Encrypt Terms of Service
```

3. Haz clic en **"Save"**

⏳ **Espera** mientras Let's Encrypt genera el certificado.

---

## 🔍 Paso 4: Verificar la Configuración

### Verificar los Proxy Hosts creados

Deberías ver 2 proxies en la lista:

| Domain | Scheme | Status | SSL |
|--------|--------|--------|-----|
| tortilla.rubiocloud.duckdns.org | https | ✅ Online | 🔒 Let's Encrypt |
| api.tortilla.rubiocloud.duckdns.org | https | ✅ Online | 🔒 Let's Encrypt |

---

## 🧪 Paso 5: Probar la Aplicación

### Frontend
Abre en tu navegador:
```
https://tortilla.rubiocloud.duckdns.org
```

Deberías ver la página principal de TortillApuestas.

### Backend API
Prueba el endpoint de salud:
```
https://api.tortilla.rubiocloud.duckdns.org/health
```

Deberías ver:
```json
{"status":"✅ API en línea"}
```

### Documentación API
Accede a la documentación interactiva:
```
https://api.tortilla.rubiocloud.duckdns.org/docs
```

---

## ⚠️ Solución de Problemas

### Problema: "502 Bad Gateway"

**Causa:** El contenedor no está accesible.

**Solución:**
```bash
ssh securedatauser@192.168.1.115
cd ~/tortilla-apuestas
docker restart tortilla-api tortilla-frontend
docker ps
```

### Problema: "SSL Certificate Error"

**Causa:** Let's Encrypt no pudo verificar el dominio.

**Solución:**
1. Verifica que tu dominio DuckDNS esté actualizado con tu IP pública
2. Verifica que los puertos 80 y 443 estén abiertos en tu router
3. Intenta regenerar el certificado:
   - Edita el Proxy Host
   - Pestaña SSL → "Force Renew"

### Problema: "Cannot connect to backend"

**Causa:** CORS o red Docker.

**Solución:**
```bash
ssh securedatauser@192.168.1.115
docker network inspect tortilla-apuestas_tortilla-network
```

Verifica que `tortilla-api`, `tortilla-frontend` y `nginx-proxy-manager-app-1` estén en redes conectadas.

---

## 📱 Paso 6: Configurar como PWA (Opcional)

1. Abre la aplicación en tu móvil
2. En Chrome/Safari: Menu → "Añadir a pantalla de inicio"
3. La app se instalará como aplicación nativa

---

## 🔄 Actualizar la Aplicación

Para desplegar cambios en el futuro:

```bash
# En tu Mac:
cd ~/Documents/tortilla-apuestas

# Copiar archivos al servidor
rsync -avz --exclude '.git' --exclude '__pycache__' . securedatauser@192.168.1.115:~/tortilla-apuestas/

# Reiniciar contenedores
ssh securedatauser@192.168.1.115 "cd ~/tortilla-apuestas && docker compose restart"
```

---

## 🎉 ¡Listo!

Tu aplicación TortillApuestas está ahora accesible desde internet con:

✅ SSL/HTTPS habilitado  
✅ Backend API protegido  
✅ Frontend responsive  
✅ Base de datos persistente  
✅ Logs centralizados  

**URLs de Producción:**
- 🌐 Frontend: https://tortilla.rubiocloud.duckdns.org
- 🔧 API: https://api.tortilla.rubiocloud.duckdns.org
- 📚 Docs: https://api.tortilla.rubiocloud.duckdns.org/docs

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs: `docker logs tortilla-api`
2. Verifica el status: `docker ps`
3. Revisa la configuración de red: `docker network ls`
