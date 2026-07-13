# Chatbot Bilingüe - Tutor de Inglés con Red Neuronal

Chatbot inteligente basado en redes neuronales para enseñanza contextual de inglés. Responde en español, enseña inglés con profesionalismo desde A1 hasta B2.

## 🎯 Características

✅ **Aprendizaje Contextual**: Frases en situaciones reales (videojuegos, chats en línea, etc.)  
✅ **Niveles Adaptativos**: A1 → A2 → B1 → B2 (CEFR)  
✅ **Red Neuronal**: Clasifica nivel del usuario automáticamente  
✅ **Evaluación Adaptativa**: Quiz inicial para determinar nivel  
✅ **Rastreo de Progreso**: Persistencia JSON, estadísticas, spaced repetition  
✅ **Responde en Español**: Base en español, guía progresiva hacia inglés  
✅ **Memoria Conversacional**: Registra conversaciones por usuario (Fase 4)  
✅ **Detección de Intención**: Analiza automáticamente intención y contexto implícito (Fase 4)  
✅ **Aprendizaje Guiado**: Captura correcciones del usuario, validación antes de incorporar (Fase 4)

## 📋 Estructura del Proyecto

```
chatbot-bilingue/
├── src/
│   ├── config/
│   │   └── settings.py                    # Config centralizada
│   ├── models/
│   │   ├── context_manager.py             # Gestor de contextos
│   │   ├── contextual/                    # Fase 3: Lecciones contextuales
│   │   │   ├── contextual_lesson.py
│   │   │   └── __init__.py
│   │   ├── memory/                        # Fase 4: Memoria conversacional
│   │   │   ├── conversation_message.py    # Mensajes y conversaciones
│   │   │   ├── detected_intention.py      # Intención detectada
│   │   │   ├── correction.py              # Correcciones propuestas/aprobadas
│   │   │   └── __init__.py
│   │   ├── levels/
│   │   │   ├── level_manager.py           # Gestión A1-B2
│   │   │   └── level_mapper.py            # Mapeo frases→niveles
│   │   └── neural/
│   │       └── level_classifier.py        # Red neuronal + clasificador
│   ├── services/
│   │   ├── evaluation_service.py          # Quiz evaluativo
│   │   ├── progress_tracker.py            # Rastreo usuario
│   │   ├── contextual_lesson_service.py   # Fase 3: Servicio de lecciones
│   │   ├── memory_service.py              # Fase 4: Persistencia de conversaciones
│   │   ├── intention_detector_service.py  # Fase 4: Detección de intención
│   │   ├── correction_validator_service.py # Fase 4: Validación de correcciones
│   │   └── __init__.py
│   ├── chatbot.py                         # Chatbot base (español)
│   └── advanced_chatbot.py                # Chatbot avanzado (NN + progresión)
├── data/
│   ├── contexts.json                      # Base de frases y contextos
│   ├── levels/                            # Frases por nivel
│   ├── user_progress/                     # Progreso de usuarios
│   ├── user_conversations/                # Fase 4: Historial de conversaciones
│   └── learned_phrases.json               # Fase 4: Correcciones propuestas/aprobadas
├── FASE1_BASE.md                          # Documentación fase 1
├── FASE2_RED_NEURONAL.md                  # Documentación fase 2
├── FASE3_CONTEXTO.md                      # Documentación fase 3
├── FASE4_MEMORIA.md                       # Documentación fase 4
├── PLAN_FASES.md                          # Plan general de fases
├── demo_interactive.py                    # Demo interactiva fase 1-3
└── demo_fase4.py                          # Demo fase 4: memoria y correcciones
```

## 📊 Niveles (CEFR)

| Nivel | Nombre | Rango | Contextos |
|-------|--------|-------|-----------|
| A1 | Principiante | 0-20% | Saludos + Videojuegos general |
| A2 | Elemental | 20-40% | Videojuegos general + Batalla |
| B1 | Intermedio | 40-70% | Videojuegos batalla + Coordinación |
| B2 | Intermedio-Alto | 70-100% | Videojuegos coordinación |

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

## 📖 Uso

### Chatbot Base (Español)
```bash
python src/chatbot.py
```

### Chatbot Avanzado (Red Neuronal + Progresión)
```bash
python src/advanced_chatbot.py
```

### Demo Interactiva (Fases 1-3)
```bash
python demo_interactive.py
```

### Demo de Fase 4 (Memoria y Correcciones)
```bash
python demo_fase4.py
```
Este script demuestra:
- Carga/creación de historial de usuario
- Almacenamiento de mensajes con intención detectada
- Detección de intención y contexto implícito
- Propuesta de correcciones
- Validación automática de correcciones
- Aprobación/rechazo por admin


## 🧠 Arquitectura

### Red Neuronal (LevelClassifier)
- **Modelo**: Dense NN con Dropout (TensorFlow/Keras)
- **Features**: 10 métricas de desempeño
  - Accuracy promedio
  - Velocidad de respuesta
  - Contextos completados
  - Racha de aciertos
  - Frases aprendidas únicas
  - Sesiones completadas
  - Días activo
  - Ratio de error
  - Velocidad lectura
  - Consistencia

### Evaluación
- **Quiz Inicial**: 5 preguntas A1
- **Criterio Progreso**: 70% accuracy + 3 sesiones exitosas
- **Spaced Repetition**: 1, 3, 7, 14 días

### Persistencia
Datos por usuario en `data/user_progress/{user_id}.json`:
```json
{
  "nivel_actual": "B1",
  "nivel_maximo": "B1",
  "frases_aprendidas": 34,
  "sesiones_completadas": 12,
  "accuracy_promedio": 0.82,
  "estadisticas": {...}
}
```

## 🌳 Ramas de Trabajo

- `main`: Versión estable
- `dev`: Rama de desarrollo
- `feature/spanish-base`: ✅ Base contextual (COMPLETADA)
- `feature/neural-network`: ✅ Red neuronal A1-B2 (COMPLETADA)

## 📦 Dependencias

```
tensorflow==2.14.0      # Red neuronal
numpy==1.24.3           # Álgebra
scikit-learn==1.3.2     # ML utilities
transformers==4.34.0    # NLP avanzado (opcional)
```

## 🎮 Ejemplo de Flujo

```
1. Usuario nuevo
   ↓
2. Quiz inicial (5 preguntas A1)
   ↓
3. Sistema clasifica: "Eres A2"
   ↓
4. Sesión de práctica en contexto
   👤 "¿Cómo digo 'Necesito ayuda' en inglés?"
   🤖 "I need help - Pedir asistencia en el juego"
   ↓
5. Después de 3 sesiones con 70% accuracy
   ✅ "Propuesta: ¿Avanzar a B1?"
```

## 📝 Próximas Fases

1. ✅ **Fase 1**: Base contextual (COMPLETADA)
2. ✅ **Fase 2**: Red neuronal + progresión A1-B2 (COMPLETADA)
3. ✅ **Fase 3**: Chatbot contextual por situaciones reales (COMPLETADA)
4. ✅ **Fase 4**: Memoria conversacional y aprendizaje guiado (COMPLETADA)
5. **Fase 5**: Motor neuronal de selección y priorización
6. **Fase 6**: Frontend web + API + persistencia SQL
7. **Fase 7**: Sistema de progreso, recompensas y personalización

## 🧭 Roadmap Contextual

El objetivo del siguiente ciclo es que el bot enseñe por contexto, no por clases aisladas. La prioridad no es hacerlo "más grande", sino hacerlo más útil, natural y adaptable.

### Fase 3: Chatbot contextual por situaciones reales
- Objetivo: enseñar frases útiles según intención y escenario.
- Ejemplos: videojuegos-coordinación, pedir ayuda, despedirse, expresar sentimientos, urgencia, trabajo en equipo.
- Entregables: catálogo de contextos, frases por contexto, variantes naturales, explicación de uso y tono.
- Criterio de éxito: el usuario puede pedir una intención y recibir frases correctas, variantes y contexto de uso.

### Fase 4: Memoria conversacional y aprendizaje guiado
- Objetivo: guardar conversaciones y convertirlas en material reutilizable.
- Entregables: historial de conversaciones, detección de intenciones, correcciones guardadas, frases aprobadas para incorporar.
- Criterio de éxito: el sistema mejora con el uso sin romper respuestas ya validadas.

### Fase 5: Motor neuronal de selección y priorización
- Objetivo: usar la neurona para decidir qué mostrar, no para inventar todo desde cero.
- Entradas: contexto, intención, nivel, historial, confianza, variabilidad de respuestas.
- Entregables: clasificación de intención, ranking de frases, predicción de dificultad y progreso.
- Criterio de éxito: las respuestas cambian según el usuario, pero siguen siendo naturales y consistentes.

### Fase 6: Frontend web + API + persistencia SQL
- Objetivo: sacar el flujo de consola y llevarlo a una interfaz web utilizable.
- Entregables: frontend, API REST, almacenamiento en base de datos, autenticación básica si hace falta.
- Criterio de éxito: el bot se puede usar de forma continua desde navegador.

### Fase 7: Sistema de progreso, recompensas y personalización
- Objetivo: hacer visible el avance del usuario.
- Entregables: streaks, badges, progreso por contexto, recomendaciones personalizadas.
- Criterio de éxito: el usuario siente progreso real y rutas de aprendizaje claras.

## 🎯 Primera Prioridad Real

Si vamos a avanzar ordenadamente, el siguiente paso técnico debe ser Fase 3: contexto y variantes naturales. Antes de ampliar neuronas, hay que ampliar el mapa de situaciones, intenciones y frases útiles.

## 🤝 Contribuir

Las ramas feature son independientes. Para agregar funcionalidad:

```bash
git checkout -b feature/tu-funcionalidad
# ... desarrollo ...
git commit -m "feat: descripción"
git push origin feature/tu-funcionalidad
```

## 📝 Documentación

- [FASE1_BASE.md](FASE1_BASE.md) - Arquitectura base del chatbot
- [FASE2_RED_NEURONAL.md](FASE2_RED_NEURONAL.md) - Red neuronal y progresión
- [PLAN_FASES.md](PLAN_FASES.md) - Roadmap contextual del proyecto
- [FASE3_CONTEXTO.md](FASE3_CONTEXTO.md) - Definición técnica de aprendizaje por contexto

## 📄 Licencia

Proyecto educativo - Libre para uso y modificación.

---

**Estado del Proyecto**: 🟢 En desarrollo activo

Última actualización: 2 de junio de 2026

