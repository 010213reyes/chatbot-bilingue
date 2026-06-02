# 🚀 Guía de Ejecución - Chatbot Bilingüe

## 📍 El Orquestador: `AdvancedBilingualChatbot`

El archivo **`src/advanced_chatbot.py`** es el **corazón del proyecto**. Coordina todos los componentes:

```
┌─────────────────────────────────────────────────────────────┐
│         AdvancedBilingualChatbot (ORQUESTADOR)              │
│                  src/advanced_chatbot.py                    │
└─────────────────────────────────────────────────────────────┘
        ↓ Usa componentes en cadena ↓

┌────────────────────────┐  ┌─────────────────────┐
│  ContextManager        │  │  LevelManager       │
│  (gestor de frases)    │  │  (manejo de niveles)│
└────────────────────────┘  └─────────────────────┘
        ↓                            ↓
┌────────────────────────┐  ┌─────────────────────┐
│  LevelMapper           │  │  LevelClassifier    │
│  (frases → niveles)    │  │  (red neuronal)     │
└────────────────────────┘  └─────────────────────┘
        ↓                            ↓
┌────────────────────────┐  ┌─────────────────────┐
│  EvaluationService     │  │  ProgressTracker    │
│  (quiz adaptativo)     │  │  (persistencia JSON)│
└────────────────────────┘  └─────────────────────┘
```

---

## 🎯 Cómo Ejecutar en Tu Máquina

### **Paso 1: Requisitos Previos**

```powershell
# Ubicarse en la carpeta del proyecto
cd "c:\Users\REYES\OneDrive\Desktop\chatbot-bilingue"

# Verificar que Python está instalado
python --version
```

**Debe mostrar**: Python 3.8+

---

### **Paso 2: Crear y Activar Entorno Virtual**

```powershell
# Crear venv (solo primera vez)
python -m venv venv

# Activar venv (IMPORTANTE - hacer esto antes de cada sesión)
.\venv\Scripts\Activate.ps1
```

**Después activado, deberías ver**: `(venv)` al inicio de tu terminal PowerShell

---

### **Paso 3: Instalar Dependencias**

```powershell
# Una sola vez
pip install -r requirements.txt
```

**Instala**: numpy, scikit-learn, tensorflow (opcional), etc.

---

### **Paso 4: Ejecutar el Chatbot**

#### **Opción A: Chatbot Simple (Base en Español)**
```powershell
python src/chatbot.py
```

**Qué hace:**
- Responde en español
- Busca frases en contextos
- Traduce al inglés
- NO tiene red neuronal ni progresión

---

#### **Opción B: Chatbot Avanzado (CON Red Neuronal)** ← **RECOMENDADO**
```powershell
python src/advanced_chatbot.py
```

**Qué hace:**
- ✅ Quiz inicial (5 preguntas)
- ✅ Clasifica nivel automáticamente (A1-B2)
- ✅ Sesiones adaptadas al nivel
- ✅ Red neuronal predice progresión
- ✅ Guarda progreso en `data/user_progress/`
- ✅ Spaced repetition automática

---

## 🧠 ¿Qué Pasa Cuando Ejecutas `advanced_chatbot.py`?

### **Flujo de Ejecución**

```
1. Usuario ejecuta: python src/advanced_chatbot.py
                    ↓
2. AdvancedBilingualChatbot.__init__() se ejecuta
   └─ Carga contextos desde data/contexts.json
   └─ Inicializa LevelMapper (mapea frases A1-B2)
   └─ Crea LevelClassifier (red neuronal lista)
   └─ Prepara EvaluationService (quiz)
   └─ Carga/Crea ProgressTracker (progreso usuario)
                    ↓
3. Muestra menú inicial:
   - Ver contextos disponibles
   - Seleccionar contexto
   - Preguntar cómo decir algo
   - Traducir del inglés
   - Practicar
   - Ver estadísticas
                    ↓
4. Usuario selecciona opción
   └─ Quiz inicial (5 preguntas) → Clasifica nivel
   └─ Sesión de práctica → Valida respuestas
   └─ Red neuronal → Evalúa progresión
   └─ ProgressTracker → Guarda progreso
```

---

## 📊 Ejemplo de Sesión Completa

```powershell
PS C:\Users\REYES\OneDrive\Desktop\chatbot-bilingue> python src/advanced_chatbot.py

╔════════════════════════════════════════════════╗
║  CHATBOT BILINGÜE - NIVEL A1                   ║
╚════════════════════════════════════════════════╝

📊 Tu progreso:
   {'user_id': 'demo_user_001', 'nivel_actual': 'A1', ...}

Opciones:
  1. Ver información de tu nivel
  2. Iniciar sesión de práctica
  3. Ver estadísticas
  4. Ver frases para repasar
  5. Salir

Selecciona (1-5): 2
✅ Practicando en contexto: Videojuegos - General

👤 Usuario: ¿Cómo se dice 'Necesito ayuda' en inglés?
🤖 Bot: I need help - Pedir asistencia en el juego
...
```

---

## 🗂️ Dónde Viven los Datos

### **Entrada (Lectura)**
```
data/
├── contexts.json              ← Frases mapeadas (ES/EN)
└── Contenido:
    - 20 frases base
    - Divididas en 4 contextos
    - Mapeadas a niveles A1-B2
```

### **Salida (Escritura)**
```
data/user_progress/
└── user_001.json              ← Progreso persistido
    - Nivel actual y máximo
    - Frases aprendidas
    - Sesiones completadas
    - Accuracy promedio
    - Timestamps de repaso
```

**Archivo generado automáticamente** después de primera sesión.

---

## 🔧 Componentes del Orquestador Explicados

### **1. ContextManager**
```python
# Lee data/contexts.json
# Busca frases por español o inglés
# Extrae vocabulario por contexto
context_manager.search_phrase_by_spanish("Necesito ayuda")
# → {'es': 'Necesito ayuda', 'en': 'I need help', ...}
```

### **2. LevelMapper**
```python
# Mapea cada frase a su nivel (A1, A2, B1, B2)
# Basado en contexto
level_mapper.get_phrases_by_level('A1')
# → [frase1, frase2, ...]
```

### **3. LevelClassifier (Red Neuronal)**
```python
# 10 features de desempeño → predice nivel
classifier.predict_level({
    'accuracy': 0.85,
    'sesiones': 5,
    'frases_unicas': 30,
    ...
})
# → ('B1', 0.92)  # Nivel B1 con 92% confianza
```

### **4. EvaluationService**
```python
# Genera quiz inicial (5 preguntas)
# Valida respuestas
# Detecta cuando subir de nivel
evaluation_service.create_initial_evaluation()
# → {'questions': [q1, q2, ...]}
```

### **5. ProgressTracker**
```python
# Guarda progreso en JSON
# Calcula estadísticas
# Programa repaso (spaced repetition)
progress_tracker.add_session({...})
# → Guarda en data/user_progress/user_001.json
```

---

## 💾 Configuración Central

**Archivo**: `src/config/settings.py`

Todos los parámetros en UN lugar:

```python
ENGLISH_LEVELS = {
    'A1': {'nombre': 'Principiante', 'rango': (0, 20)},
    'A2': {'nombre': 'Elemental', 'rango': (20, 40)},
    'B1': {'nombre': 'Intermedio', 'rango': (40, 70)},
    'B2': {'nombre': 'Intermedio-Alto', 'rango': (70, 100)},
}

MAX_LEVEL = 'B2'  # Máximo nivel soportado

EVALUATION_CONFIG = {
    'preguntas_por_nivel': 5,      # 5 preguntas quiz inicial
    'puntaje_minimo_progreso': 70,  # 70% para subir nivel
    'sesiones_para_consolidar': 3,  # 3 sesiones exitosas
}

PROGRESSION_CONFIG = {
    'frases_nuevas_por_sesion': 3,
    'repeticion_espaciada_dias': [1, 3, 7, 14],  # Repaso programado
    'duracion_sesion_minutos': 15,
}
```

**¿Quieres cambiar algo?** Edita aquí y afecta TODO el proyecto.

---

## 🎮 Casos de Uso

### **Caso 1: Usuario Nuevo**
```
1. python src/advanced_chatbot.py
2. Sistema crea user_001.json en data/user_progress/
3. Quiz inicial (5 preguntas)
4. Clasificado como A1/A2/B1/B2
5. Sesión de práctica
6. Guarda progreso
```

### **Caso 2: Usuario Existente**
```
1. python src/advanced_chatbot.py
2. Lee user_001.json existente
3. Carga nivel y frases aprendidas
4. Sesión nueva
5. Actualiza estadísticas
6. Verifica si puede avanzar nivel
```

### **Caso 3: Personalización**
```
# Cambiar usuario
bot = AdvancedBilingualChatbot(contexts_file, user_id="otro_usuario")

# Cambiar contexto
bot.start_practice_session("videojuegos_batalla")

# Ver progreso
print(bot.progress_tracker.get_progress_summary())
```

---

## 🐛 Troubleshooting

### **Error: ModuleNotFoundError**
```
❌ ModuleNotFoundError: No module named 'numpy'

✅ Solución:
pip install -r requirements.txt
```

### **Error: contexts.json no encontrado**
```
❌ FileNotFoundError: No encontrado: data/contexts.json

✅ Solución:
# Asegúrate estar en la carpeta correcta
cd "c:\Users\REYES\OneDrive\Desktop\chatbot-bilingue"
```

### **Error: venv no activado**
```
❌ No ve los paquetes instalados

✅ Solución:
.\venv\Scripts\Activate.ps1
# Deberías ver (venv) en tu prompt
```

---

## 📈 Estructura de Datos (JSON)

### **contexts.json** (Entrada)
```json
{
  "contexts": {
    "saludo_basico": {
      "nombre": "Saludos Básicos",
      "frases": [
        {
          "es": "Hola, ¿cómo estás?",
          "en": "Hi, how are you?",
          "en_alt": ["Hello, how are you doing?"],
          "uso": "Saludo informal"
        }
      ]
    }
  }
}
```

### **user_001.json** (Salida - Progreso)
```json
{
  "user_id": "user_001",
  "nivel_actual": "A2",
  "nivel_maximo": "B1",
  "frases_aprendidas": [
    {"frase": "I need help", "nivel": "A1", "fecha_aprendida": "2026-06-02T..."}
  ],
  "sesiones": [
    {"fecha": "2026-06-02T...", "aciertos": 4, "total": 5, "accuracy": 0.8}
  ],
  "estadisticas": {
    "total_sesiones": 5,
    "accuracy_promedio": 0.78,
    "aciertos_totales": 39
  }
}
```

---

## 🚀 Comandos Rápidos

```powershell
# Entrar a la carpeta
cd "c:\Users\REYES\OneDrive\Desktop\chatbot-bilingue"

# Activar venv (CADA VEZ)
.\venv\Scripts\Activate.ps1

# Ejecutar chatbot avanzado
python src/advanced_chatbot.py

# Ver historial de commits
git log --oneline

# Ver qué cambió
git status

# Desactivar venv (cuando termines)
deactivate
```

---

## 📝 Resumiendo

| Componente | Archivo | Función |
|-----------|---------|---------|
| **Orquestador** | `src/advanced_chatbot.py` | Coordina todo |
| **Contextos** | `src/models/context_manager.py` | Lee frases |
| **Niveles** | `src/models/levels/` | Gestiona A1-B2 |
| **Red Neuronal** | `src/models/neural/level_classifier.py` | Predice nivel |
| **Evaluación** | `src/services/evaluation_service.py` | Quiz y progresión |
| **Progreso** | `src/services/progress_tracker.py` | Guarda datos |
| **Config** | `src/config/settings.py` | Parámetros centrales |
| **Datos** | `data/contexts.json` | Frases entrada |
| **Usuario** | `data/user_progress/user_001.json` | Progreso salida |

---

**¿Preguntas?** El comando mágico es:
```powershell
python src/advanced_chatbot.py
```

Todo lo demás sucede **automáticamente**.
