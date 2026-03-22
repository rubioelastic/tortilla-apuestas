# 🌶️ TortillApuestas - Servidor Privado

**La app de apuestas entre amigos** alojada en tu servidor privado con Docker.

---

## ⚡ Quick Start

```bash
# 1. Permisos en script
chmod +x init.sh

# 2. Ejecutar inicialización
./init.sh

# 3. Editar .env con tus valores
nano .env

# 4. Abrir en navegador
# http://localhost:3000
```

---

## 🏗️ Arquitectura

```
nginx (frontend) ← Nginx Proxy Manager ← Internet
       ↓
Docker Network
├── Frontend (Nginx + HTML/JS)  :3000
├── API (FastAPI + Python)      :8000
└── DB (PostgreSQL)             :5432

All Encrypted with HTTPS via NPM
```

---

## 📦 Servicios Incluidos

| Servicio | Tecnología | Puerto | Función |
|----------|-----------|--------|---------|
| **Frontend** | Nginx | 3000 | Interfaz web |
| **API** | FastAPI (Python) | 8000 | Backend REST |
| **Database** | PostgreSQL | 5432 | Almacenamiento |

---

## 🚀 Desplegar en Producción

**Ver [DEPLOYMENT.md](DEPLOYMENT.md)** para instrucciones completas de cómo:
- Configurar en tu servidor Linux
- Conectar con Nginx Proxy Manager
- Obtener SSL/HTTPS automático
- Hacer backups de datos

---

## 📚 API Endpoints

Documentación interactiva en: `http://localhost:8000/docs`

### Autenticación
```
POST   /api/auth/register       # Registrarse
POST   /api/auth/login          # Login
GET    /api/auth/me             # Datos usuario
```

### Apuestas
```
POST   /api/bets                # Crear apuesta
GET    /api/bets                # Listar apuestas
GET    /api/bets/{id}           # Obtener apuesta
PUT    /api/bets/{id}           # Actualizar
DELETE /api/bets/{id}           # Eliminar
POST   /api/bets/{id}/join      # Unirse
DELETE /api/bets/{id}/leave     # Abandonar
```

### Estadísticas
```
GET    /api/ranking             # Ranking global
GET    /api/users/{id}/stats    # Stats de usuario
```

---

## 📁 Estructura del Proyecto

```
tortilla-apuestas/
├── backend/
│   ├── main.py                 # API FastAPI
│   ├── models.py               # Modelos BD (SQLAlchemy)
│   ├── schemas.py              # Validación (Pydantic)
│   ├── database.py             # Conexión PostgreSQL
│   ├── auth.py                 # Autenticación JWT
│   ├── requirements.txt         # Dependencias Python
│   └── Dockerfile              # Contenedor API
│
├── frontend/
│   ├── index.html              # App web
│   ├── manifest.json           # PWA config
│
├── docker-compose.yml          # Orquestación
├── nginx.conf                  # Config Nginx
├── .env.example                # Variables template
├── init.sh                      # Script setup
├── DEPLOYMENT.md               # Guía completa
└── README.md                   # Este archivo
```

---

## 🔐 Características de Seguridad

✅ **Autenticación JWT**
- Tokens expiran en 30 días
- Contraseñas hasheadas con bcrypt

✅ **Base de datos segura**
- Acceso solo desde red interna Docker
- Puerto 5432 no expuesto a internet

✅ **API protegida**
- CORS configurado
- Rate limiting posible

✅ **HTTPS/SSL**
- Certificados Let's Encrypt automáticos
- Gestionado por Nginx Proxy Manager

---

## 🛠️ Comandos Útiles

```bash
# Ver estado
docker-compose ps

# Logs en tiempo real
docker-compose logs -f api

# Reiniciar servicios
docker-compose restart

# Parar (sin perder datos)
docker-compose down

# Acceder BD
docker exec -it tortilla-db psql -U postgres

# Reconstruir después de cambios
docker-compose up -d --build
```

---

## 🗄️ Base de Datos

**PostgreSQL 16** con esquema incluido:

- **users** - Usuarios registrados
- **bets** - Apuestas creadas
- **bet_participants** - Participación en apuestas

Los datos se guardan en volumen persistente `tortilla_db_data`.

---

## 🔄 Actualizaciones

```bash
cd tortilla-apuestas
git pull                          # Actualizar código
docker-compose up -d --build      # Reconstruir
# Los datos en BD se mantienen
```

---

## 📊 Monitoreo

```bash
# Ver estadísticas en tiempo real
docker stats

# Revisar espacio
df -h /

# Ver logs históricos
docker-compose logs
```

---

## 🚨 Troubleshooting

### No puedo acceder
```bash
docker-compose ps  # Verificar que todo esté running
curl http://localhost:3000  # Test local
```

### Errores API
```bash
docker-compose logs api  # Ver errores
docker-compose restart api
```

### BD no conecta
```bash
docker-compose logs db
docker-compose restart db
sleep 10
```

---

## 📞 Soporte & Mejoras

Para contribuir o reportar problemas:
1. Revisa los logs: `docker-compose logs`
2. Verifica la documentación en DEPLOYMENT.md
3. Consulta la API docs: `http://localhost:8000/docs`

---

## 🎯 Roadmap de Funcionalidades

- [ ] Notificaciones por WhatsApp
- [ ] Estadísticas avanzadas
- [ ] Exportar datos (CSV/JSON)
- [ ] Grupos privados de apuestas
- [ ] Fotos de apuestas
- [ ] App móvil nativa

---

## 📄 Licencia

Este proyecto es libre para usar en tu servidor privado.

---

**¡Que disfrutes TortillApuestas en tu servidor privado! 🌶️🎉**
