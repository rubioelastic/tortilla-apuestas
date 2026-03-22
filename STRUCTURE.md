# 📋 ESTRUCTURA FINAL DEL PROYECTO

Aquí está la estructura completa de TortillApuestas configurada para tu servidor privado.

```
tortilla-apuestas/
│
├── 📁 backend/                    ← Backend Python con FastAPI
│   ├── Dockerfile                 (Contenedor API)
│   ├── main.py                    (🚀 API principal - 500+ líneas)
│   ├── models.py                  (🗄️ Modelos de BD)
│   ├── schemas.py                 (✅ Validación de datos)
│   ├── database.py                (🔌 Conexión PostgreSQL)
│   ├── auth.py                    (🔐 JWT + Seguridad)
│   └── requirements.txt            (📦 Dependencias Python)
│
├── 📁 frontend/                   ← Frontend HTML + JS
│   ├── index.html                 (💅 App web completa)
│   └── manifest.json              (📱 PWA config)
│
├── 🐳 DOCKER & DEPLOYMENT
│   ├── docker-compose.yml         (🎼 Orquestación de servicios)
│   ├── nginx.conf                 (🌐 Configuración Nginx)
│   ├── init.sh                    (🚀 Script rápido setup)
│   ├── stop.sh                    (🛑 Script parada)
│   └── verify.py                  (✅ Verificación sistema)
│
├── ⚙️ CONFIGURACIÓN
│   ├── .env.example               (📝 Template variables)
│   └── .env.development           (🔧 Para desarrollo local)
│
├── 📚 DOCUMENTACIÓN
│   ├── QUICKSTART.md              (⚡ 5 minutos setup)
│   ├── DEPLOYMENT.md              (🚀 Guía completa production)
│   ├── ARCHITECTURE.md            (🏗️ Decisiones técnicas)
│   ├── README-SERVER.md           (📖 Guía proyecto)
│   └── STRUCTURE.md               (Este archivo)
│
└── 📁 Frontend Histórico/         ← Versiones anteriores
    ├── index.html                 (Original)
    ├── index-whatsapp.html        (Con WhatsApp)
    └── ...
```

---

## 🎯 ARCHIVOS CLAVE A TENER EN CUENTA

### 🔴 CRÍTICOS (no tocar a menos que sepas qué haces)
- ✋ `docker-compose.yml` - Orquestación
- ✋ `backend/main.py` - API backend
- ✋ `backend/models.py` - Estructura BD

### 🟡 IMPORTANTES (pueden necesitar ajustes)
- ⚙️ `.env` - Contraseñas y configuración
- ⚙️ `frontend/index.html` - Interfaz usuario
- ⚙️ `nginx.conf` - Routing web

### 🟢 DOCUMENTACIÓN (lectura recomendada)
- 📖 `QUICKSTART.md` - Comienza aquí
- 📖 `DEPLOYMENT.md` - Para producción
- 📖 `ARCHITECTURE.md` - Entender la arquitectura

---

## 🚀 CÓMO EMPEZAR (en tu servidor)

### Opción A: Rápido (5 minutos)
```bash
chmod +x init.sh
./init.sh
```

### Opción B: Manual (para entender)
```bash
cp .env.example .env
nano .env                    # Editar valores
docker-compose build
docker-compose up -d
docker-compose logs -f api   # Ver si funciona
```

### Opción C: Verificar primero
```bash
python3 verify.py           # Chequeo de requisitos
```

---

## 📊 TECNOLOGÍAS UTILIZADAS

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Frontend** | HTML + Vanilla JS | - |
| **API** | FastAPI | 0.109.0 |
| **Servidor API** | Uvicorn | 0.27.0 |
| **ORM** | SQLAlchemy | 2.0.25 |
| **Base de Datos** | PostgreSQL | 16 |
| **Web Server** | Nginx | Alpine |
| **Contenedorización** | Docker | 20.10+ |
| **Orquestación** | Docker Compose | 2.0+ |
| **Reverse Proxy** | Nginx Proxy Manager | (externo) |
| **SSL** | Let's Encrypt | (vía NPM) |

---

## 🔐 SEGURIDAD IMPLEMENTADA

```
┌─ Frontend (HTML/JS)
│  └─ Corre en navegador
│     └─ Envía peticiones a /api/*
│
├─ SSL/HTTPS (Let's Encrypt)
│  └─ Gestionado por Nginx Proxy Manager
│     └─ Certificado automático
│
├─ API (FastAPI)
│  ├─ Valida con Pydantic
│  ├─ Verifica JWT
│  ├─ CORS configurado
│  └─ Rate limiting posible
│
├─ Autenticación
│  ├─ Usuarios registrados con email
│  ├─ Contraseñas hasheadas (bcrypt)
│  └─ JWT tokens 30-día de expiración
│
└─ Base de Datos (PostgreSQL)
   ├─ Acceso solo desde Docker network
   ├─ Puerto 5432 no expuesto
   ├─ Requiere contraseña
   └─ Datos persistentes en volumen
```

---

## 🌊 FLUJO DE DATOS

```
1. Usuario abre: https://tortilla.rubiocloud.duckdns.org
                            ↓
2. Nginx Proxy Manager recibe HTTPS
                            ↓
3. Redirige a http://localhost:3000
                            ↓
4. Nginx Frontend sirve HTML + JS
                            ↓
5. JS carga en navegador
                            ↓
6. Usuario hace login/registro
                            ↓
7. JS envía a /api/auth/login
                            ↓
8. API FastAPI valida contraseña
                            ↓
9. Devuelve JWT token
                            ↓
10. JS guarda en localStorage
                            ↓
11. Próximos requests incluyen token
                            ↓
12. API verifica JWT válido
                            ↓
13. Consulta PostgreSQL
                            ↓
14. Retorna JSON
                            ↓
15. JS actualiza interfaz
```

---

## 📈 ESTADÍSTICAS DEL PROYECTO

| Métrica | Cantidad |
|---------|----------|
| Líneas de código Python | ~500+ |
| Endpoints de API | 15+ |
| Modelos de BD | 3 |
| Líneas de configuración | ~200 |
| Documentación | 5 guías |
| Dependencias externas | 10 |

---

## 🔄 FLUJO DE DEPLOYMENT

```
Tu Computadora
    ↓
Git Push
    ↓
GitHub (opcional)
    ↓
Tu Servidor Linux
    ↓
Docker Compose
    ├── Descarga imágenes
    ├── Crea red interna
    ├── Inicia PostgreSQL
    ├── Inicia FastAPI (backend)
    ├── Inicia Nginx (frontend)
    └── Crea volumen persistente
    
    ↓
Docker network (172.20.0.0/16)
    ├── API → BD: localhost:5432
    ├── Frontend → API: localhost:8000
    └── Browser → Frontend: puerto 3000
    
    ↓
Nginx Proxy Manager (externo)
    ├── Recibe: tortilla.rubiocloud.duckdns.org
    └── Redirige a: localhost:3000
    
    ↓
Internet
    ↓
Usuario final: https://tortilla.rubiocloud.duckdns.org
```

---

## 🛠️ COMANDOS MÁS UTILIZADOS

```bash
# Iniciar
./init.sh

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f api

# Reiniciar
docker-compose restart

# Parar
./stop.sh

# Acceder BD
docker exec -it tortilla-db psql -U postgres -d tortilla_apuestas

# Backup automático
docker exec tortilla-db pg_dump -U postgres -d tortilla_apuestas > backup.sql

# Reconstruir después de cambios
docker-compose up -d --build

# Limpieza
docker system prune
```

---

## ✨ LO QUE PUEDES HACER AHORA

✅ **Crear apuestas** entre amigos  
✅ **Registrarse/Login** con email y contraseña  
✅ **Ver ranking** de ganadores  
✅ **Unirse a apuestas** de otros usuarios  
✅ **Todo sincronizado** en base de datos privada  
✅ **Sin Firebase**, **Sin Google**, **Sin dependencias externas**  
✅ **100% tuyo**, corriendo en tu servidor privado  

---

## 📞 PRÓXIMOS PASOS

1. **Leer QUICKSTART.md** - 2 minutos
2. **Ejecutar init.sh** - 5 minutos
3. **Abrir en navegador** - http://localhost:3000
4. **Conectar con NPM** - última cosa
5. **¡Usar la app!** - 🎉

---

**¿Preguntas o problemas? Revisa:**
- `DEPLOYMENT.md` - Para issues de deploy
- `ARCHITECTURE.md` - Para entender cómo funciona
- API Docs: `http://localhost:8000/docs` - Para endpoints

---

**¡Bienvenido a TortillApuestas en tu servidor privado! 🌶️🔥**
