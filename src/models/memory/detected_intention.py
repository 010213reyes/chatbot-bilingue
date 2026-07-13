"""
Modelo para representar la intención detectada en un mensaje del usuario.

Fase 4: Detección de intención y contexto implícito.
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class DetectedIntention:
    """
    Resultado del análisis de intención en un mensaje del usuario.
    
    Attributes:
        intention: la intención principal (ej: "translation_request", "teaching_request", "clarification")
        context: el contexto implícito (ej: "videojuegos_coordinacion", "saludo_basico")
        confidence: confianza del análisis (0.0 a 1.0)
        explanation: breve explicación de por qué se detectó esta intención
        alternative_intentions: otras posibles intenciones con menor confianza
    """
    intention: str
    context: str
    confidence: float
    explanation: str = ""
    alternative_intentions: dict = None  # {intention_name: confidence}

    def __post_init__(self):
        """Validar que la confianza esté entre 0 y 1."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        if self.alternative_intentions is None:
            self.alternative_intentions = {}

    @property
    def is_high_confidence(self) -> bool:
        """Determinar si la confianza es alta (> 0.8)."""
        return self.confidence > 0.8

    @property
    def is_medium_confidence(self) -> bool:
        """Determinar si la confianza es media (0.5-0.8)."""
        return 0.5 <= self.confidence <= 0.8

    @property
    def is_low_confidence(self) -> bool:
        """Determinar si la confianza es baja (< 0.5)."""
        return self.confidence < 0.5

    def to_dict(self):
        """Serializar a dict para JSON."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DetectedIntention":
        """Deserializar desde dict."""
        return cls(**data)


# Intentiones comunes
COMMON_INTENTIONS = {
    "translation_request": "El usuario pide traducción de una frase",
    "teaching_request": "El usuario quiere aprender algo nuevo",
    "clarification": "El usuario pide aclaración sobre algo",
    "confirmation": "El usuario confirma que entendió",
    "correction": "El usuario corrige algo que el chatbot dijo",
    "practice": "El usuario quiere practicar",
    "context_help": "El usuario pide ayuda contextual",
    "status_check": "El usuario pregunta su progreso",
    "greeting": "El usuario saluda",
    "farewell": "El usuario se despide",
    "other": "Otra intención no clasificada",
}
