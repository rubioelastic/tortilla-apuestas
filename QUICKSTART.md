# 🚀 QUICK START - Instrucciones Rápidas

## ⚡ En tu servidor en 5 minutos

```bash
# 1. SSH a tu servidor
ssh usuario@tu-servidor

# 2. Clonar repo (o copiar archivos)
cd /home/proyectos/
git clone <url-del-repo> tortilla-apuestas
cd tortilla-apuestas

# 3. Permisos
chmod +x init.sh

# 4. Ejecutar
./init.sh

# 5. Configurar .env
nano .env
# Cambiar DB_PASSWORD y SECRET_KEY

# 6. Guardar y LISTO
# Todo inicia automáticamente
```

## ✅ Verificar que funciona

```bash
# Debería ver 3 servicios "Up"
docker-compose ps

# Test API
curl http://localhost:8000/health

# Abrir en navegador
# http://localhost:3000
```

## 🔗 Conectar con NPM (última paso)

1. Ir a panel NPM: `http://tu-servidor:81`
2. Proxy Hosts → Add
3. Domain: `tortilla.rubiocloud.duckdns.org`
4. Forward to: `localhost:3000`
5. SSL: Let's Encrypt automático
6. ✅ Save

## 💾 Datos persistentes

Los datos en PostgreSQL se guardan en:
```
/var/lib/docker/volumes/tortilla_db_data/
```

Nunca se pierden aunque reinicies contenedores.

## 🚨 Si algo falla

```bash
# Ver logs
docker-compose logs api

# Reiniciar todo
docker-compose restart

# Recrear desde cero (cuidado!)
docker-compose down -v
docker-compose up -d
```

---

**¡Eso es todo! Tu servidor privado está listo. 🎉**
