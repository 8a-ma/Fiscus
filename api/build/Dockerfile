FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Establece un directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt ./

# Instala las dependencias de Python como lo hacías originalmente
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ .

# Expone el puerto 8000 donde se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación

CMD ["gunicorn", \
     "-k","gevent", \
     "--worker-connections","1000", \
     "--workers","4", \
     "--timeout","120", \
     "--graceful-timeout","10", \
     "--keep-alive","1", \
     "--max-requests","200", \
     "--max-requests-jitter","20", \
     "--access-logfile","-", \
     "--error-logfile","-", \
     "--log-level","info", \
     "-b","0.0.0.0:8000", \
     "api:app"]
