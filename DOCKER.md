# 🐋 Guía de Docker - TortillApuestas

## 📋 Requisitos previos

1. **Instalar Docker Desktop**:
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Descarga e instala Docker Desktop para Mac (Apple Silicon o Intel)
   - Verifica instalación: `docker --version` y `docker-compose --version`

## 🚀 Iniciar con Docker

### 1️⃣ Primera vez - Configuración inicial

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. (Opcional) Editar .env con tu SECRET_KEY personalizada
# nano .env

# 3. Construir y levantar contenedores
docker-compose up -d --build
```

### 2️⃣ Verificar que todo funciona

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Verificar que los contenedores están corriendo
docker-compose ps

# Deberías ver:
# - tortilla-api (backend) - Estado: Up
# - tortilla-frontend (nginx) - Estado: Up
```

### 3️⃣ Acceder a la aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

### 4️⃣ Migrar tu base de datos actual a Docker

Si ya tienes datos en `backend/tortilla_apuestas_dev.db`:

```bash
# Opción A: Copiar la BD antes de construir (recomendado)
# La BD se copiará automáticamente al construir la imagen

# Opción B: Copiar la BD a un contenedor ya corriendo
docker cp backend/tortilla_apuestas_dev.db tortilla-api:/app/data/tortilla_apuestas_dev.db
docker-compose restart api
```

## 🛠️ Comandos útiles

### Gestión básica

```bash
# Iniciar todos los servicios
docker-compose up -d

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ BORRA LA BASE DE DATOS)
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart api
docker-compose restart frontend

# Ver logs de un servicio
docker-compose logs -f api
docker-compose logs -f frontend
```

### Reconstruir tras cambios en código

```bash
# Reconstruir la imagen del backend
docker-compose up -d --build api

# Reconstruir todo desde cero
docker-compose down
docker-compose up -d --build
```

### Acceso al contenedor

```bash
# Entrar al contenedor del backend
docker exec -it tortilla-api bash

# Ver archivos de la base de datos
docker exec -it tortilla-api ls -lh /app/data/

# Hacer backup de la base de datos
docker cp tortilla-api:/app/data/tortilla_apuestas_dev.db ./backup-$(date +%Y%m%d).db
```

### Limpiar Docker (liberar espacio)

```bash
# Eliminar contenedores parados
docker container prune

# Eliminar imágenes sin usar
docker image prune -a

# Eliminar volúmenes sin usar
docker volume prune

# Limpieza completa (⚠️ cuidado)
docker system prune -a --volumes
```

## 📦 Estructura de volúmenes

La base de datos SQLite se guarda en un volumen Docker persistente:

```
tortilla_db_data → /app/data/tortilla_apuestas_dev.db
```

Esto significa que **tus datos persisten** aunque detengas o elimines contenedores.

## 🔧 Desarrollo con Docker

Si quieres desarrollar con hot-reload dentro de Docker:

1. Edita `docker-compose.yml`
2. Descomenta la línea:
   ```yaml
   # - ./backend:/app
   ```
3. Reinicia: `docker-compose restart api`

Ahora los cambios en `backend/` se reflejan automáticamente.

## ❓ Troubleshooting

### Error: "port is already allocated"

```bash
# Matar procesos en puertos 3000 y 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Reintentar
docker-compose up -d
```

### Error: "no such file or directory: tortilla_apuestas_dev.db"

```bash
# Copiar tu BD existente
docker cp backend/tortilla_apuestas_dev.db tortilla-api:/app/data/
docker-compose restart api
```

### Frontend no carga

```bash
# Verificar logs
docker-compose logs frontend

# Reiniciar Nginx
docker-compose restart frontend
```

### Backend no responde

```bash
# Ver logs del backend
docker-compose logs api

# Reiniciar backend
docker-compose restart api

# Si persiste, reconstruir
docker-compose up -d --build api
```

## 🔒 Seguridad para producción

Antes de llevar a producción:

1. **Cambiar SECRET_KEY** en `.env`:
   ```bash
   openssl rand -hex 32
   ```

2. **Comentar el volumen de desarrollo** en `docker-compose.yml`:
   ```yaml
   # volumes:
   #   - ./backend:/app
   ```

3. **Configurar HTTPS** con Nginx Proxy Manager o Certbot

4. **Restricciones de red**: Exponer solo puerto 80/443 externamente

## 📚 Recursos adicionales

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/docker/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

**¿Necesitas ayuda?** Abre un issue en el proyecto 🚀
