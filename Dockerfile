# Usa una imagen base de Python (3.12 es compatible con tu proyecto)
FROM python:3.12-slim
WORKDIR /app

# Copia e instala dependencias mínimas
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

# Copia el código de la aplicación
COPY . .

# El comando para arrancar la aplicación
# Cloud Run asigna el puerto dinámicamente via variable de entorno PORT
CMD ["python", "main.py"]
