# Chatbot Bilingüe - Tutor de Inglés

Chatbot inteligente basado en redes neuronales para enseñanza de inglés con soporte multiidioma.

## 🎯 Objetivos

- Responder en español como idioma base
- Enseñanza progresiva de inglés
- Usar red neuronal para adaptarse al nivel del usuario
- Tres idiomas soportados (español, inglés, posiblemente portugués)

## 📋 Estructura del Proyecto

```
chatbot-bilingue/
├── src/
│   ├── models/          # Modelos de red neuronal
│   ├── utils/           # Funciones auxiliares
│   └── main.py         # Punto de entrada
├── data/                # Datasets de entrenamiento
├── notebooks/           # Notebooks de análisis y desarrollo
├── requirements.txt     # Dependencias
└── README.md
```

## 🚀 Configuración Inicial

### 1. Clonar y configurar entorno

```bash
cd chatbot-bilingue
python -m venv venv
```

### 2. Activar entorno virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 📦 Ramas de Trabajo

- `main`: Versión estable
- `dev`: Rama de desarrollo
- `feature/neural-network`: Implementación de red neuronal
- `feature/spanish-base`: Base de respuestas en español
- `feature/progressive-english`: Sistema de enseñanza progresiva

## 🔧 Próximas Fases

1. **Base del chatbot** - Estructura y respuestas iniciales en español
2. **Red neuronal** - Modelo de aprendizaje
3. **Sistema de progresión** - Lógica de enseñanza inglés

## 📝 Notas

- Proyecto en construcción
- Las dependencias pueden ajustarse según necesidades
