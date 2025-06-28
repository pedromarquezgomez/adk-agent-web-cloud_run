import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Session DB URL
SESSION_DB_URL = "sqlite:///./sessions.db"
# CORS origins
ALLOWED_ORIGINS = ["*"]
# Enable web UI
SERVE_WEB_INTERFACE = True

# Create the FastAPI app with correct parameters
app = get_fast_api_app(
    agent_dir=AGENT_DIR,
    session_db_url=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

if __name__ == "__main__":
    # Use the PORT that Cloud Run wants (8000 by default)
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))