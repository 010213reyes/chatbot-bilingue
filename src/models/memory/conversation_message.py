"""
Modelos para representar conversaciones y mensajes en la Fase 4.

Almacena el historial de interacciones del usuario con el chatbot.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List
from enum import Enum


class MessageRole(str, Enum):
    """Rol del que genera el mensaje."""
    USER = "user"
    ASSISTANT = "assistant"


class FeedbackType(str, Enum):
    """Tipo de retroalimentación del usuario."""
    ACKNOWLEDGMENT = "acknowledgment"  # "ok, gracias"
    CORRECTION = "correction"  # "no, se dice..."
    CLARIFICATION = "clarification"  # "¿qué significa?"
    APPRECIATION = "appreciation"  # "perfecto", "gracias"
    CONFUSION = "confusion"  # "no entiendo"
    OTHER = "other"


@dataclass
class Message:
    """
    Un mensaje individual en una conversación.
    
    Attributes:
        role: quién envía (USER o ASSISTANT)
        content: texto del mensaje
        timestamp: cuándo se envió
        detected_intention: intención detectada (si es del usuario)
        detected_context: contexto implícito (si es del usuario)
        confidence: confianza de la detección de intención (0-1)
        suggested_phrases: frases sugeridas por el chatbot (si es ASSISTANT)
        is_correction: si el usuario está corrigiendo algo
        feedback_type: tipo de retroalimentación (si es USER)
    """
    role: MessageRole
    content: str
    timestamp: str  # ISO format
    detected_intention: Optional[str] = None
    detected_context: Optional[str] = None
    confidence: float = 0.0
    suggested_phrases: List[str] = field(default_factory=list)
    is_correction: bool = False
    feedback_type: Optional[FeedbackType] = None

    def to_dict(self):
        """Serializar a dict para JSON."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Deserializar desde dict."""
        if isinstance(data.get("role"), str):
            data["role"] = MessageRole(data["role"])
        if data.get("feedback_type") and isinstance(data["feedback_type"], str):
            data["feedback_type"] = FeedbackType(data["feedback_type"])
        return cls(**data)


@dataclass
class Conversation:
    """
    Una sesión de conversación entre un usuario y el chatbot.
    
    Attributes:
        session_id: identificador único de la sesión
        user_id: a quién pertenece
        timestamp: cuándo inició
        messages: lista de mensajes en orden cronológico
        language_level: nivel detectado o del usuario en esa sesión
        context_focus: contexto principal de la sesión (ej: "videojuegos_coordinacion")
    """
    session_id: str
    user_id: str
    timestamp: str  # ISO format
    messages: List[Message] = field(default_factory=list)
    language_level: Optional[str] = None
    context_focus: Optional[str] = None

    def add_message(self, message: Message) -> None:
        """Agregar un mensaje a la conversación."""
        self.messages.append(message)

    def get_last_user_message(self) -> Optional[Message]:
        """Obtener el último mensaje del usuario."""
        for msg in reversed(self.messages):
            if msg.role == MessageRole.USER:
                return msg
        return None

    def get_last_assistant_message(self) -> Optional[Message]:
        """Obtener la última respuesta del chatbot."""
        for msg in reversed(self.messages):
            if msg.role == MessageRole.ASSISTANT:
                return msg
        return None

    def to_dict(self):
        """Serializar a dict."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "language_level": self.language_level,
            "context_focus": self.context_focus,
            "messages": [msg.to_dict() for msg in self.messages],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Conversation":
        """Deserializar desde dict."""
        messages = [Message.from_dict(m) for m in data.get("messages", [])]
        return cls(
            session_id=data["session_id"],
            user_id=data["user_id"],
            timestamp=data["timestamp"],
            messages=messages,
            language_level=data.get("language_level"),
            context_focus=data.get("context_focus"),
        )


@dataclass
class UserConversationHistory:
    """
    Historial completo de conversaciones de un usuario.
    
    Attributes:
        user_id: identificador único del usuario
        created_at: cuándo se creó la historia
        language_level: nivel del usuario (puede actualizarse)
        total_conversations: cuántas sesiones ha tenido
        conversations: lista de conversaciones
    """
    user_id: str
    created_at: str  # ISO format
    language_level: str
    conversations: List[Conversation] = field(default_factory=list)

    @property
    def total_conversations(self) -> int:
        """Contar conversaciones."""
        return len(self.conversations)

    def add_conversation(self, conversation: Conversation) -> None:
        """Agregar una conversación."""
        self.conversations.append(conversation)

    def get_conversation(self, session_id: str) -> Optional[Conversation]:
        """Buscar una conversación por session_id."""
        for conv in self.conversations:
            if conv.session_id == session_id:
                return conv
        return None

    def get_latest_conversations(self, limit: int = 10) -> List[Conversation]:
        """Obtener las últimas N conversaciones."""
        return sorted(
            self.conversations,
            key=lambda c: c.timestamp,
            reverse=True
        )[:limit]

    def to_dict(self):
        """Serializar a dict."""
        return {
            "user_id": self.user_id,
            "created_at": self.created_at,
            "language_level": self.language_level,
            "total_conversations": self.total_conversations,
            "conversations": [c.to_dict() for c in self.conversations],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserConversationHistory":
        """Deserializar desde dict."""
        conversations = [
            Conversation.from_dict(c)
            for c in data.get("conversations", [])
        ]
        return cls(
            user_id=data["user_id"],
            created_at=data["created_at"],
            language_level=data["language_level"],
            conversations=conversations,
        )
