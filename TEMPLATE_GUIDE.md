# 📖 Guía de la Plantilla ADK

## 🎯 Cómo usar esta plantilla para nuevos proyectos

### 1. **Crear un nuevo proyecto desde esta plantilla:**

```bash
# Opción A: Usar como template en GitHub
# 1. Ve al repositorio en GitHub
# 2. Click en "Use this template"
# 3. Crea tu nuevo repositorio

# Opción B: Clonar y personalizar
git clone https://github.com/TU-USUARIO/adk-template.git mi-nuevo-agente
cd mi-nuevo-agente
rm -rf .git
git init
```

### 2. **Personalizar para tu agente:**

#### **Cambiar el nombre del directorio del agente:**
```bash
# Renombrar el directorio
mv adk_short_bot mi_agente

# Actualizar imports en main.py si es necesario
```

#### **Actualizar pyproject.toml:**
```toml
[project]
name = "mi-agente-personalizado"
version = "0.1.0"
description = "Descripción de mi agente"
authors = [
    {name = "Tu Nombre", email = "tu@email.com"}
]
```

#### **Personalizar el agente:**
```python
# mi_agente/agent.py
root_agent = Agent(
    name="mi_agente_personalizado",
    model="gemini-2.0-flash",
    description="Mi agente hace cosas increíbles",
    instruction=MI_INSTRUCCION_PERSONALIZADA,
    tools=[mis_tools_personalizadas],
)
```

## 🔧 Gestión de dependencias: Mejores prácticas

### **Solo Poetry (Recomendado) 🏆**

#### ✅ **Ventajas:**
- **Una sola fuente de verdad**: `pyproject.toml`
- **Lock file automático**: reproducibilidad garantizada
- **Resolución inteligente**: evita conflictos de dependencias
- **Compatible con Cloud Run**: buildpacks detecta automáticamente
- **Gestión de versiones**: easy upgrade/downgrade

#### 🚀 **Workflow recomendado:**
```bash
# Desarrollo
poetry add nueva-dependencia

# Testing
poetry add --group dev pytest black flake8

# Deploy
# ¡No hacer nada! Cloud Run usa Poetry automáticamente
```

### **Poetry + requirements.txt (Solo si es necesario) ⚠️**

#### 📋 **¿Cuándo usar ambos?**
- Servicios legacy que requieren requirements.txt
- CI/CD que no soporta Poetry
- Heroku u otros PaaS sin soporte Poetry

#### 🔄 **Mantener sincronizados:**
```bash
# Generar requirements.txt desde Poetry
poetry export --output requirements.txt --without-hashes

# Agregar al pre-commit hook:
# .git/hooks/pre-commit
poetry export --output requirements.txt --without-hashes
git add requirements.txt
```

### **Solo requirements.txt (No recomendado) ❌**

#### ⚠️ **Problemas:**
- No hay lock file (builds no reproducibles)
- Resolución manual de dependencias
- No metadata del proyecto
- Propenso a errores de versión

## 🏗️ Arquitectura de la plantilla

### **Componentes principales:**

```
main.py ← Entry point
├── Configura FastAPI con ADK
├── Maneja puerto dinámico de Cloud Run
└── Activa interfaz web

adk_short_bot/ ← Tu agente
├── agent.py ← Configuración del agente
├── prompt.py ← Instrucciones/comportamiento
└── tools/ ← Herramientas funcionales
    ├── __init__.py ← Exportaciones
    └── *.py ← Implementaciones
```

### **Flujo de ejecución:**

```
Cloud Run → main.py → FastAPI → ADK → Tu Agente → Tools → Respuesta
```

## 🔄 Ciclo de desarrollo recomendado

### **1. Desarrollo local:**
```bash
# Instalar
poetry install

# Ejecutar
poetry run python main.py

# Probar en: http://localhost:8000
```

### **2. Testing:**
```bash
# Agregar tests
poetry add --group dev pytest

# Ejecutar tests
poetry run pytest
```

### **3. Deploy:**
```bash
# Commit cambios
git add .
git commit -m "feat: nueva funcionalidad"
git push

# Deploy directo
gcloud run deploy mi-agente --source . --region us-central1
```

## 🎨 Personalización avanzada

### **Agregar nuevas herramientas:**

```python
# mi_agente/tools/api_client.py
import requests

def llamar_api_externa(url: str, params: dict) -> dict:
    """
    Llama a una API externa y retorna los resultados
    
    Args:
        url: URL de la API
        params: Parámetros para la llamada
        
    Returns:
        dict: Respuesta de la API
    """
    response = requests.get(url, params=params)
    return response.json()
```

```python
# mi_agente/tools/__init__.py
from .character_counter import count_characters
from .api_client import llamar_api_externa

# Exportar todas las tools
__all__ = ["count_characters", "llamar_api_externa"]
```

```python
# mi_agente/agent.py
from mi_agente.tools import count_characters, llamar_api_externa

root_agent = Agent(
    name="mi_agente",
    tools=[count_characters, llamar_api_externa],  # 👈 Agregar aquí
    # ... resto de la configuración
)
```

### **Personalizar el modelo:**

```python
# Diferentes modelos disponibles
root_agent = Agent(
    name="mi_agente",
    model="gemini-2.0-flash",      # ← Más rápido
    # model="gemini-1.5-pro",      # ← Más potente
    # model="gemini-1.5-flash",    # ← Balance
)
```

### **Configuración avanzada de FastAPI:**

```python
# main.py - Personalización avanzada
app = get_fast_api_app(
    agents_dir=AGENTS_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=["https://mi-frontend.com"],  # ← Restringir CORS
    web=True,
    # title="Mi API personalizada",              # ← Título personalizado
    # version="1.0.0",                          # ← Versión
)
```

## 📦 Estructura de archivos recomendada

### **Para agentes simples:**
```
mi_agente/
├── main.py
├── pyproject.toml
├── poetry.lock
└── mi_agente/
    ├── agent.py
    ├── prompt.py
    └── tools/
        └── mi_tool.py
```

### **Para agentes complejos:**
```
mi_agente/
├── main.py
├── pyproject.toml
├── poetry.lock
├── config/
│   ├── settings.py
│   └── environments/
├── mi_agente/
│   ├── agent.py
│   ├── prompts/
│   │   ├── base.py
│   │   └── specialized.py
│   ├── tools/
│   │   ├── web/
│   │   ├── data/
│   │   └── analysis/
│   └── utils/
├── tests/
└── docs/
```

## 🚀 Tips de optimización

### **Performance:**
- Usa `gemini-2.0-flash` para respuestas rápidas
- Limita el tamaño de herramientas complejas
- Implementa caché para llamadas externas costosas

### **Costos:**
- Cloud Run cobra por uso (escalado a 0)
- Gemini se cobra por tokens
- Optimiza prompts para reducir tokens

### **Monitoreo:**
```bash
# Ver logs en tiempo real
gcloud run services logs tail mi-agente --region=us-central1

# Métricas en Cloud Console
gcloud run services describe mi-agente --region=us-central1
```

## 🔒 Consideraciones de seguridad

### **Variables de entorno sensibles:**
```bash
# Para secrets
gcloud run services update mi-agente \
  --set-env-vars="API_KEY=mi-secret-key" \
  --region=us-central1

# Mejor: usar Secret Manager
gcloud run services update mi-agente \
  --set-secrets="API_KEY=projects/PROJECT/secrets/api-key:latest" \
  --region=us-central1
```

### **Autenticación:**
```bash
# Quitar acceso público
gcloud run services remove-iam-policy-binding mi-agente \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=us-central1

# Agregar usuarios específicos
gcloud run services add-iam-policy-binding mi-agente \
  --member="user:usuario@dominio.com" \
  --role="roles/run.invoker" \
  --region=us-central1
```

---

**💡 Esta guía te ayudará a aprovechar al máximo la plantilla y crear agentes ADK profesionales.** 