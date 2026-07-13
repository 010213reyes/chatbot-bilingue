"""
Modelos y constructor para aprendizaje por contexto.

La Fase 3 organiza el contenido por situación, intención y explicación escrita
para que el chatbot enseñe expresiones naturales en lugar de traducciones
puntuales.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ContextualPhrase:
    """Representa una frase contextual con metadatos de uso."""

    es: str
    en: str
    en_alt: List[str] = field(default_factory=list)
    uso: str = ""
    intencion: str = ""
    situacion: str = ""
    nivel: str = "A1"
    explicacion: str = ""
    ejemplos: List[str] = field(default_factory=list)


@dataclass
class ContextualLesson:
    """Lección contextual compuesta por contexto e intenciones."""

    context_id: str
    nombre: str
    descripcion: str
    objetivo: str
    nivel: str
    intenciones: List[str] = field(default_factory=list)
    frases: List[ContextualPhrase] = field(default_factory=list)


class ContextualLessonBuilder:
    """Construye lecciones contextuales a partir de datos crudos."""

    def build_from_context(self, context_id: str, context_data: Dict[str, Any], default_level: str = "A1") -> ContextualLesson:
        """Convierte un bloque de contexto en una lección estructurada."""
        frases: List[ContextualPhrase] = []

        for phrase in context_data.get("frases", []):
            frases.append(
                ContextualPhrase(
                    es=phrase.get("es", ""),
                    en=phrase.get("en", ""),
                    en_alt=phrase.get("en_alt", []),
                    uso=phrase.get("uso", ""),
                    intencion=phrase.get("intencion", phrase.get("uso", "")),
                    situacion=phrase.get("situacion", context_data.get("nombre", "")),
                    nivel=phrase.get("nivel", default_level),
                    explicacion=phrase.get("explicacion", ""),
                    ejemplos=phrase.get("ejemplos", []),
                )
            )

        return ContextualLesson(
            context_id=context_id,
            nombre=context_data.get("nombre", context_id),
            descripcion=context_data.get("descripcion", ""),
            objetivo=context_data.get("objetivo", "Aprender por contexto"),
            nivel=context_data.get("nivel", default_level),
            intenciones=context_data.get("intenciones", []),
            frases=frases,
        )

    def summarize_lesson(self, lesson: ContextualLesson) -> Dict[str, Any]:
        """Devuelve un resumen compacto de la lección."""
        return {
            "contexto": lesson.nombre,
            "nivel": lesson.nivel,
            "objetivo": lesson.objetivo,
            "intenciones": lesson.intenciones,
            "frases": len(lesson.frases),
        }

    def render_text_lesson(self, lesson: ContextualLesson) -> List[str]:
        """Genera una vista textual simple para lectura en pantalla."""
        lines = [f"Contexto: {lesson.nombre}", f"Objetivo: {lesson.objetivo}"]

        for phrase in lesson.frases:
            lines.append(f"- {phrase.es} -> {phrase.en}")
            if phrase.uso:
                lines.append(f"  Uso: {phrase.uso}")
            if phrase.intencion:
                lines.append(f"  Intención: {phrase.intencion}")
            if phrase.situacion:
                lines.append(f"  Situación: {phrase.situacion}")
            if phrase.explicacion:
                lines.append(f"  Explicación: {phrase.explicacion}")
            if phrase.ejemplos:
                lines.append(f"  Ejemplos: {', '.join(phrase.ejemplos)}")

        return lines