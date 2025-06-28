# Usa una imagen base de Python (3.12 es compatible con tu proyecto)
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de tu proyecto al contenedor
COPY . .

# El comando para arrancar la aplicación
# Cloud Run asigna el puerto dinámicamente via variable de entorno PORT
CMD ["python", "main.py"]
