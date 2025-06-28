import os
import uvicorn
import threading
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

# Estado global para ADK
adk_ready = False
adk_error = None
adk_loading = True

# Aplicación FastAPI mínima que inicia inmediatamente
app = FastAPI(title="ADK Agent Loader", description="Loading ADK Agent...")

@app.get("/health")
def health_check():
    """Health check endpoint para Cloud Run - debe responder inmediatamente"""
    return JSONResponse({"status": "healthy", "service": "adk-loader"})

@app.get("/")
def root():
    """Root endpoint que siempre responde"""
    return JSONResponse({
        "message": "ADK Agent Loader", 
        "status": "running",
        "adk_ready": adk_ready,
        "loading": adk_loading
    })

@app.get("/ping")
def ping():
    """Ping endpoint simple"""
    return JSONResponse({"ping": "pong", "timestamp": time.time()})

def load_adk_background():
    """Carga ADK en background de forma muy simple"""
    global adk_ready, adk_error, adk_loading
    
    try:
        time.sleep(2)  # Simular que está cargando
        print("🚀 Intentando cargar ADK...")
        
        # Configuración
        AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
        SESSION_DB_URL = "sqlite:///./sessions.db"
        ALLOWED_ORIGINS = ["*"]
        
        # Importar solo cuando sea necesario
        from google.adk.cli.fast_api import get_fast_api_app
        
        # Crear app ADK
        adk_app = get_fast_api_app(
            agents_dir=AGENTS_DIR,
            session_service_uri=SESSION_DB_URL,
            allow_origins=ALLOWED_ORIGINS,
            web=True,
        )
        
        # Montar como sub-aplicación
        app.mount("/adk", adk_app)
        
        adk_ready = True
        adk_loading = False
        print("✅ ADK cargado exitosamente")
        
    except Exception as e:
        adk_error = str(e)
        adk_loading = False
        print(f"❌ Error cargando ADK: {e}")

# Iniciar carga de ADK en background
print("🔧 FastAPI iniciando...")
threading.Thread(target=load_adk_background, daemon=True).start()
print("✅ FastAPI listo - ADK cargando en background")

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