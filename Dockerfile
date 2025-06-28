# Usa una imagen base de Python (3.12 es compatible con tu proyecto)
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código de tu proyecto al contenedor
COPY . .

# Expone el puerto 8080 (Cloud Run mapea automáticamente)
EXPOSE 8080

# El comando para arrancar la aplicación
CMD ["python", "main.py"]
