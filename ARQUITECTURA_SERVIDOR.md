# 🖥️ ARQUITECTURA DEL SERVIDOR - Documentación Completa

**Fecha de documentación:** 15 de marzo de 2026  
**Proyecto actual:** TortillApuestas  
**Propósito:** Información completa para integrar nuevos proyectos Docker en el mismo servidor

---

## 📍 INFORMACIÓN DEL SERVIDOR

```yaml
IP del servidor: 192.168.1.115
Usuario SSH: securedatauser
Puerto SSH: 22
Sistema Operativo: Linux
Gestor de contenedores: Docker + Docker Compose
```

### Acceso SSH
```bash
ssh securedatauser@192.168.1.115
# o con puerto explícito:
ssh -p 22 securedatauser@192.168.1.115
```

---

## 🐋 STACK TECNOLÓGICO

### Software Instalado
- **Docker** (versión 20.10+)
- **Docker Compose** (versión 2.0+)
- **Nginx Proxy Manager** (NPM) - Gestión de proxy reverso y SSL
- **DuckDNS** - Servicio DNS dinámico

### Dominio Principal
```
Dominio base: rubiocloud.duckdns.org
Subdominios activos:
  - tortilla.rubiocloud.duckdns.org (TortillApuestas)
  - api.tortilla.rubiocloud.duckdns.org (API Backend)
```

---

## 🌐 NGINX PROXY MANAGER (NPM)

### Acceso a la Interfaz Web
```
URL: http://192.168.1.115:8181
Puerto: 8181

Credenciales por defecto (primera vez):
  Email: admin@example.com
  Password: changeme
```

### Configuración de Proxy Hosts Actual

#### 1. Frontend TortillApuestas
```yaml
Domain: tortilla.rubiocloud.duckdns.org
Scheme: http
Forward Hostname: tortilla-frontend
Forward Port: 3000

SSL/HTTPS:
  Provider: Let's Encrypt
  Force SSL: ✅ Habilitado
  HTTP/2 Support: ✅ Habilitado
  HSTS Enabled: ✅ Habilitado
  HSTS Subdomains: ✅ Habilitado

Opciones adicionales:
  - Cache Assets: ✅
  - Block Common Exploits: ✅
  - Websockets Support: ✅
```

#### 2. Backend API TortillApuestas (opcional)
```yaml
Domain: api.tortilla.rubiocloud.duckdns.org
Scheme: http
Forward Hostname: tortilla-api
Forward Port: 8000

SSL/HTTPS:
  Provider: Let's Encrypt
  Force SSL: ✅ Habilitado
  HTTP/2 Support: ✅ Habilitado
  HSTS Enabled: ✅ Habilitado

Opciones adicionales:
  - Block Common Exploits: ✅
  - Websockets Support: ✅
```

### Puertos del Sistema
```
Puerto 80   → HTTP (redirige a HTTPS automáticamente)
Puerto 443  → HTTPS (gestionado por NPM con Let's Encrypt)
Puerto 8181 → Nginx Proxy Manager Web UI
```

**⚠️ IMPORTANTE:** Puertos 80 y 443 están abiertos en el router y redirigidos al servidor.

---

## 📦 PROYECTO ACTUAL: TORTILLAPUESTAS

### Ubicación en el Servidor
```bash
Ruta: /home/securedatauser/tortilla-apuestas
```

### Estructura del Proyecto
```
tortilla-apuestas/
├── backend/                    # Backend FastAPI
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tortilla_apuestas_dev.db (SQLite)
│
├── frontend/                   # Frontend HTML/JS
│   ├── index.html
│   └── manifest.json
│
├── docker-compose.yml          # Orquestación de servicios
├── nginx.conf                  # Config Nginx del frontend
├── nginx-production.conf       # Config alternativa
├── .env                        # Variables de entorno
└── deploy-to-server.sh         # Script de deploy automático
```

### Docker Compose Configuration

```yaml
version: '3.9'

services:
  # ══════════════════════════════════════════════════════
  # BACKEND API
  # ══════════════════════════════════════════════════════
  api:
    build: ./backend
    container_name: tortilla-api
    restart: unless-stopped
    
    ports:
      - "8000:8000"
    
    volumes:
      - tortilla_db_data:/app/data
    
    networks:
      - tortilla-network
    
    environment:
      - DB_PATH=/app/data/tortilla_apuestas_dev.db
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ══════════════════════════════════════════════════════
  # FRONTEND
  # ══════════════════════════════════════════════════════
  frontend:
    image: nginx:alpine
    container_name: tortilla-frontend
    restart: unless-stopped
    
    ports:
      - "3000:3000"
    
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    
    networks:
      - tortilla-network
    
    depends_on:
      - api

# ══════════════════════════════════════════════════════
# VOLÚMENES
# ══════════════════════════════════════════════════════
volumes:
  tortilla_db_data:
    driver: local

# ══════════════════════════════════════════════════════
# REDES
# ══════════════════════════════════════════════════════
networks:
  tortilla-network:
    driver: bridge
```

### Servicios Docker

#### 1. tortilla-api (Backend)
```yaml
Contenedor: tortilla-api
Imagen: Custom (build desde ./backend/Dockerfile)
Tecnología: FastAPI + Python 3.11+
Puerto expuesto: 8000:8000
Red: tortilla-network

Volúmenes:
  - tortilla_db_data → /app/data (SQLite database)

Health Check:
  - URL: http://localhost:8000/docs
  - Intervalo: 30s
  - Timeout: 10s
  - Retries: 3

Variables de entorno:
  - DB_PATH=/app/data/tortilla_apuestas_dev.db
  - SECRET_KEY (desde .env)
  - ENVIRONMENT=production
```

#### 2. tortilla-frontend (Frontend)
```yaml
Contenedor: tortilla-frontend
Imagen: nginx:alpine
Puerto expuesto: 3000:3000
Red: tortilla-network

Volúmenes:
  - ./frontend → /usr/share/nginx/html (archivos estáticos)
  - ./nginx.conf → /etc/nginx/nginx.conf (configuración)

Dependencias:
  - api (backend debe estar corriendo)
```

---

## 🔌 PUERTOS UTILIZADOS Y DISPONIBLES

### Puertos en Uso
```
Sistema:
  80    → HTTP (NPM - redirige a HTTPS)
  443   → HTTPS (NPM - con SSL Let's Encrypt)
  8181  → Nginx Proxy Manager UI

TortillApuestas:
  3000  → tortilla-frontend (Nginx)
  8000  → tortilla-api (FastAPI)
```

### Puertos Disponibles para Nuevos Proyectos
```
Sugerencias:
  3001, 3002, 3003... → Frontends adicionales
  8001, 8002, 8003... → APIs adicionales
  5432, 5433, 5434... → Bases de datos PostgreSQL
  6379, 6380, 6381... → Redis
  27017, 27018...     → MongoDB
```

**⚠️ Recordatorio:** Siempre verifica puertos libres antes de asignar:
```bash
netstat -tuln | grep LISTEN
# o con docker:
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

---

## 🌐 REDES DOCKER

### Red Actual: tortilla-network
```yaml
Nombre: tortilla-network
Driver: bridge
Tipo: Interna (comunicación entre contenedores)

Contenedores conectados:
  - tortilla-api
  - tortilla-frontend
```

### Comunicación entre Contenedores
Los contenedores en la misma red pueden comunicarse usando sus nombres:
```
Ejemplo desde tortilla-frontend:
  http://tortilla-api:8000/api/...
  
Ejemplo desde tortilla-api:
  http://tortilla-frontend:3000/
```

### Opciones para Nuevos Proyectos

#### Opción A: Red Independiente (Recomendado)
```yaml
# En tu nuevo docker-compose.yml
networks:
  nuevo-proyecto-network:
    driver: bridge
```

#### Opción B: Red Compartida (Si necesitas comunicación entre apps)
```yaml
# En tu nuevo docker-compose.yml
networks:
  default:
    name: tortilla-network
    external: true
```

#### Opción C: Red Híbrida
```yaml
# Conectar a ambas redes
networks:
  nueva-red:
    driver: bridge
  tortilla-network:
    external: true

services:
  mi-servicio:
    networks:
      - nueva-red
      - tortilla-network
```

---

## 💾 VOLÚMENES Y PERSISTENCIA

### Volúmenes Docker Actuales
```
Nombre: tortilla_db_data
Driver: local
Montado en: /app/data (dentro de tortilla-api)
Contenido: tortilla_apuestas_dev.db (SQLite)
```

### Ver Volúmenes en el Servidor
```bash
# Listar todos los volúmenes
docker volume ls

# Inspeccionar volumen específico
docker volume inspect tortilla_db_data

# Ubicación física en el servidor (típicamente):
# /var/lib/docker/volumes/tortilla_db_data/_data/
```

### Backup de Volúmenes
```bash
# Backup de la base de datos
docker cp tortilla-api:/app/data/tortilla_apuestas_dev.db ./backup-$(date +%Y%m%d).db

# Backup de un volumen completo
docker run --rm -v tortilla_db_data:/data -v $(pwd):/backup alpine tar czf /backup/tortilla_db_backup.tar.gz -C /data .
```

---

## 🔒 SEGURIDAD Y CERTIFICADOS SSL

### Certificados SSL (Let's Encrypt)
```yaml
Proveedor: Let's Encrypt
Gestión: Automática via Nginx Proxy Manager
Renovación: Automática (90 días)
Wildcard: No (certificado por subdominio)

Dominios con certificado actual:
  - tortilla.rubiocloud.duckdns.org
  - api.tortilla.rubiocloud.duckdns.org (si configurado)
```

### Headers de Seguridad Configurados
```nginx
# En nginx.conf
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### Variables de Entorno Sensibles
```bash
# Archivo: .env (en la raíz del proyecto)
SECRET_KEY=abc123...  # Token JWT
DB_PASSWORD=...        # Si usas PostgreSQL
ENVIRONMENT=production
```

**⚠️ IMPORTANTE:** Nunca commitear archivos `.env` a Git. Usar `.env.example` como template.

---

## 🚀 WORKFLOW DE DEPLOY

### Deploy Desde Local (Mac) al Servidor

#### Script Automático
```bash
# Desde: /Users/rubioja/Documents/Proyectos/tortilla-apuestas/

# 1. Hacer cambios en el código local
# 2. Ejecutar script de deploy
./deploy-to-server.sh

# El script hace:
# ✅ Verifica conexión SSH
# ✅ Verifica Docker en servidor
# ✅ Transfiere archivos con rsync
# ✅ Configura .env
# ✅ Construye y levanta contenedores
# ✅ Verifica que los servicios estén OK
```

#### Deploy Manual
```bash
# 1. Transferir archivos
rsync -avz --progress \
  --exclude '.git' --exclude '__pycache__' \
  -e "ssh -p 22" \
  ./ securedatauser@192.168.1.115:/home/securedatauser/tortilla-apuestas/

# 2. Conectar al servidor
ssh securedatauser@192.168.1.115

# 3. Ir al directorio
cd /home/securedatauser/tortilla-apuestas

# 4. Construir y levantar
docker-compose down
docker-compose up -d --build

# 5. Verificar
docker-compose ps
docker-compose logs -f
```

---

## 📊 COMANDOS ÚTILES DOCKER

### Gestión de Contenedores
```bash
# Ver contenedores corriendo
docker ps

# Ver todos (incluyendo detenidos)
docker ps -a

# Logs en tiempo real
docker-compose logs -f
docker-compose logs -f api      # Solo backend
docker-compose logs -f frontend # Solo frontend

# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar un servicio
docker-compose restart api

# Reconstruir tras cambios de código
docker-compose up -d --build

# Eliminar todo (incluyendo volúmenes) ⚠️
docker-compose down -v
```

### Inspección y Debug
```bash
# Entrar a un contenedor
docker exec -it tortilla-api bash
docker exec -it tortilla-frontend sh

# Ver recursos usados
docker stats

# Ver redes
docker network ls
docker network inspect tortilla-network

# Ver volúmenes
docker volume ls
docker volume inspect tortilla_db_data

# Copiar archivos desde/hacia contenedor
docker cp tortilla-api:/app/data/db.db ./local-backup.db
docker cp ./local-file.txt tortilla-api:/app/
```

### Limpieza del Sistema
```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune

# Limpiar todo (⚠️ cuidado)
docker system prune -a

# Limpiar volúmenes no usados
docker volume prune
```

---

## 🧩 CONFIGURACIÓN NGINX (Frontend)

### Archivo: nginx.conf

```nginx
# Configuración actual de tortilla-frontend

server {
    listen 3000;
    server_name _;
    
    root /usr/share/nginx/html;
    index index.html;
    
    # Configuraciones importantes:
    client_max_body_size 20M;
    gzip on;
    
    # Servir archivos estáticos
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy al backend
    location /api/ {
        proxy_pass http://tortilla-api:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Endpoints específicos
    location /health {
        proxy_pass http://tortilla-api:8000/health;
    }
    
    location /docs {
        proxy_pass http://tortilla-api:8000/docs;
    }
}
```

---

## 📝 PLANTILLA PARA NUEVO PROYECTO

### Estructura Recomendada
```
nuevo-proyecto/
├── docker-compose.yml
├── .env.example
├── .env
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt (Python)
│   └── ...
└── frontend/
    ├── Dockerfile (opcional)
    └── ...
```

### docker-compose.yml Template
```yaml
version: '3.9'

services:
  # Backend
  nuevo-api:
    build: ./backend
    container_name: nuevo-api
    restart: unless-stopped
    ports:
      - "8001:8001"  # ⚠️ Puerto diferente a TortillApuestas
    volumes:
      - nuevo_data:/app/data
    networks:
      - nuevo-network
    environment:
      - VARIABLE_1=${VAR1}
      - VARIABLE_2=${VAR2}

  # Frontend
  nuevo-frontend:
    image: nginx:alpine
    container_name: nuevo-frontend
    restart: unless-stopped
    ports:
      - "3001:3001"  # ⚠️ Puerto diferente
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - nuevo-network
    depends_on:
      - nuevo-api

volumes:
  nuevo_data:
    driver: local

networks:
  nuevo-network:
    driver: bridge
```

### Configurar en Nginx Proxy Manager
1. Acceder a: `http://192.168.1.115:8181`
2. Ir a "Proxy Hosts" → "Add Proxy Host"
3. Configurar:
   ```
   Domain: nuevo.rubiocloud.duckdns.org
   Forward Hostname: nuevo-frontend
   Forward Port: 3001
   ```
4. Pestaña SSL:
   ```
   ✅ Request new SSL Certificate
   ✅ Force SSL
   ✅ HTTP/2 Support
   ```

---

## 🎯 CHECKLIST PARA NUEVO PROYECTO

### Antes de Empezar
- [ ] Elegir puertos disponibles (frontend y backend)
- [ ] Decidir nombre del proyecto (prefijo para contenedores/volúmenes)
- [ ] Elegir subdominio DuckDNS (ej: `nuevo.rubiocloud.duckdns.org`)
- [ ] Definir si necesita comunicación con TortillApuestas (red compartida)

### Durante el Setup
- [ ] Crear `docker-compose.yml` con nombres únicos en `container_name`
- [ ] Crear archivo `.env` con variables sensibles
- [ ] Configurar `nginx.conf` si es necesario
- [ ] Transferir archivos al servidor en directorio separado
- [ ] Levantar servicios: `docker-compose up -d --build`
- [ ] Verificar logs: `docker-compose logs -f`

### Configuración NPM
- [ ] Crear Proxy Host en NPM
- [ ] Configurar dominio y forward
- [ ] Solicitar certificado SSL Let's Encrypt
- [ ] Verificar que Force SSL está habilitado
- [ ] Probar acceso desde navegador

### Post-Deploy
- [ ] Verificar que la app responde correctamente
- [ ] Configurar health checks en docker-compose
- [ ] Documentar puertos y dominios usados
- [ ] Configurar backups si es necesario

---

## 🆘 TROUBLESHOOTING COMÚN

### Contenedor no arranca
```bash
# Ver logs detallados
docker-compose logs nombre-servicio

# Reconstruir imagen
docker-compose up -d --build nombre-servicio

# Verificar puertos en uso
netstat -tuln | grep PUERTO
docker ps --format "{{.Names}}: {{.Ports}}"
```

### Error de puerto ya en uso
```bash
# Encontrar qué está usando el puerto
sudo lsof -i :PUERTO

# Cambiar el puerto en docker-compose.yml
# ports:
#   - "NUEVO_PUERTO:PUERTO_INTERNO"
```

### No se puede acceder desde el dominio
```bash
# Verificar que NPM está corriendo
docker ps | grep nginx-proxy-manager

# Verificar en logs de NPM
docker logs -f nombre-contenedor-npm

# Verificar que el certificado SSL está activo
# En NPM UI → SSL Certificates
```

### Base de datos perdida
```bash
# Verificar que el volumen existe
docker volume ls | grep nombre-volumen

# Restaurar desde backup
docker cp backup.db nombre-contenedor:/ruta/destino/
docker-compose restart
```

---

## 📞 INFORMACIÓN DE CONTACTO Y RECURSOS

### Recursos del Servidor
```
Servidor IP: 192.168.1.115
Usuario: securedatauser
DuckDNS: rubiocloud.duckdns.org
NPM UI: http://192.168.1.115:8181
```

### URLs Actuales
```
TortillApuestas Frontend: https://tortilla.rubiocloud.duckdns.org
TortillApuestas API: http://192.168.1.115:8000
TortillApuestas Docs: http://192.168.1.115:8000/docs
```

### Documentación Útil
- Docker: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Nginx Proxy Manager: https://nginxproxymanager.com/
- DuckDNS: https://www.duckdns.org/
- Let's Encrypt: https://letsencrypt.org/

---

## 📅 HISTORIAL DE CAMBIOS

| Fecha | Cambio | Responsable |
|-------|--------|-------------|
| 15/03/2026 | Documentación inicial de la arquitectura | Sistema |
| - | - | - |

---

## 🔄 MANTENIMIENTO RECOMENDADO

### Semanal
- [ ] Verificar logs de contenedores: `docker-compose logs --tail=100`
- [ ] Verificar espacio en disco: `df -h`

### Mensual
- [ ] Actualizar imágenes Docker: `docker-compose pull && docker-compose up -d`
- [ ] Limpiar recursos no usados: `docker system prune`
- [ ] Verificar certificados SSL en NPM (renovación automática)

### Trimestral
- [ ] Backup completo de volúmenes Docker
- [ ] Revisar y actualizar esta documentación
- [ ] Verificar actualizaciones de seguridad del sistema

---

**📌 NOTA FINAL:** Este documento debe actualizarse cada vez que se añada un nuevo proyecto o se modifique la infraestructura del servidor.
