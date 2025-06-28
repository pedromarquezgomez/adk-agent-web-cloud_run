# 🤖 Plantilla ADK Agent + Cloud Run

Una plantilla completa para crear y desplegar agentes de Google ADK (Agent Development Kit) en Cloud Run con interfaz web.

## 📋 ¿Qué incluye esta plantilla?

- ✅ **Agente ADK** configurado y funcional
- ✅ **Interfaz Web** integrada con FastAPI
- ✅ **Deploy automático** en Google Cloud Run
- ✅ **Gestión de dependencias** con Poetry
- ✅ **Base de datos SQLite** para sesiones
- ✅ **Estructura modular** y escalable

## 🛠️ Tecnologías utilizadas

- **Python 3.12+**
- **Google ADK** (Agent Development Kit)
- **FastAPI** para la API web
- **SQLite** para persistencia
- **Poetry** para gestión de dependencias
- **Google Cloud Run** para deployment
- **Buildpacks** para containerización automática

## 📁 Estructura del proyecto

```
proyecto/
├── main.py                    # 🚀 Entry point de la aplicación
├── pyproject.toml            # 📦 Configuración de Poetry y proyecto
├── poetry.lock              # 🔒 Lock file de dependencias
├── .gitignore               # 🚫 Archivos a ignorar en Git
├── .gcloudignore           # ☁️ Archivos a ignorar en Cloud Build
├── README.md               # 📚 Esta documentación
└── adk_short_bot/          # 🤖 Directorio del agente
    ├── __init__.py         #     Configuración del paquete
    ├── agent.py           #     Definición del agente
    ├── prompt.py          #     Instrucciones del agente
    └── tools/             #     🛠️ Herramientas del agente
        ├── __init__.py    #     Exportación de tools
        └── character_counter.py  # Herramienta de ejemplo
```

## 🚀 Uso de esta plantilla

### 1. **Clona o usa como template:**
```bash
git clone [URL-DE-TU-TEMPLATE]
cd tu-proyecto-adk
```

### 2. **Personaliza tu agente:**
- Edita `adk_short_bot/agent.py` - nombre, modelo, descripción
- Modifica `adk_short_bot/prompt.py` - instrucciones del agente
- Agrega tools en `adk_short_bot/tools/` - funcionalidades adicionales

### 3. **Instala dependencias:**
```bash
poetry install
```

### 4. **Prueba localmente:**
```bash
poetry run python main.py
```
Visita: http://localhost:8000

### 5. **Deploya en Cloud Run:**
```bash
gcloud run deploy tu-agente --source . --platform managed --region us-central1 --allow-unauthenticated
```

## ⚙️ Configuración

### Variables de entorno (.env):
```bash
# Opcional: Para configuraciones específicas
GOOGLE_CLOUD_PROJECT=tu-proyecto-id
GOOGLE_CLOUD_LOCATION=us-central1
# El agente funciona sin .env, pero puedes agregar configuraciones aquí
```

### Configuración de Google Cloud:
```bash
# 1. Instala gcloud CLI
# 2. Autentícate
gcloud auth login
gcloud config set project tu-proyecto-id

# 3. Habilita APIs (automático en primer deploy)
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## 📦 Gestión de dependencias: Poetry vs Requirements

### 🎯 **Recomendación: Solo Poetry**

Esta plantilla usa **exclusivamente Poetry** porque:

#### ✅ **Ventajas de Poetry:**
- **Gestión unificada**: dependencias + metadata del proyecto
- **Lock file automático**: `poetry.lock` garantiza builds reproducibles
- **Resolución de dependencias**: evita conflictos automáticamente
- **Entornos virtuales**: manejo automático
- **Build y publish**: integrados

#### ❌ **¿Por qué NO mezclar con requirements.txt?**
- **Duplicación**: mantener dos archivos es propenso a errores
- **Conflictos**: versiones diferentes entre archivos
- **Complejidad**: dos fuentes de verdad
- **Cloud Run + Buildpacks**: detecta y usa Poetry automáticamente

#### 🏗️ **Para deployment en Cloud Run:**
1. **Buildpacks detecta Poetry** automáticamente
2. **Instala dependencias** desde `pyproject.toml`
3. **Usa poetry.lock** para versiones exactas
4. **No necesita** Dockerfile ni requirements.txt

### 📋 **Comandos útiles de Poetry:**

```bash
# Agregar dependencia
poetry add nombre-paquete

# Agregar dependencia de desarrollo
poetry add --group dev nombre-paquete

# Actualizar dependencias
poetry update

# Instalar en producción (solo main dependencies)
poetry install --only=main

# Mostrar dependencias
poetry show --tree
```

## 🔧 Personalización del agente

### 1. **Cambia el nombre y comportamiento:**
```python
# adk_short_bot/agent.py
root_agent = Agent(
    name="tu_agente",  # 👈 Cambia aquí
    model="gemini-2.0-flash",
    description="Descripción de tu agente",  # 👈 Y aquí
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[tus_tools],  # 👈 Agrega tus herramientas
)
```

### 2. **Modifica las instrucciones:**
```python
# adk_short_bot/prompt.py
ROOT_AGENT_INSTRUCTION = """
Tus instrucciones personalizadas aquí...
"""
```

### 3. **Agrega nuevas herramientas:**
```python
# adk_short_bot/tools/nueva_tool.py
def nueva_funcionalidad(parametro: str) -> str:
    """
    Descripción de tu nueva herramienta
    """
    return f"Resultado: {parametro}"
```

## 🚀 Deployment

### Proceso automático con Buildpacks:
1. **Detecta** Python + Poetry automáticamente
2. **Instala** dependencias desde pyproject.toml
3. **Ejecuta** main.py como entry point
4. **Configura** puerto dinámico automáticamente

### URL de tu aplicación:
Después del deploy: `https://tu-servicio-[ID].us-central1.run.app`

## 🔍 Debugging

### Logs en tiempo real:
```bash
gcloud run services logs tail tu-servicio --region=us-central1
```

### Prueba local:
```bash
poetry run python main.py
# Abre: http://localhost:8000
# API docs: http://localhost:8000/docs
```

## 📚 Recursos adicionales

- **[Google ADK Documentation](https://cloud.google.com/agent-development-kit)**
- **[Poetry Documentation](https://python-poetry.org/docs/)**
- **[Cloud Run Documentation](https://cloud.google.com/run/docs)**
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)**

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

[Tu licencia preferida]

---

**💡 Tip**: Esta plantilla está optimizada para simplicidad y mejores prácticas. ¡Úsala como base para tus proyectos ADK!