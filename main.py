import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Obtiene el directorio donde está main.py
AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
# ADK necesita una base de datos para las sesiones, SQLite es perfecto para esto
SESSION_DB_URL = "sqlite:///./sessions.db"
# Permite todas las conexiones
ALLOWED_ORIGINS = ["*"]
# Activa la interfaz web
SERVE_WEB_INTERFACE = True

# Llama a la función del ADK para obtener la aplicación FastAPI
app = get_fast_api_app(
    agents_dir=AGENTS_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

if __name__ == "__main__":
    # Inicia el servidor en el puerto correcto y escuchando en 0.0.0.0
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))