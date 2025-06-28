# Usa una imagen base de Python (3.12 es compatible con tu proyecto)
FROM python:3.12-slim
WORKDIR /app

# Instala Poetry
RUN pip install poetry

# Configura Poetry para no crear entorno virtual (ya estamos en contenedor)
RUN poetry config virtualenvs.create false

# Copia archivos de configuración de Poetry
COPY pyproject.toml poetry.lock ./

# Instala dependencias
RUN poetry install --only=main --no-dev

# Copia el código de la aplicación
COPY . .

# El comando para arrancar la aplicación
# Cloud Run asigna el puerto dinámicamente via variable de entorno PORT
CMD ["python", "main.py"]
