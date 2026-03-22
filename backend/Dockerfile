FROM python:3.11.10-slim

WORKDIR /app

# Instalar dependencias (gcc para compilar, curl para healthcheck)
RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*

# Crear directorio para la base de datos
RUN mkdir -p /app/data

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Si existe la BD en el directorio actual, copiarla a /app/data
RUN if [ -f tortilla_apuestas_dev.db ]; then \
        cp tortilla_apuestas_dev.db /app/data/tortilla_apuestas_dev.db; \
        echo "✅ Base de datos copiada"; \
    else \
        echo "⚠️ No se encontró base de datos, se creará una nueva"; \
    fi

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
