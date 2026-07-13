# Fase 3: Chatbot Contextual por Situaciones Reales

## Objetivo

Construir una capa de aprendizaje que enseñe inglés por intención, situación y explicación escrita, no por clases aisladas de gramática.

## Qué debe resolver

El usuario no debe preguntar solo "cómo se traduce X", sino también:
- cómo pedir cobertura en un juego,
- cómo decir que está ocupado,
- cómo pedir que esperen,
- cómo expresar sentimientos,
- cómo coordinar un equipo,
- y qué frase suena más natural en cada caso.

## Principio de diseño

Cada contexto debe enseñar:
- intención,
- situación,
- frase principal,
- variantes naturales,
- explicación de uso,
- y nivel recomendado.

## Estructura mínima de un contexto

```json
{
  "id": "videojuegos_coordinacion",
  "nombre": "Videojuegos - Coordinación",
  "descripcion": "Frases para dirigir y coordinar al equipo",
  "objetivo": "Aprender frases útiles para dar instrucciones",
  "nivel": "A2",
  "intenciones": ["coordinar", "pedir apoyo", "dar instrucciones"],
  "frases": [
    {
      "es": "Síganme",
      "en": "Follow me",
      "en_alt": ["Come with me", "Let's go"],
      "uso": "Dirigir al equipo",
      "situacion": "partida en equipo",
      "explicacion": "Se usa para indicar movimiento conjunto"
    }
  ]
}
```

## Primer alcance de implementación

1. Definir modelos de contexto y frase contextual.
2. Crear un constructor que convierta los datos actuales en lecciones estructuradas.
3. Etiquetar cada frase con intención, situación y explicación.
4. Permitir que el chatbot responda con variantes naturales, no con una sola traducción fija.
5. Preparar la base para memoria conversacional futura.

## Criterio de éxito

La fase 3 estará lista cuando el sistema pueda:
- recibir una intención,
- ubicar el contexto correcto,
- enseñar una frase natural,
- explicar cuándo se usa,
- y ofrecer variantes válidas según situación.

## Qué no hace todavía

Esta fase no entrena una neurona nueva ni genera texto libre sin control.
Primero ordena el conocimiento y la enseñanza contextual.