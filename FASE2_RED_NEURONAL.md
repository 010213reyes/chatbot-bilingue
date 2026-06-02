# Fase 2: Red Neuronal y Progresión A1-B2

## ✅ Completado

### Arquitectura Modular

```
src/
├── config/
│   └── settings.py          # Configuración centralizada
├── models/
│   ├── levels/
│   │   ├── level_manager.py # Gestión de niveles A1-B2
│   │   └── level_mapper.py  # Mapeo de frases a niveles
│   └── neural/
│       └── level_classifier.py  # Red neuronal (TensorFlow/fallback)
├── services/
│   ├── evaluation_service.py    # Quiz evaluativo
│   └── progress_tracker.py      # Rastreo de usuario
└── advanced_chatbot.py      # Chatbot integrado
```

### Funcionalidades Implementadas

#### 1. **Sistema de Niveles (A1-B2)**
- ✅ Definición de 4 niveles CEFR
- ✅ Rango de puntajes por nivel
- ✅ Transición automática entre niveles
- ✅ Contextos asociados a cada nivel

**Mapeo:**
- **A1 (0-20%)**: Saludos básicos + Videojuegos general
- **A2 (20-40%)**: Videojuegos general + Batalla
- **B1 (40-70%)**: Videojuegos batalla + Coordinación
- **B2 (70-100%)**: Videojuegos coordinación

#### 2. **Red Neuronal - LevelClassifier**
- ✅ Modelo con capas Dense + Dropout
- ✅ Fallback a SimpleClassifier (sin TensorFlow)
- ✅ 10 features de desempeño:
  - Accuracy promedio
  - Velocidad de respuesta
  - Contextos completados
  - Racha de aciertos
  - Frases aprendidas
  - Sesiones completadas
  - Días activo
  - Ratio de error
  - Velocidad lectura
  - Consistencia

#### 3. **Evaluación Adaptativa**
- ✅ Quiz inicial (5 preguntas A1)
- ✅ Validación de respuestas
- ✅ Cálculo de puntaje y nivel recomendado
- ✅ Detección automática de progresión

#### 4. **Rastreo de Progreso**
- ✅ Persistencia en JSON por usuario
- ✅ Estadísticas agregadas
- ✅ Historial de sesiones
- ✅ Frases aprendidas con timestamps
- ✅ Spaced repetition (1, 3, 7, 14 días)

#### 5. **Chatbot Avanzado - AdvancedBilingualChatbot**
Integra todos los componentes:
- ✅ Evaluación inicial
- ✅ Selección automática de contextos por nivel
- ✅ Sesiones de práctica adaptativas
- ✅ Validación de respuestas
- ✅ Detección de progresión
- ✅ Resumen de sesión
- ✅ Estadísticas en tiempo real

### Configuración Centralizada (src/config/settings.py)

```python
ENGLISH_LEVELS = {
    'A1': {'nombre': 'Principiante', 'rango': (0, 20)},
    'A2': {'nombre': 'Elemental', 'rango': (20, 40)},
    'B1': {'nombre': 'Intermedio', 'rango': (40, 70)},
    'B2': {'nombre': 'Intermedio-Alto', 'rango': (70, 100)},
}

MAX_LEVEL = 'B2'

EVALUATION_CONFIG = {
    'preguntas_por_nivel': 5,
    'puntaje_minimo_progreso': 70,  # 70%
    'sesiones_para_consolidar': 3,
}

PROGRESSION_CONFIG = {
    'frases_nuevas_por_sesion': 3,
    'repeticion_espaciada_dias': [1, 3, 7, 14],
    'duracion_sesion_minutos': 15,
}
```

### Flujo de Usuario

```
1. Usuario nuevo → Evaluación inicial (5 preguntas)
   ↓
2. Clasificación automática (A1-B2)
   ↓
3. Inicia sesión de práctica en contexto del nivel
   ↓
4. ¿Accuracy ≥ 70%? + ¿3 sesiones exitosas?
   ├─ SÍ → Propone avanzar de nivel
   └─ NO → Sigue en nivel actual
   ↓
5. Spaced repetition: repasa frases a los 1, 3, 7, 14 días
```

### Archivos Clave

| Archivo | Responsabilidad |
|---------|-----------------|
| `level_manager.py` | Gestión de niveles y transiciones |
| `level_mapper.py` | Mapeo de contextos/frases a niveles |
| `level_classifier.py` | Predicción de nivel con NN |
| `evaluation_service.py` | Quiz y evaluación |
| `progress_tracker.py` | Persistencia y rastreo de usuario |
| `advanced_chatbot.py` | Integración completa |

### Validaciones

✅ 10 frases en A1 (saludos + videojuegos general)
✅ 5 frases en A2 (batalla)
✅ 5 frases en B1 (coordinación)
✅ 0 frases en B2 (listo para agregar)
✅ Red neuronal funcional con fallback simple

### Datos Persistidos

Por usuario (data/user_progress/{user_id}.json):
```json
{
  "user_id": "user_001",
  "nivel_actual": "A1",
  "nivel_maximo": "A2",
  "frases_aprendidas": [...],
  "sesiones": [...],
  "estadisticas": {
    "accuracy_promedio": 0.78,
    "total_sesiones": 5,
    "aciertos_totales": 39
  }
}
```

## 🔧 Próximos Pasos

1. **Agregar contextos B2** (más frases avanzadas)
2. **Entrenar red neuronal** con datos reales
3. **Frontend web** (Flask/Django)
4. **API REST** para cliente móvil
5. **Sistema de recompensas** (badges, streak counter)

## 📦 Ejecución

```bash
# Demo del sistema
python src/advanced_chatbot.py

# Con venv
venv\Scripts\python src/advanced_chatbot.py
```

## 🌳 Rama

`feature/neural-network` ✅ Completada y con commit
