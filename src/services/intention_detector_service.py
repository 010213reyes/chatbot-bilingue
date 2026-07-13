"""
Servicio de detección de intención para Fase 4.

Analiza mensajes del usuario para detectar intención y contexto implícito.
"""

from typing import Optional, List, Dict
from difflib import SequenceMatcher
import json

from src.models.memory import DetectedIntention, COMMON_INTENTIONS
from src.models.context_manager import ContextManager


class IntentionDetectorService:
    """
    Servicio para detectar la intención y contexto implícito en mensajes del usuario.
    
    Estrategia:
    1. Palabras clave heurísticas (traduce, enseña, ayuda, etc.)
    2. Similitud textual con frases conocidas en los contextos
    3. Contexto de conversación anterior
    4. Confianza basada en múltiples señales
    """

    def __init__(self, contexts_path: str = "data/contexts.json"):
        """
        Inicializar el detector.
        
        Args:
            contexts_path: ruta al archivo de contextos
        """
        self.context_manager = ContextManager(contexts_path)
        self.all_phrases = self._build_phrase_index()
        self.keyword_patterns = self._build_keyword_patterns()

    def _build_phrase_index(self) -> Dict[str, List[str]]:
        """
        Construir índice de todas las frases por contexto.
        
        Returns:
            Dict con estructura: {context_id: [lista de frases en español]}
        """
        index = {}
        context_ids = self.context_manager.list_contexts()

        for context_id in context_ids:
            context = self.context_manager.get_context(context_id)
            if context:
                phrases = []
                if "frases" in context:
                    phrases = [f.get("es", "").lower() for f in context["frases"]]
                index[context_id] = phrases

        return index

    def _build_keyword_patterns(self) -> Dict[str, List[str]]:
        """
        Construir patrones de palabras clave para cada intención.
        
        Returns:
            Dict con: {intention: [palabras clave]}
        """
        return {
            "translation_request": [
                "cómo se dice",
                "traduce",
                "traducción de",
                "en inglés",
                "¿se dice",
                "cuál es la palabra",
            ],
            "teaching_request": [
                "enseña",
                "quiero aprender",
                "cómo se usa",
                "explica",
                "más sobre",
            ],
            "clarification": [
                "qué significa",
                "no entiendo",
                "puedes aclarar",
                "no comprendo",
                "qué quiere decir",
            ],
            "correction": [
                "no, se dice",
                "la forma correcta",
                "debería ser",
                "no es así",
                "la forma correcta es",
            ],
            "practice": [
                "practicar",
                "ejercicio",
                "quiz",
                "test",
                "prueba",
            ],
            "context_help": [
                "contexto",
                "en qué caso",
                "cuándo se usa",
                "en qué situación",
            ],
            "status_check": [
                "mi progreso",
                "cuánto he aprendido",
                "qué sigue",
                "nivel",
            ],
            "greeting": [
                "hola",
                "buenos días",
                "buenas noches",
                "qué tal",
            ],
            "farewell": [
                "adiós",
                "hasta luego",
                "nos vemos",
                "chao",
            ],
        }

    def detect_intention(
        self,
        user_message: str,
        previous_context: Optional[str] = None,
    ) -> DetectedIntention:
        """
        Detectar la intención y contexto en un mensaje del usuario.
        
        Args:
            user_message: el mensaje a analizar
            previous_context: contexto de la conversación anterior (opcional)
            
        Returns:
            DetectedIntention: intención, contexto y confianza
        """
        message_lower = user_message.lower()

        # Paso 1: Detectar intención por palabras clave
        intention, keyword_confidence = self._detect_by_keywords(message_lower)

        # Paso 2: Detectar contexto por similitud textual
        context, similarity_confidence = self._detect_by_similarity(
            message_lower, previous_context
        )

        # Paso 3: Combinar confianzas
        final_confidence = (keyword_confidence + similarity_confidence) / 2

        # Paso 4: Generar explicación
        explanation = self._generate_explanation(
            intention, context, keyword_confidence, similarity_confidence
        )

        return DetectedIntention(
            intention=intention,
            context=context,
            confidence=final_confidence,
            explanation=explanation,
        )

    def _detect_by_keywords(
        self, message_lower: str
    ) -> tuple[str, float]:
        """
        Detectar intención por palabras clave.
        
        Returns:
            (intention: str, confidence: float)
        """
        matches = {}

        for intention, keywords in self.keyword_patterns.items():
            match_count = sum(
                1 for keyword in keywords if keyword in message_lower
            )
            if match_count > 0:
                matches[intention] = match_count

        if not matches:
            return "other", 0.3

        # Intención con más coincidencias
        best_intention = max(matches, key=matches.get)
        max_matches = matches[best_intention]
        confidence = min(max_matches / 3, 1.0)  # Normalizar a 0-1

        return best_intention, confidence

    def _detect_by_similarity(
        self,
        message_lower: str,
        previous_context: Optional[str] = None,
    ) -> tuple[str, float]:
        """
        Detectar contexto por similitud textual con frases conocidas.
        
        Returns:
            (context: str, confidence: float)
        """
        best_context = previous_context or "saludo_basico"
        best_score = 0.0

        # Buscar en cada contexto
        for context_id, phrases in self.all_phrases.items():
            for phrase in phrases:
                similarity = SequenceMatcher(
                    None, message_lower, phrase
                ).ratio()
                if similarity > best_score:
                    best_score = similarity
                    best_context = context_id

        # Confianza: cuán similar es al mejor match
        confidence = max(best_score, 0.5) if best_score > 0.3 else 0.3

        return best_context, confidence

    def _generate_explanation(
        self,
        intention: str,
        context: str,
        keyword_conf: float,
        similarity_conf: float,
    ) -> str:
        """Generar una explicación breve de la detección."""
        intent_desc = COMMON_INTENTIONS.get(intention, "Intención desconocida")
        parts = [f"Intención: {intent_desc}"]

        if keyword_conf > 0.6:
            parts.append("(detectada por palabras clave)")

        if similarity_conf > 0.6:
            parts.append(f"Contexto probable: {context}")

        return " ".join(parts)

    def update_intention_from_user_feedback(
        self,
        current_intention: DetectedIntention,
        user_feedback: str,
    ) -> DetectedIntention:
        """
        Actualizar la intención basándose en retroalimentación del usuario.
        
        Ejemplo: si el usuario dice "no, quería enseñanza", actualizamos a teaching_request.
        
        Args:
            current_intention: intención actual
            user_feedback: feedback del usuario
            
        Returns:
            DetectedIntention actualizada
        """
        # Re-detectar con el feedback
        new_intention = self.detect_intention(user_feedback)
        return new_intention
