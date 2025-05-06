# Usa una imagen liviana de Python
FROM python:3.12-slim

# Instala paquetes necesarios del sistema para psycopg2 y otros
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

# Crea y usa un directorio de trabajo
WORKDIR /app

# Copia todos los archivos al contenedor
COPY . /app/

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 (Render lo usa por defecto)
EXPOSE 8000

# Comando que corre migraciones y levanta Gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn gestorAlum.wsgi:application --bind 0.0.0.0:8000"]
