# 📖 ARQUITECTURA Y TECNOLOGÍAS

## 🏗️ Decisiones Técnicas Realizadas

### Backend: FastAPI (Python)
**Por qué:**
- ✅ Perfecto para APIs REST modernas
- ✅ Validación automática con Pydantic
- ✅ Documentación autogenerada (Swagger)
- ✅ Rápido y escalable
- ✅ Fácil de aprender y mantener

**Alternativas consideradas:**
- Node.js/Express: Más complejo, menos tipo seguro
- Django: Overkill para este proyecto
- Go: Curva de aprendizaje más pronunciada

### BD: PostgreSQL
**Por qué:**
- ✅ Relacional (perfecta para apuestas)
- ✅ Gratuita y confiable
- ✅ Funciona bien con Docker
- ✅ Súper mantenible

### Frontend: HTML + Vanilla JS
**Por qué:**
- ✅ Sin dependencias complejas
- ✅ Funciona perfecto en PWA
- ✅ Bajo overhead de recursos
- ✅ Deploy simple

**Vs:**
- React/Vue: Overkill para esta app
- Svelte: Bueno, pero más lento para desembarcar

### Orquestación: Docker + Docker Compose
**Por qué:**
- ✅ Aislamiento perfecto (como tu arquitectura actual)
- ✅ Reproducible en cualquier servidor
- ✅ Fácil de respaldar
- ✅ Escalable

---

## 🔐 Seguridad Implementada

### 1. Autenticación JWT
```
Token = Header.Payload.Signature
Vence en 30 días automáticamente
```

### 2. Contraseñas Hasheadas
```
bcrypt ha iteraciones
10 años a prueba de fuerza bruta
```

### 3. BD Aislada
- Solo accesible desde Docker network
- Puerto 5432 no expuesto
- Contraseña requerida

### 4. CORS Configurado
- Solo dominios autorizados pueden llamar API
- Previene ataques cross-site

### 5. HTTPS/SSL
- Let's Encrypt (automático via NPM)
- Todos los datos encriptados en tránsito

---

## 📊 Estructura de Datos

### Tabla: `users`
```sql
id              INTEGER PRIMARY KEY
username        VARCHAR UNIQUE
email           VARCHAR UNIQUE
hashed_password VARCHAR
display_name    VARCHAR
phone           VARCHAR (para WhatsApp)
created_at      TIMESTAMP
is_active       BOOLEAN
```

### Tabla: `bets`
```sql
id              INTEGER PRIMARY KEY
title           VARCHAR
description     VARCHAR
creator_id      FOREIGN KEY -> users
status          VARCHAR (open, closed, completed)
created_at      TIMESTAMP
closed_at       TIMESTAMP
completed_at    TIMESTAMP
winner_id       FOREIGN KEY -> users
notes           VARCHAR
```

### Tabla: `bet_participants`
```sql
id              INTEGER PRIMARY KEY
bet_id          FOREIGN KEY -> bets
user_id         FOREIGN KEY -> users
number          INTEGER (número elegido)
joined_at       TIMESTAMP
```

---

## 🔄 Flujo de Requests

```
User Browser
     ↓
HTTPS Request
     ↓
Nginx Proxy Manager (SSL/Reverse Proxy)
     ↓
Nginx Frontend (Puerto 3000)
     ↓
HTML Sirve + JS ejecuta
     ↓
JS hace petición /api/...
     ↓
API FastAPI (Puerto 8000)
     ↓
Valida con Pydantic
     ↓
Verifica JWT
     ↓
Consulta PostgreSQL
     ↓
Respuesta JSON
     ↓
JS actualiza DOM
```

---

## 📈 Escalabilidad Posible

### Ahora (Simple)
```
1 servidor → 1 API → 1 BD
```

### Futuro (Escalado)
```
Load Balancer
├── API Server 1
├── API Server 2
└── API Server 3
     ↓
DB Master
├── DB Replica 1
└── DB Replica 2

Redis Cache
```

---

## 🚀 Performance Esperado

- API response: < 100ms
- BD queries: < 50ms
- Frontend render: < 500ms
- Usuarios concurrentes: 50-100

Con optimizaciones:
- Caché en Redis
- Compresión Gzip
- CDN para assets
- Load balancing

---

## 📔 Dependencias Python

| Paquete | Versión | Uso |
|---------|---------|-----|
| fastapi | 0.109.0 | Framework API |
| uvicorn | 0.27.0 | Servidor ASGI |
| sqlalchemy | 2.0.25 | ORM BD |
| psycopg2 | 2.9.9 | Driver PostgreSQL |
| pydantic | 2.5.3 | Validación |
| python-jose | 3.3.0 | JWT tokens |
| passlib | 1.7.4 | Hash contraseñas |

---

## 💭 Decisiones de Diseño

### 1. Por qué no usar Firebase?
- ❌ Datos en servidores de Google
- ❌ No es privado
- ❌ Costo en escala

### 2. Por qué no usar un CMS como WordPress?
- ❌ Overkill
- ❌ Menos rendimiento
- ❌ Seguridad más compleja

### 3. Por qué JWT en lugar de sessions?
- ✅ Stateless (más escalable)
- ✅ Funciona bien con APIs
- ✅ Mobile-friendly
- ✅ Expira automáticamente

### 4. Por qué Pydantic para validación?
- ✅ Type hints (mejor que manual)
- ✅ Error messages automáticos
- ✅ Documentación autogenerada

---

## 🔮 Funcionalidades Futuras Fáciles de Agregar

```python
# Ej: Agregar campo en Bet
class Bet(Base):
    __tablename__ = "bets"
    ...
    imagen_url = Column(String(500), nullable=True)  # ← Nueva línea
    
# FastAPI automáticamente lo incluye en /docs
```

---

## 📚 Recursos Útiles

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy tutorial](https://docs.sqlalchemy.org/)
- [PostgreSQL manual](https://www.postgresql.org/docs/)
- [Docker best practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 🎓 Conceptos Aprendidos

Con esta arquitectura, entiendes:
- ✅ APIs REST modernas
- ✅ Autenticación con JWT
- ✅ Bases de datos relacionales
- ✅ Docker & microservicios
- ✅ Seguridad web
- ✅ Deploy en producción
