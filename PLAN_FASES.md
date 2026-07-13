# Plan de Fases - Chatbot Bilingüe Contextual

Este documento define la ruta del proyecto para que el chatbot enseñe inglés por contexto, intención y uso real, no solo por traducción literal o reglas aisladas.

## Objetivo General

Convertir el sistema en un tutor contextual que:
- detecte la intención del usuario,
- enseñe frases naturales según la situación,
- explique por qué se usa cada expresión,
- aprenda de conversaciones y correcciones,
- y use la red neuronal para priorizar, no para reemplazar el criterio pedagógico.

## Fase 3: Chatbot contextual por situaciones reales

### Meta
Enseñar por escenarios prácticos: videojuegos, sentimientos, trabajo en equipo, despedidas, ayuda, urgencia y coordinación.

### Qué debe tener
- Catálogo de contextos con nombre, propósito y nivel.
- Frases base por contexto.
- Variantes naturales para cada frase.
- Explicación de uso, tono y cuándo conviene usarla.
- Ejemplos de conversación que no suenen a clase tradicional.

### Resultado esperado
El usuario dice una intención y el bot responde con expresiones útiles, naturales y contextualizadas.

## Fase 4: Memoria conversacional y aprendizaje guiado

### Meta
Guardar conversaciones y convertirlas en conocimiento útil sin corromper la base del sistema.

### Qué debe tener
- Registro de conversaciones por usuario.
- Detección de intención y contexto implícito.
- Correcciones del usuario como señal de aprendizaje.
- Flujo de revisión antes de incorporar frases nuevas.

### Resultado esperado
El chatbot mejora con el uso y puede incorporar frases nuevas solo después de validarlas.

## Fase 5: Motor neuronal de selección y priorización

### Meta
Usar la neurona para decidir qué enseñar, qué reforzar y qué frase conviene mostrar.

### Qué debe tener
- Clasificación de intención.
- Priorización de frases y contextos.
- Estimación de dificultad.
- Señales de progreso más ricas que un simple score.
- Datos de entrenamiento con contexto, tono, nivel y variación.

### Resultado esperado
Las respuestas no serán puntuales ni repetitivas, pero seguirán controladas y coherentes.

## Fase 6: Frontend web + API + persistencia SQL

### Meta
Sacar el producto de la consola y llevarlo a una experiencia usable en navegador.

### Qué debe tener
- Interfaz web clara.
- API para chat, progreso y evaluación.
- Persistencia SQL para usuarios, sesiones y frases aprendidas.
- Posible autenticación simple.

### Resultado esperado
El proyecto se convierte en una aplicación real y no solo en una demo de terminal.

## Fase 7: Progreso, recompensas y personalización

### Meta
Hacer visible el avance y mantener motivación.

### Qué debe tener
- Streaks.
- Badges.
- Progreso por contexto.
- Recomendaciones personalizadas.
- Repaso inteligente según desempeño.

### Resultado esperado
El usuario siente evolución constante y sabe qué aprender después.

## Orden recomendado

1. Fase 3: contextos y variantes naturales.
2. Fase 4: memoria y aprendizaje guiado.
3. Fase 5: neurona para selección y priorización.
4. Fase 6: frontend, API y base de datos.
5. Fase 7: recompensas y personalización.

## Regla de decisión

Antes de agrandar la red neuronal, el sistema debe tener:
- datos mejores,
- contextos más ricos,
- evaluaciones más útiles,
- y memoria conversacional validada.

Si eso no existe, más neuronas no aportan valor real.