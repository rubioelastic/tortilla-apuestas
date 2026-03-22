# 🔄 Cómo actualizar GitHub Pages con la redirección

## Pasos para subir el nuevo index.html a GitHub

### Opción 1: Desde la web de GitHub (Más fácil)

1. **Ir a tu repositorio en GitHub**
   - Entra en: `https://github.com/TU-USUARIO/tortilla-apuestas`

2. **Editar el archivo index.html**
   - Haz clic en el archivo `index.html` en la lista de archivos
   - Haz clic en el icono del lápiz (Edit this file) en la esquina superior derecha
   
3. **Reemplazar el contenido**
   - Selecciona todo el contenido actual (Ctrl+A / Cmd+A)
   - Bórralo
   - Copia y pega el contenido del nuevo `index.html` (el de tu carpeta local)
   
4. **Guardar cambios (Commit)**
   - Baja hasta el final de la página
   - En "Commit changes" escribe: `Agregar redirección a nueva URL`
   - Haz clic en "Commit changes"

5. **¡Listo! 🎉**
   - En 1-2 minutos, tu GitHub Pages estará redirigiendo automáticamente
   - Prueba entrando a `https://TU-USUARIO.github.io/tortilla-apuestas`

---

### Opción 2: Usando Git desde terminal

```bash
cd /Users/rubioja/Documents/Proyectos/tortilla-apuestas

# Agregar el cambio
git add index.html

# Hacer commit
git commit -m "Agregar redirección a nueva URL"

# Subir a GitHub
git push origin main
```

---

## ¿Cómo funciona la redirección?

El nuevo `index.html` tiene **3 métodos de redirección** para máxima compatibilidad:

1. **Meta refresh** (`<meta http-equiv="refresh">`) - Redirección HTML estándar
2. **JavaScript** (`window.location.replace()`) - Redirección JavaScript como backup
3. **Link manual** - Por si los métodos automáticos fallan

Además, mientras se redirige, muestra un mensaje bonito con la tortilla flotante 🥚

---

## Verificar que funciona

1. Ve a tu URL de GitHub Pages: `https://TU-USUARIO.github.io/tortilla-apuestas`
2. Deberías ver el mensaje "¡Nos hemos mudado! 🥚" por un segundo
3. Luego serás redirigido automáticamente a: `https://tortilla.rubiocloud.duckdns.org`

---

## Archivos de respaldo

Por si necesitas recuperar la versión antigua:
- **index-firebase-old.html** - La versión con Firebase (la original)
- **index.html.backup** - Otra copia de seguridad anterior
- **frontend/index.html** - La versión nueva que usa el servidor

---

## Notas importantes

- ✅ Los usuarios que tengan guardada la URL antigua serán redirigidos automáticamente
- ✅ Los marcadores/favoritos seguirán funcionando (redirigen a la nueva URL)
- ✅ La redirección es instantánea (0 segundos)
- ⚠️ El cambio en GitHub Pages puede tardar 1-2 minutos en aplicarse
