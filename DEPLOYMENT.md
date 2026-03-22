# 🚀 Deploy de TortillApuestas en tu Servidor Privado

Esta es la **guía completa** para desplegar TortillApuestas en tu servidor con Docker.

---

## 📋 Requisitos Previos

Asegúrate de tener instalado en tu servidor Linux:

```bash
# Docker
docker --version  # Debe ser 20.10+

# Docker Compose
docker-compose --version  # Debe ser 2.0+

# Git (opcional, para clonar el repo)
git --version
```

**¿No tienes Docker instalado?** Ejecuta:

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh && sudo bash get-docker.sh

# Agregar tu usuario al grupo docker (para no usar sudo cada vez)
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🔧 Pasos de Instalación

### Paso 1: Preparar el Directorio

```bash
# Ir a tu carpeta de proyectos Docker
cd /home/tu-usuario/projects/

# Si no tienes el código, clonarlo o copiar los archivos
# Opción A: Con Git
git clone https://github.com/tu-usuario/tortilla-apuestas.git
cd tortilla-apuestas

# Opción B: Copiar archivos manualmente
# Asegúrate de que la estructura sea:
# tortilla-apuestas/
# ├── backend/       (backend Python)
# ├── frontend/      (frontend HTML)
# ├── docker-compose.yml
# ├── nginx.conf
# └── .env.example
```

### Paso 2: Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env

# Editar con valores seguros
nano .env
```

**Contenido recomendado de `.env`:**

```env
# Base de datos
DB_USER=tortilla_user
DB_PASSWORD=TuContraseñaMuySegura12345!
DB_NAME=tortilla_apuestas

# Seguridad - Genera con: openssl rand -hex 32
SECRET_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

ENVIRONMENT=production
FRONTEND_URL=https://tortilla.rubiocloud.duckdns.org
```

### Paso 3: Construir e Iniciar los Contenedores

```bash
# Construir imágenes (solo primera vez o si hay cambios)
docker-compose build

# Iniciar servicios en modo background (-d = daemon)
docker-compose up -d

# Ver que todo está iniciado
docker-compose ps

# Debería mostrar:
# NAME                 STATUS
# tortilla-db          Up 2 minutes (healthy)
# tortilla-api         Up 1 minute (healthy)
# tortilla-frontend    Up 1 minute (healthy)
```

### Paso 4: Verificar que Funciona

```bash
# API está respondiendo
curl http://localhost:8000/health
# Debería mostrar: {"status":"✅ API en línea"}

# Frontend está sirviendo
curl http://localhost:3000/
# Debería mostrar HTML

# Ver logs para ver si hay errores
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f frontend
```

---

## 🌐 Conectar con Nginx Proxy Manager (NPM)

Ahora que tienes TortillApuestas corriendo localmente, **expónlo a internet a través de NPM**:

### 1. Acceder a NPM

```bash
# Tu NPM generalmente está en:
# http://tu-servidor:81/

# O si tienes dominio
# https://npm.rubiocloud.duckdns.org/
```

### 2. Crear Nuevo Host Proxy

1. **Haz clic en "Proxy Hosts"** (menú izquierdo)
2. **Haz clic en "+ Add Proxy Host"** (botón arriba)

### 3. Configuración del Host

Completa estos campos:

| Campo | Valor |
|-------|-------|
| **Domain Names** | `tortilla.rubiocloud.duckdns.org` |
| **Scheme** | `http` |
| **Forward Hostname/IP** | `localhost` |
| **Forward Port** | `3000` |
| **Cache Assets** | ✅ Activado |
| **Block Common Exploits** | ✅ Activado |
| **Websockets Support** | ✅ Activado |

**Haz click en "Save"**

### 4. Configurar SSL/HTTPS

1. Ve a la pestaña **"SSL"** del host que acabas de crear
2. Haz clic en **"Request a new SSL Certificate"**
3. Selecciona **"Let's Encrypt"**
4. Marca ✅ **"Agree to Let's Encrypt terms"**
5. Haz clic en **"Save"**

**Espera 30 segundos...**

✅ ¡En 2-3 minutos tendrás SSL automático!

---

## 📱 Acceso desde Internet

```
🔗 https://tortilla.rubiocloud.duckdns.org
```

¡Ya está accesible desde cualquier dispositivo en el mundo!

---

## 🔍 Comandos Útiles para Gestionar

```bash
# Ver estado de los servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f api

# Parar todos los servicios (sin eliminar datos)
docker-compose down

# Reiniciar (por si algo falla)
docker-compose restart api

# Recrear (si hay cambios en código)
docker-compose up -d --build

# Acceder a la BD directamente
docker exec -it tortilla-db psql -U tortilla_user -d tortilla_apuestas

# Ver espacio de disco usado
docker system df

# Limpiar datos innecesarios (cuidado!)
docker system prune -a
```

---

## 💾 Copias de Seguridad de la BD

### Crear Backup Manual

```bash
# Hacer backup
docker exec tortilla-db pg_dump -U tortilla_user -d tortilla_apuestas > backup.sql

# Restaurar desde backup
cat backup.sql | docker exec -i tortilla-db psql -U tortilla_user -d tortilla_apuestas
```

### Backup Automático (Cron)

```bash
# Editar crontab
crontab -e

# Agregar esta línea (backup diario a las 3 AM)
0 3 * * * docker exec tortilla-db pg_dump -U tortilla_user -d tortilla_apuestas > /home/backups/tortilla-$(date +\%Y\%m\%d).sql
```

---

## 🐛 Solucionar Problemas

### ❌ "No puedo acceder a la app"

```bash
# Verificar que los contenedores están corriendo
docker-compose ps

# Ver logs de errores
docker-compose logs
```

### ❌ "Base de datos no conecta"

```bash
# Reiniciar BD
docker-compose restart db

# Esperar a que esté lista (ver logs)
docker-compose logs db
```

### ❌ "Errores de API"

```bash
# Ver logs detallados
docker-compose logs api

# Reiniciar API
docker-compose restart api
```

### ❌ "SSL no funciona"

```bash
# Verificar que DuckDNS está actualizado
# Ir a https://www.duckdns.org y verificar tu dominio

# En NPM, ir a Settings > DuckDNS
# Actualizar el dominio y esperar 5 minutos
```

---

## 🔐 Seguridad - Checklist

- ✅ Cambiar `SECRET_KEY` en `.env` (usar valores seguros)
- ✅ Cambiar `DB_PASSWORD` (contraseña fuerte)
- ✅ Puerto 5432 (BD) no está expuesto a internet
- ✅ Solo puerto 3000 está detrás de NPM
- ✅ SSL/HTTPS está activado
- ✅ Firewall del servidor está configurado (UFW)

```bash
# Ver firewall (Ubuntu)
sudo ufw status

# Si está activado, permitir puertos necesarios
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (NPM redirect)
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 81/tcp    # NPM admin (cambiar después)
```

---

## 📊 Monitoreo

### Ver uso de recursos

```bash
# CPU, memoria, red de contenedores
docker stats

# Espacio en disco
df -h
du -h /home/tu-usuario/projects/tortilla-apuestas/
```

### Logs persistentes

Los logs están guardados en:
```
/var/lib/docker/containers/*/
```

---

## 🚀 Actualizaciones

Para actualizar el código sin perder datos:

```bash
# Ir al directorio
cd /home/tu-usuario/projects/tortilla-apuestas/

# Descargar cambios (si usas Git)
git pull

# Reconstruir e reiniciar
docker-compose up -d --build

# Los datos en BD se mantienen (volúmenes persistentes)
```

---

## ✨ Próximos Pasos (Opcional)

1. **Configurar dominio propio** en lugar de DuckDNS
2. **Agregar SMTP** para envío de emails
3. **Alertas de monitoreo** (Uptime Kuma)
4. **Rate limiting** en Nginx
5. **2FA** en login

---

## 📞 Soporte

Si algo no funciona:

1. **Revisa los logs**: `docker-compose logs`
2. **Verifica conexión de BD**: `docker-compose logs db`
3. **Prueba ping a localhost**: `curl http://localhost:3000/`

---

**¡Felicidades! 🎉 Ahora tienes TortillApuestas corriendo en tu servidor privado!**
