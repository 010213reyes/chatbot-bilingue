# Chatbot Bilingüe - Tutor de Inglés con Red Neuronal

Chatbot inteligente basado en redes neuronales para enseñanza contextual de inglés. Responde en español, enseña inglés con profesionalismo desde A1 hasta B2.

## 🎯 Características

✅ **Aprendizaje Contextual**: Frases en situaciones reales (videojuegos, chats en línea, etc.)  
✅ **Niveles Adaptativos**: A1 → A2 → B1 → B2 (CEFR)  
✅ **Red Neuronal**: Clasifica nivel del usuario automáticamente  
✅ **Evaluación Adaptativa**: Quiz inicial para determinar nivel  
✅ **Rastreo de Progreso**: Persistencia JSON, estadísticas, spaced repetition  
✅ **Responde en Español**: Base en español, guía progresiva hacia inglés  

## 📋 Estructura del Proyecto

```
chatbot-bilingue/
├── src/
│   ├── config/
│   │   └── settings.py              # Config centralizada
│   ├── models/
│   │   ├── context_manager.py       # Gestor de contextos
│   │   ├── levels/
│   │   │   ├── level_manager.py     # Gestión A1-B2
│   │   │   └── level_mapper.py      # Mapeo frases→niveles
│   │   └── neural/
│   │       └── level_classifier.py  # Red neuronal + clasificador
│   ├── services/
│   │   ├── evaluation_service.py    # Quiz evaluativo
│   │   └── progress_tracker.py      # Rastreo usuario
│   ├── chatbot.py                   # Chatbot base (español)
│   └── advanced_chatbot.py          # Chatbot avanzado (NN + progresión)
├── data/
│   ├── contexts.json                # Base de frases y contextos
│   ├── levels/                      # Frases por nivel
│   └── user_progress/               # Progreso de usuarios
├── FASE1_BASE.md                    # Documentación fase 1
├── FASE2_RED_NEURONAL.md            # Documentación fase 2
└── requirements.txt
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

### Chatbot Avanzado (Neutral Network + Progresión)
```bash
python src/advanced_chatbot.py
```

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
3. **Fase 3**: Frontend web (Flask)
4. **Fase 4**: API REST + persistencia SQL
5. **Fase 5**: Sistema de recompensas (badges, streak counter)

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

## 📄 Licencia

Proyecto educativo - Libre para uso y modificación.

---

**Estado del Proyecto**: 🟢 En desarrollo activo

Última actualización: 2 de junio de 2026

