"""
Paquete de modelos para Fase 4: Memoria Conversacional.

Exporta los dataclasses y enums para conversaciones, intenciones y correcciones.
"""

from .conversation_message import (
    Message,
    MessageRole,
    FeedbackType,
    Conversation,
    UserConversationHistory,
)

from .detected_intention import (
    DetectedIntention,
    COMMON_INTENTIONS,
)

from .correction import (
    ProposedCorrection,
    ApprovedPhrase,
    CorrectionBatch,
    CorrectionStatus,
    ValidationIssue,
)

__all__ = [
    # Conversation
    "Message",
    "MessageRole",
    "FeedbackType",
    "Conversation",
    "UserConversationHistory",
    # Intention
    "DetectedIntention",
    "COMMON_INTENTIONS",
    # Correction
    "ProposedCorrection",
    "ApprovedPhrase",
    "CorrectionBatch",
    "CorrectionStatus",
    "ValidationIssue",
]
