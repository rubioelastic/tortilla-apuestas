# 🚀 Deploy con Docker en Servidor - TortillApuestas

Guía actualizada para desplegar TortillApuestas con **Docker + SQLite** en tu servidor.

---

## 📋 Pre-requisitos en el Servidor

Tu servidor debe tener:
- ✅ Docker instalado (versión 20.10+)
- ✅ Docker Compose instalado
- ✅ Acceso SSH
- ✅ Puertos 80/443 abiertos (o usar Nginx Proxy Manager)

### Verificar en el servidor:

```bash
ssh usuario@tortilla.rubiocloud.duckdns.org
docker --version
docker-compose --version
```

Si no tienes Docker instalado:

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo bash get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Instalar Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

---

## 🚀 Pasos de Despliegue

### 1️⃣ Transferir archivos al servidor

**Opción A: Usando Git (recomendado)**

```bash
# En el servidor
cd ~
git clone https://github.com/tu-usuario/tortilla-apuestas.git
cd tortilla-apuestas
```

**Opción B: Usando rsync (desde tu Mac)**

```bash
# Desde tu Mac
cd ~/Documents/tortilla-apuestas

# Transferir archivos (excluye node_modules, .git, etc)
rsync -avz --exclude '.git' \
           --exclude '__pycache__' \
           --exclude '*.pyc' \
           --exclude 'venv' \
           --exclude '.DS_Store' \
           . usuario@tortilla.rubiocloud.duckdns.org:~/tortilla-apuestas/
```

**Opción C: Clonar y copiar BD manualmente**

```bash
# 1. En el servidor: clonar el repo
ssh usuario@tortilla.rubiocloud.duckdns.org
cd ~
git clone https://github.com/tu-usuario/tortilla-apuestas.git
exit

# 2. Desde tu Mac: copiar la BD con tus datos
scp ~/Documents/tortilla-apuestas/backend/tortilla_apuestas_dev.db \
    usuario@tortilla.rubiocloud.duckdns.org:~/tortilla-apuestas/backend/
```

---

### 2️⃣ Configurar variables de entorno

```bash
# En el servidor
cd ~/tortilla-apuestas

# Copiar template
cp .env.example .env

# Generar SECRET_KEY segura
openssl rand -hex 32

# Editar .env
nano .env
```

**Contenido del .env:**

```env
# Base de datos SQLite (ya está configurada automáticamente)
DB_PATH=/app/data/tortilla_apuestas_dev.db

# Seguridad - IMPORTANTE: usa la clave generada arriba
SECRET_KEY=TU_CLAVE_GENERADA_CON_OPENSSL

# Entorno
ENVIRONMENT=production

# URL del frontend (tu dominio)
FRONTEND_URL=https://tortilla.rubiocloud.duckdns.org
```

---

### 3️⃣ Construir e iniciar contenedores

```bash
# Construir imágenes
docker-compose build

# Iniciar en segundo plano
docker-compose up -d

# Verificar que todo está corriendo
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f
```

**Deberías ver:**

```
NAME                 STATUS
tortilla-api         Up (healthy)
tortilla-frontend    Up (healthy)
```

---

### 4️⃣ Copiar base de datos con tus datos reales

```bash
# Copiar tu BD actual al contenedor
docker cp backend/tortilla_apuestas_dev.db tortilla-api:/app/data/tortilla_apuestas_dev.db

# Reiniciar backend para cargar los datos
docker-compose restart api

# Verificar logs
docker-compose logs api
```

---

### 5️⃣ Configurar Nginx Proxy Manager (opcional pero recomendado)

Si usas Nginx Proxy Manager para HTTPS:

1. **Agregar Proxy Host:**
   - Domain: `tortilla.rubiocloud.duckdns.org`
   - Forward Host: `tortilla-frontend` (o IP del servidor)
   - Forward Port: `3000`
   - ✅ Block Common Exploits
   - ✅ Websockets Support

2. **SSL:**
   - ✅ Force SSL
   - ✅ HTTP/2 Support
   - Certificado: Let's Encrypt (automático)

3. **Custom Nginx Configuration** (añadir en la pestaña Advanced):

```nginx
# Proxy para API
location /api {
    proxy_pass http://tortilla-api:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /docs {
    proxy_pass http://tortilla-api:8000;
}

location /openapi.json {
    proxy_pass http://tortilla-api:8000;
}
```

**Alternativa sin Nginx Proxy Manager:**

Exponer directamente el puerto 80:

```yaml
# En docker-compose.yml, cambiar:
ports:
  - "80:3000"  # En lugar de 3000:3000
```

---

## 📊 Verificar que funciona

```bash
# Probar API directamente
curl http://localhost:8000/docs

# Probar frontend
curl http://localhost:3000

# Desde internet (con tu dominio)
https://tortilla.rubiocloud.duckdns.org
```

---

## 🔧 Gestión y Mantenimiento

### Ver logs

```bash
# Logs del backend
docker-compose logs -f api

# Logs del frontend
docker-compose logs -f frontend

# Logs de todo
docker-compose logs -f
```

### Reiniciar servicios

```bash
# Reiniciar todo
docker-compose restart

# Reiniciar solo API
docker-compose restart api

# Reiniciar todo desde cero
docker-compose down
docker-compose up -d
```

### Actualizar la aplicación

```bash
# 1. Hacer backup de la BD
docker cp tortilla-api:/app/data/tortilla_apuestas_dev.db ./backup-$(date +%Y%m%d).db

# 2. Actualizar código (si usas Git)
git pull origin main

# 3. Reconstruir imágenes
docker-compose build

# 4. Reiniciar con nuevo código
docker-compose up -d
```

### Backup de la base de datos

```bash
# Backup manual
docker cp tortilla-api:/app/data/tortilla_apuestas_dev.db ./backup-$(date +%Y%m%d).db

# Script de backup automático (crear como cron job)
#!/bin/bash
BACKUP_DIR="/home/usuario/backups/tortilla"
mkdir -p $BACKUP_DIR
docker cp tortilla-api:/app/data/tortilla_apuestas_dev.db \
    $BACKUP_DIR/tortilla-$(date +%Y%m%d-%H%M%S).db

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "tortilla-*.db" -mtime +7 -delete
```

**Configurar backup diario:**

```bash
# Editar crontab
crontab -e

# Añadir (backup diario a las 3 AM)
0 3 * * * /home/usuario/backup-tortilla.sh
```

### Restaurar desde backup

```bash
# Detener contenedor
docker-compose stop api

# Restaurar BD
docker cp backup-20260223.db tortilla-api:/app/data/tortilla_apuestas_dev.db

# Reiniciar
docker-compose start api
```

---

## 🐛 Troubleshooting

### El frontend no carga

```bash
# Verificar logs
docker-compose logs frontend

# Verificar que Nginx está sirviendo archivos
docker exec tortilla-frontend ls -la /usr/share/nginx/html/
```

### API devuelve 401 Unauthorized

- ✅ Verifica que SECRET_KEY en `.env` es la misma
- ✅ Limpia localStorage del navegador y vuelve a hacer login
- ✅ Verifica logs: `docker-compose logs api`

### No se conecta a la base de datos

```bash
# Verificar que la BD existe
docker exec tortilla-api ls -la /app/data/

# Ver logs de la API
docker-compose logs api | grep -i database
```

### Puertos ocupados

```bash
# Ver qué está usando el puerto
sudo lsof -i :8000
sudo lsof -i :3000

# Matar proceso que lo está usando
sudo kill -9 <PID>
```

### Errores de permisos

```bash
# Dar permisos al volumen de datos
docker-compose down
sudo chown -R $USER:$USER ./backend/
docker-compose up -d
```

---

## 🔒 Seguridad en Producción

### 1. Cambiar contraseñas por defecto

```bash
# En el servidor, acceder a la BD
docker exec -it tortilla-api sqlite3 /app/data/tortilla_apuestas_dev.db

# Ver usuarios
SELECT username FROM users;

# (Los usuarios deben cambiar su contraseña desde la app)
```

### 2. Firewall

```bash
# Solo permitir SSH, HTTP y HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Verificar
sudo ufw status
```

### 3. Actualizaciones automáticas de Docker

```bash
# Watchtower: actualiza contenedores automáticamente
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --cleanup \
  --interval 86400
```

---

## 📈 Monitoreo (Opcional)

### Añadir Portainer para gestión visual

```bash
docker volume create portainer_data

docker run -d \
  -p 9000:9000 \
  --name portainer \
  --restart always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

Accede en: `http://tu-servidor:9000`

---

## ✅ Checklist Final

- [ ] Docker y Docker Compose instalados en servidor
- [ ] Código transferido al servidor
- [ ] `.env` configurado con SECRET_KEY única
- [ ] `docker-compose up -d` ejecutado sin errores
- [ ] Base de datos copiada al contenedor
- [ ] Contenedores en estado "healthy": `docker-compose ps`
- [ ] API responde: `curl http://localhost:8000/docs`
- [ ] Frontend carga: `curl http://localhost:3000`
- [ ] Nginx Proxy Manager configurado (si aplica)
- [ ] HTTPS funcionando con Let's Encrypt
- [ ] Login funciona desde internet
- [ ] Backup automático configurado

---

## 🎉 ¡Listo!

Tu aplicación debería estar corriendo en:

**🌐 https://tortilla.rubiocloud.duckdns.org**

---

## 📞 Soporte

Si encuentras problemas:

1. Revisa logs: `docker-compose logs -f`
2. Verifica estado: `docker-compose ps`
3. Reinicia servicios: `docker-compose restart`
4. Consulta este documento

**Comandos de diagnóstico rápido:**

```bash
# Estado general
docker-compose ps
docker stats --no-stream

# Logs de todo
docker-compose logs --tail=50

# Test de conectividad
curl -I http://localhost:8000/docs
curl -I http://localhost:3000
```
