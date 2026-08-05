# Usamos una imagen oficial de Python ligera y moderna
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para compilar si hiciera falta
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos primero los requirements para aprovechar el sistema de caché de capas de Docker
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código fuente del proyecto al contenedor
COPY . .

# Exponemos el puerto donde corre FastAPI
EXPOSE 8000

# Comando por defecto para iniciar la aplicación con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]