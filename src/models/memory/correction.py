"""
Modelo para representar correcciones propuestas por usuarios.

Fase 4: Captura de correcciones y flujo de validación.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
from enum import Enum


class CorrectionStatus(str, Enum):
    """Estado de una corrección propuesta."""
    PENDING = "pending"  # Esperando revisión
    APPROVED = "approved"  # Aprobada e incorporada
    REJECTED = "rejected"  # Rechazada
    ARCHIVED = "archived"  # Archivada (no usar)


class ValidationIssue(str, Enum):
    """Tipos de problemas en validación."""
    EMPTY = "empty"  # Corrección vacía
    INVALID_ENGLISH = "invalid_english"  # Inglés inválido
    DUPLICATE = "duplicate"  # Ya existe en catálogo
    INCOHERENT = "incoherent"  # No tiene sentido en el contexto
    SPAM = "spam"  # Spam o ofensiva
    OTHER = "other"  # Otro problema


@dataclass
class ProposedCorrection:
    """
    Una corrección propuesta por un usuario que debe ser validada.
    
    Attributes:
        id: identificador único de la corrección
        user_id: quién propuso la corrección
        session_id: en qué sesión
        timestamp: cuándo se propuso
        original_chatbot_response: lo que respondió el chatbot
        user_correction: lo que el usuario sugiere
        context: contexto implícito
        intention: intención implícita
        confidence: confianza de la intención
        status: estado actual de la corrección
        validation_issues: problemas encontrados en validación
        review_timestamp: cuándo se revisó (si aplica)
        reviewer_id: quién la revisó (si aplica)
        reviewer_notes: comentarios del revisor
    """
    id: str
    user_id: str
    session_id: str
    timestamp: str  # ISO format
    original_chatbot_response: str
    user_correction: str
    context: str
    intention: str
    confidence: float = 0.0
    status: CorrectionStatus = CorrectionStatus.PENDING
    validation_issues: list = field(default_factory=list)  # List[ValidationIssue]
    review_timestamp: Optional[str] = None
    reviewer_id: Optional[str] = None
    reviewer_notes: str = ""

    def mark_reviewed(self, reviewer_id: str, status: CorrectionStatus, notes: str = ""):
        """Marcar como revisada."""
        self.review_timestamp = datetime.now().isoformat()
        self.reviewer_id = reviewer_id
        self.status = status
        self.reviewer_notes = notes

    def add_validation_issue(self, issue: ValidationIssue):
        """Agregar un problema de validación."""
        if issue not in self.validation_issues:
            self.validation_issues.append(issue)

    @property
    def is_valid(self) -> bool:
        """Determinar si pasó validación (sin problemas)."""
        return len(self.validation_issues) == 0

    def to_dict(self):
        """Serializar a dict."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "original_chatbot_response": self.original_chatbot_response,
            "user_correction": self.user_correction,
            "context": self.context,
            "intention": self.intention,
            "confidence": self.confidence,
            "status": self.status.value,
            "validation_issues": [i.value for i in self.validation_issues],
            "review_timestamp": self.review_timestamp,
            "reviewer_id": self.reviewer_id,
            "reviewer_notes": self.reviewer_notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProposedCorrection":
        """Deserializar desde dict."""
        data = data.copy()
        if isinstance(data.get("status"), str):
            data["status"] = CorrectionStatus(data["status"])
        if data.get("validation_issues"):
            data["validation_issues"] = [
                ValidationIssue(i) if isinstance(i, str) else i
                for i in data["validation_issues"]
            ]
        return cls(**data)


@dataclass
class ApprovedPhrase:
    """
    Una frase que fue aprobada de una corrección y puede ser usada en respuestas.
    
    Attributes:
        id: identificador único
        context: contexto al que pertenece
        es: frase en español
        en: frase en inglés
        approved_by_user: quién aprobó (admin)
        approved_at: cuándo fue aprobada
        source_correction_id: de cuál ProposedCorrection viene
        usage_count: cuántas veces se ha usado
        added_to_catalog: si ya está en contexts.json (True cuando está incorporada)
    """
    id: str
    context: str
    es: str
    en: str
    approved_by_user: str
    approved_at: str  # ISO format
    source_correction_id: str
    usage_count: int = 0
    added_to_catalog: bool = False

    def increment_usage(self):
        """Incrementar contador de uso."""
        self.usage_count += 1

    def mark_added_to_catalog(self):
        """Marcar como ya incorporada al catálogo."""
        self.added_to_catalog = True

    def to_dict(self):
        """Serializar a dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ApprovedPhrase":
        """Deserializar desde dict."""
        return cls(**data)


@dataclass
class CorrectionBatch:
    """
    Un lote de correcciones para revisión en masa.
    
    Attributes:
        batch_id: identificador del lote
        created_at: cuándo se creó
        corrections: lista de correcciones en el lote
        total_corrections: total de correcciones
        pending_count: cuántas siguen pendientes
        status: si el lote está abierto o cerrado
    """
    batch_id: str
    created_at: str  # ISO format
    corrections: list = field(default_factory=list)  # List[ProposedCorrection]
    status: str = "open"  # "open" o "closed"

    @property
    def total_corrections(self) -> int:
        """Contar correcciones."""
        return len(self.corrections)

    @property
    def pending_count(self) -> int:
        """Contar pendientes."""
        return sum(
            1 for c in self.corrections
            if c.status == CorrectionStatus.PENDING
        )

    @property
    def approved_count(self) -> int:
        """Contar aprobadas."""
        return sum(
            1 for c in self.corrections
            if c.status == CorrectionStatus.APPROVED
        )

    def add_correction(self, correction: ProposedCorrection):
        """Agregar una corrección al lote."""
        self.corrections.append(correction)

    def to_dict(self):
        """Serializar a dict."""
        return {
            "batch_id": self.batch_id,
            "created_at": self.created_at,
            "status": self.status,
            "total_corrections": self.total_corrections,
            "pending_count": self.pending_count,
            "approved_count": self.approved_count,
            "corrections": [c.to_dict() for c in self.corrections],
        }
