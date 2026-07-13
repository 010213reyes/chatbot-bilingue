# Fase 4: Memoria Conversacional y Aprendizaje Guiado

## Objetivo

Que el chatbot recuerde conversaciones anteriores y aprenda de las correcciones del usuario, sin corromper la base contextual ya establecida.

## Qué debe resolver

Actualmente, el chatbot es stateless: olvida cada sesión. Fase 4 agrega:
- el usuario hace una pregunta,
- el chatbot responde,
- el usuario corrige ("no, se dice así"),
- el chatbot guarda eso como retroalimentación,
- después, puede proponer que se añada a la base si es válido.

## Principios de diseño

### 1. Memoria per-usuario
Cada usuario tiene su conversación guardada en archivos JSON separados bajo `data/user_conversations/`.

### 2. Intención explícita en contexto
Cada mensaje del usuario se analiza para extraer:
- intención (ej: "pedir ayuda", "saludar", "coordinar")
- contexto implícito (ej: "videojuegos_batalla", "saludo_básico")
- confianza de la detección (0–1)

### 3. Correcciones como tuplas (propuesta, corrección)
Cuando el usuario dice "no, se dice X, no Y", guardamos:
```json
{
  "user_input": "no se dice así",
  "timestamp": "2026-07-13T10:30:00",
  "original_response": "Do you want to play?",
  "user_correction": "Do you want to play with me?",
  "context": "videojuegos_general",
  "intention": "invitation",
  "confidence": 0.85
}
```

### 4. Revisión y validación
Antes de que una corrección se incorpore al catálogo base, debe pasar por:
- validación de formato,
- revisión de coherencia contexto-frase,
- filtro de spam o sin sentido.

### 5. No se sobrescriben contextos base
Las nuevas frases se guardan en `data/learned_phrases.json`, separadas del archivo principal de contextos.

## Estructura de datos

### Conversación de usuario
Archivo: `data/user_conversations/{user_id}/history.json`

```json
{
  "user_id": "juan",
  "created_at": "2026-07-10T09:00:00",
  "language_level": "A2",
  "conversations": [
    {
      "session_id": "s001",
      "timestamp": "2026-07-13T10:00:00",
      "messages": [
        {
          "role": "user",
          "content": "¿cómo se dice 'sígueme'?",
          "timestamp": "2026-07-13T10:00:05",
          "detected_intention": "translation_request",
          "detected_context": "videojuegos_coordinacion",
          "confidence": 0.92
        },
        {
          "role": "assistant",
          "content": "Follow me",
          "timestamp": "2026-07-13T10:00:10",
          "suggested_phrases": ["Follow me", "Come with me"]
        },
        {
          "role": "user",
          "content": "ok, gracias",
          "timestamp": "2026-07-13T10:00:15",
          "is_correction": false,
          "feedback_type": "acknowledgment"
        }
      ]
    }
  ]
}
```

### Correcciones propuestas
Archivo: `data/learned_phrases.json`

```json
{
  "proposed_corrections": [
    {
      "id": "pc001",
      "user_id": "juan",
      "session_id": "s001",
      "timestamp": "2026-07-13T10:30:00",
      "original_chatbot_response": "Do you want to play?",
      "user_correction": "Do you want to play with me?",
      "context": "videojuegos_general",
      "intention": "invitation",
      "confidence": 0.85,
      "status": "pending",
      "review_timestamp": null,
      "reviewer_notes": ""
    }
  ],
  "approved_phrases": [
    {
      "id": "ap001",
      "context": "videojuegos_coordinacion",
      "es": "Espera aquí",
      "en": "Wait here",
      "approved_by_user": "admin",
      "approved_at": "2026-07-13T11:00:00",
      "source_correction_id": "pc001",
      "usage_count": 0
    }
  ]
}
```

## Componentes a implementar

### 1. Modelo de Conversación
Archivo: `src/models/memory/conversation_message.py`

- `Message` — una línea de chat (usuario o asistente)
- `Conversation` — una sesión de conversación (lista de mensajes)
- `UserConversationHistory` — historial completo de un usuario

### 2. Modelo de Intención Detectada
Archivo: `src/models/memory/detected_intention.py`

- `DetectedIntention` — resultado del análisis de intención
  - `intention`: str (ej: "translation_request", "context_teaching")
  - `context`: str (ej: "videojuegos_coordinacion")
  - `confidence`: float (0–1)

### 3. Modelo de Corrección
Archivo: `src/models/memory/correction.py`

- `ProposedCorrection` — corrección pendiente de revisión
- `ApprovedPhrase` — frase que ya pasó revisión y está lista para el catálogo

### 4. Servicio de Memoria
Archivo: `src/services/memory_service.py`

- `save_message(user_id, session_id, role, content, intention, context, confidence)`
- `get_conversation_history(user_id, limit=50)`
- `detect_correction_attempt(user_message, last_bot_response)` → `bool`

### 5. Servicio de Intención
Archivo: `src/services/intention_detector_service.py`

- `detect_intention(user_message)` → `DetectedIntention`
  - usa similitud con frases conocidas,
  - mapea a contextos registrados,
  - devuelve confianza de detección.

### 6. Servicio de Correcciones
Archivo: `src/services/correction_validator_service.py`

- `propose_correction(user_id, original_response, correction, context, intention)`
- `list_pending_corrections()`
- `approve_correction(correction_id, reviewer_id)` → incorpora a `learned_phrases.json`
- `reject_correction(correction_id, reason)`

## Flujo de interacción

1. **Usuario inicia sesión** → cargamos su historial desde `data/user_conversations/{user_id}/history.json`
2. **Usuario pregunta algo** → detectamos intención y contexto
3. **Chatbot responde** → registramos respuesta en la conversación
4. **Usuario reacciona**:
   - Si es aprobación: guardar como retroalimentación positiva
   - Si es corrección: guardar como `ProposedCorrection` con estado `pending`
   - Si es pregunta nueva: continuar conversación
5. **Admin revisa correcciones** → en un flujo separado, alguien valida y aprueba
6. **Frase aprobada** → se agrega a `learned_phrases.json` y queda disponible para futuras respuestas

## Validaciones de corrección

Una corrección es válida si:
- ✓ No está vacía
- ✓ Tiene sentido gramatical básico en inglés
- ✓ Es coherente con el contexto declarado
- ✓ No es ofensiva o spam
- ✓ No es idéntica a una frase ya en el catálogo

Una corrección se rechaza si:
- ✗ Falla alguna validación arriba
- ✗ El contexto no existe
- ✗ La intención no está mapeada

## Cronograma de implementación

### Semana 1: Modelos de datos
- Crear `src/models/memory/` con dataclasses para conversación, intención, corrección

### Semana 2: Servicios core
- `MemoryService` — guardar/cargar conversaciones
- `IntentionDetectorService` — detectar intención y contexto

### Semana 3: Validación y revisión
- `CorrectionValidatorService` — proponer, validar, aprobar correcciones
- Integración con servicios existentes

### Semana 4: Integración en flujo
- Conectar Fase 4 al chatbot base
- Tests de conversación multi-turno
- Validación end-to-end

## Qué NO es Fase 4

- ❌ No es un LLM entrenado con esas correcciones
- ❌ No es aprendizaje automático en tiempo real
- ❌ No corrompe el catálogo sin validación
- ❌ No almacena mensajes privados indefinidamente (limpieza después de 30 días)

## Qué SÍ es Fase 4

- ✓ Memoria estructurada de conversaciones
- ✓ Detección de intención basada en reglas y similitud
- ✓ Captura de correcciones con validación
- ✓ Un flujo claro de revisión antes de incorporar frases nuevas
- ✓ Base sólida para Fase 5 (red neuronal aprende de esto)

## Dependencias

- Fase 3 (contextos y lecciones): ya completada
- `src/models/contextual/` — para información de contextos
- `src/config/settings.py` — configuración de nivel y contextos
- `data/contexts.json` — catálogo base

## Criterio de éxito

- [ ] Cada usuario tiene un historial guardado en `data/user_conversations/`
- [ ] Cada mensaje registra intención y contexto con confianza
- [ ] Las correcciones se proponen sin corromper el catálogo base
- [ ] Un flujo admin puede revisar y aprobar correcciones
- [ ] El chatbot incorpora frases aprobadas en respuestas futuras
- [ ] Tests verifican memoria, intención y validación de correcciones
