"""
Servicio para construir lecciones textuales por contexto.

Esta capa permite convertir el catálogo de contexts.json en lecciones legibles
por pantalla con intención, situación, ejemplos y explicación escrita.
"""

from typing import Dict, List, Optional

from src.models.contextual.contextual_lesson import ContextualLesson, ContextualLessonBuilder
from src.models.context_manager import ContextManager


class ContextualLessonService:
    """Construye lecciones contextuales a partir del catálogo actual."""

    def __init__(self, contexts_file: str):
        self.context_manager = ContextManager(contexts_file)
        self.builder = ContextualLessonBuilder()

    def get_lesson(self, context_id: str, default_level: str = "A1") -> Optional[ContextualLesson]:
        """Devuelve una lección contextual completa."""
        context_data = self.context_manager.get_context(context_id)
        if not context_data:
            return None

        return self.builder.build_from_context(context_id, context_data, default_level=default_level)

    def get_text_lesson(self, context_id: str, default_level: str = "A1") -> List[str]:
        """Devuelve la lección como líneas de texto listas para mostrar."""
        lesson = self.get_lesson(context_id, default_level=default_level)
        if not lesson:
            return ["Contexto no encontrado"]

        return self.builder.render_text_lesson(lesson)

    def list_lesson_summaries(self) -> List[Dict]:
        """Devuelve un resumen textual de todos los contextos."""
        summaries = []
        for context_id in self.context_manager.list_contexts():
            lesson = self.get_lesson(context_id)
            if lesson:
                summaries.append(self.builder.summarize_lesson(lesson))
        return summaries