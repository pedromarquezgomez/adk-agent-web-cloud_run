import os
import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# Configuración básica
AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DB_URL = "sqlite:///./sessions.db"
ALLOWED_ORIGINS = ["*"]
SERVE_WEB_INTERFACE = True

print("🔧 Iniciando configuración de ADK...")

# Crear aplicación básica primero para health check
base_app = FastAPI(title="ADK Agent Health Check")

@base_app.get("/health")
async def health_check():
    """Health check endpoint para Cloud Run"""
    return {"status": "healthy", "service": "adk-agent"}

@base_app.get("/")
async def root():
    """Root endpoint redirect"""
    return {"message": "ADK Agent is running", "status": "ok"}

try:
    print("🚀 Configurando ADK...")
    # Llama a la función del ADK para obtener la aplicación FastAPI
    app = get_fast_api_app(
        agents_dir=AGENTS_DIR,
        session_service_uri=SESSION_DB_URL,
        allow_origins=ALLOWED_ORIGINS,
        web=SERVE_WEB_INTERFACE,
    )
    print("✅ ADK configurado exitosamente")
except Exception as e:
    print(f"❌ Error configurando ADK: {e}")
    # Usar aplicación básica como fallback
    app = base_app

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