import os
import uvicorn
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Aplicación FastAPI completamente independiente para test
app = FastAPI(title="Test FastAPI App", description="Testing Cloud Run deployment")

@app.get("/health")
def health_check():
    """Health check endpoint para Cloud Run"""
    return JSONResponse({"status": "healthy", "service": "test-app", "timestamp": time.time()})

@app.get("/")
def root():
    """Root endpoint"""
    return JSONResponse({
        "message": "Test FastAPI App funcionando correctamente", 
        "status": "running",
        "timestamp": time.time(),
        "port": os.environ.get("PORT", "8000")
    })

@app.get("/ping")
def ping():
    """Ping endpoint"""
    return JSONResponse({"ping": "pong", "timestamp": time.time()})

@app.get("/test")
def test():
    """Test endpoint para verificar que todo funciona"""
    return JSONResponse({
        "test": "successful",
        "message": "FastAPI está funcionando correctamente en Cloud Run",
        "env_vars": {
            "PORT": os.environ.get("PORT"),
            "PYTHONPATH": os.environ.get("PYTHONPATH", "not set")
        }
    })

print("🚀 FastAPI iniciando...")

if __name__ == "__main__":
    # Configuración optimizada para Cloud Run
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Iniciando servidor en puerto {port}")
    
    # Inicia el servidor con configuración optimizada para Cloud Run
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        access_log=False,  # Reduce overhead en producción
        timeout_keep_alive=120,  # Mantiene conexiones vivas más tiempo
    )