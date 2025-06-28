import os
import uvicorn
import asyncio
import threading
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

# Configuración básica
AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_DB_URL = "sqlite:///./sessions.db"
ALLOWED_ORIGINS = ["*"]
SERVE_WEB_INTERFACE = True

# Estado global para ADK
adk_app = None
adk_ready = False
adk_error = None

# Aplicación FastAPI que inicia inmediatamente
app = FastAPI(title="ADK Agent Proxy")

@app.get("/health")
async def health_check():
    """Health check endpoint para Cloud Run"""
    return {"status": "healthy", "service": "adk-agent", "adk_ready": adk_ready}

@app.get("/")
async def root():
    """Status endpoint"""
    if adk_ready and adk_app:
        return {"message": "ADK Agent is ready", "status": "ready"}
    elif adk_error:
        return {"message": f"ADK Agent failed to load: {adk_error}", "status": "error"}
    else:
        return {"message": "ADK Agent is loading...", "status": "loading"}

@app.get("/status")
async def status():
    """Endpoint de estado detallado"""
    return {
        "adk_ready": adk_ready,
        "adk_error": str(adk_error) if adk_error else None,
        "message": "ADK Agent Status"
    }

@app.get("/ui", response_class=HTMLResponse)
async def ui_redirect():
    """Redirección a la UI de ADK cuando esté lista"""
    if adk_ready and adk_app:
        return """
        <html>
            <head><meta http-equiv="refresh" content="0; url=/web"></head>
            <body>Redirecting to ADK UI...</body>
        </html>
        """
    else:
        return """
        <html>
            <body>
                <h1>ADK Agent Loading...</h1>
                <p>Please wait while the ADK agent initializes.</p>
                <script>setTimeout(() => location.reload(), 3000);</script>
            </body>
        </html>
        """

def initialize_adk():
    """Inicializa ADK en background thread"""
    global adk_app, adk_ready, adk_error
    
    try:
        print("🚀 Iniciando configuración de ADK en background...")
        from google.adk.cli.fast_api import get_fast_api_app
        
        # Configurar ADK
        temp_app = get_fast_api_app(
            agents_dir=AGENTS_DIR,
            session_service_uri=SESSION_DB_URL,
            allow_origins=ALLOWED_ORIGINS,
            web=SERVE_WEB_INTERFACE,
        )
        
        # Mount ADK app como sub-aplicación
        app.mount("/adk", temp_app)
        app.mount("/web", temp_app)  # Para la UI web
        
        adk_app = temp_app
        adk_ready = True
        print("✅ ADK configurado exitosamente y montado")
        
    except Exception as e:
        adk_error = e
        print(f"❌ Error configurando ADK: {e}")

# Inicializar ADK en background thread
print("🔧 Iniciando aplicación FastAPI...")
threading.Thread(target=initialize_adk, daemon=True).start()

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