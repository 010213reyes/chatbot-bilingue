"""
Servicio de validación y gestión de correcciones para Fase 4.

Propone, valida, aprueba y rechaza correcciones del usuario.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from uuid import uuid4

from src.models.memory import (
    ProposedCorrection,
    ApprovedPhrase,
    CorrectionStatus,
    ValidationIssue,
    CorrectionBatch,
)
from src.models.context_manager import ContextManager


class CorrectionValidatorService:
    """
    Servicio para gestionar el flujo de correcciones propuestas por usuarios.
    
    Persistencia:
    - data/learned_phrases.json: contiene correcciones propuestas y aprobadas
    
    Flujo:
    1. Usuario propone una corrección
    2. Se valida automáticamente
    3. Si es válida, se marca como "pending"
    4. Admin la revisa y aprueba/rechaza
    5. Si se aprueba, se agrega a contexts.json y se marca como added_to_catalog
    """

    def __init__(
        self,
        learned_phrases_path: str = "data/learned_phrases.json",
        contexts_path: str = "data/contexts.json",
    ):
        """
        Inicializar el validador.
        
        Args:
            learned_phrases_path: ruta al archivo de correcciones
            contexts_path: ruta al archivo de contextos
        """
        self.learned_phrases_path = learned_phrases_path
        self.context_manager = ContextManager(contexts_path)
        self._ensure_learned_phrases_file()

    def _ensure_learned_phrases_file(self) -> None:
        """Crear el archivo si no existe."""
        path = Path(self.learned_phrases_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            initial_data = {
                "proposed_corrections": [],
                "approved_phrases": [],
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)

    def _load_learned_phrases(self) -> dict:
        """Cargar el archivo de correcciones."""
        with open(self.learned_phrases_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_learned_phrases(self, data: dict) -> None:
        """Guardar el archivo de correcciones."""
        with open(self.learned_phrases_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def propose_correction(
        self,
        user_id: str,
        session_id: str,
        original_chatbot_response: str,
        user_correction: str,
        context: str,
        intention: str,
        confidence: float = 0.8,
    ) -> ProposedCorrection:
        """
        Proponer una nueva corrección.
        
        Args:
            user_id: quién propone
            session_id: en qué sesión
            original_chatbot_response: lo que dijo el chatbot
            user_correction: lo que el usuario sugiere
            context: contexto asociado
            intention: intención detectada
            confidence: confianza de la intención
            
        Returns:
            ProposedCorrection: la corrección propuesta (sin validar aún)
        """
        correction_id = f"pc_{uuid4().hex[:8]}"

        correction = ProposedCorrection(
            id=correction_id,
            user_id=user_id,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            original_chatbot_response=original_chatbot_response,
            user_correction=user_correction,
            context=context,
            intention=intention,
            confidence=confidence,
            status=CorrectionStatus.PENDING,
        )

        # Validar automáticamente
        self._validate_correction(correction)

        # Guardar
        data = self._load_learned_phrases()
        data["proposed_corrections"].append(correction.to_dict())
        self._save_learned_phrases(data)

        return correction

    def _validate_correction(self, correction: ProposedCorrection) -> None:
        """
        Validar una corrección y agregar issues si es necesario.
        
        Modifica correction.validation_issues in-place.
        """
        issues = []

        # Validación 1: No está vacía
        if not correction.user_correction or not correction.user_correction.strip():
            issues.append(ValidationIssue.EMPTY)

        # Validación 2: Contexto existe
        try:
            self.context_manager.get_context(correction.context)
        except ValueError:
            issues.append(ValidationIssue.OTHER)  # Contexto no existe

        # Validación 3: No es duplicada
        if self._is_duplicate(correction):
            issues.append(ValidationIssue.DUPLICATE)

        # Validación 4: Básica de inglés (no es spam)
        if self._is_likely_spam(correction.user_correction):
            issues.append(ValidationIssue.SPAM)

        # Validación 5: Coherencia con contexto
        if not self._is_coherent_with_context(
            correction.user_correction, correction.context
        ):
            issues.append(ValidationIssue.INCOHERENT)

        correction.validation_issues = issues

    def _is_duplicate(self, correction: ProposedCorrection) -> bool:
        """Verificar si la frase ya existe en el catálogo."""
        try:
            context = self.context_manager.get_context(correction.context)
            if "frases" in context:
                for phrase in context["frases"]:
                    if (
                        phrase.get("en", "").lower()
                        == correction.user_correction.lower()
                    ):
                        return True
        except ValueError:
            pass

        # También verificar en approved_phrases
        data = self._load_learned_phrases()
        for approved in data.get("approved_phrases", []):
            if (
                approved.get("en", "").lower()
                == correction.user_correction.lower()
            ):
                return True

        return False

    def _is_likely_spam(self, text: str) -> bool:
        """Detectar si es probable spam."""
        # Heurísticas simples
        if len(text) < 2:
            return True
        if text.count(" ") == 0 and len(text) > 50:
            return True  # Una sola palabra muy larga
        if text.startswith("http"):
            return True  # URL

        return False

    def _is_coherent_with_context(
        self, phrase: str, context_id: str
    ) -> bool:
        """
        Verificar coherencia básica con el contexto.
        
        Por ahora, solo chequea que la frase no sea vacía y que el contexto exista.
        Más adelante se puede hacer más sofisticado.
        """
        if not phrase or not context_id:
            return False

        try:
            self.context_manager.get_context(context_id)
            return True
        except ValueError:
            return False

    def get_pending_corrections(
        self, context_filter: Optional[str] = None
    ) -> List[ProposedCorrection]:
        """
        Obtener todas las correcciones pendientes.
        
        Args:
            context_filter: si se proporciona, filtrar por contexto
            
        Returns:
            List[ProposedCorrection]: correcciones pendientes
        """
        data = self._load_learned_phrases()
        corrections = [
            ProposedCorrection.from_dict(c)
            for c in data.get("proposed_corrections", [])
            if ProposedCorrection.from_dict(c).status == CorrectionStatus.PENDING
        ]

        if context_filter:
            corrections = [
                c for c in corrections if c.context == context_filter
            ]

        return corrections

    def approve_correction(
        self,
        correction_id: str,
        reviewer_id: str,
        notes: str = "",
    ) -> Optional[ApprovedPhrase]:
        """
        Aprobar una corrección propuesta.
        
        Args:
            correction_id: ID de la corrección
            reviewer_id: quién aprueba
            notes: notas del revisor
            
        Returns:
            ApprovedPhrase: la frase aprobada, o None si no se encontró
        """
        data = self._load_learned_phrases()

        # Buscar la corrección
        correction_dict = None
        for i, c in enumerate(data.get("proposed_corrections", [])):
            if c["id"] == correction_id:
                correction_dict = c
                correction_idx = i
                break

        if not correction_dict:
            return None

        correction = ProposedCorrection.from_dict(correction_dict)

        # Si tiene problemas de validación, rechazar
        if correction.validation_issues:
            self.reject_correction(
                correction_id,
                reviewer_id,
                "Falló validación automática",
            )
            return None

        # Crear frase aprobada
        approved_phrase = ApprovedPhrase(
            id=f"ap_{uuid4().hex[:8]}",
            context=correction.context,
            es=self._extract_spanish_from_correction(correction),
            en=correction.user_correction,
            approved_by_user=reviewer_id,
            approved_at=datetime.now().isoformat(),
            source_correction_id=correction_id,
        )

        # Actualizar corrección a aprobada
        correction.mark_reviewed(
            reviewer_id, CorrectionStatus.APPROVED, notes
        )
        data["proposed_corrections"][correction_idx] = correction.to_dict()

        # Agregar frase aprobada
        data["approved_phrases"].append(approved_phrase.to_dict())

        self._save_learned_phrases(data)

        return approved_phrase

    def _extract_spanish_from_correction(
        self, correction: ProposedCorrection
    ) -> str:
        """
        Extraer la frase en español de la corrección.
        
        Intenta obtenerla del contexto o usa un placeholder.
        """
        try:
            context = self.context_manager.get_context(correction.context)
            if "frases" in context:
                # Buscar una frase que traduce a la inglesa similar
                for phrase in context["frases"]:
                    en_phrase = phrase.get("en", "").lower()
                    if (
                        en_phrase in correction.user_correction.lower()
                        or correction.user_correction.lower() in en_phrase
                    ):
                        return phrase.get("es", "[Nueva frase]")
        except ValueError:
            pass

        return "[Nueva frase]"

    def reject_correction(
        self,
        correction_id: str,
        reviewer_id: str,
        reason: str = "",
    ) -> bool:
        """
        Rechazar una corrección propuesta.
        
        Args:
            correction_id: ID de la corrección
            reviewer_id: quién rechaza
            reason: razón del rechazo
            
        Returns:
            bool: True si se rechazó, False si no se encontró
        """
        data = self._load_learned_phrases()

        for i, c in enumerate(data.get("proposed_corrections", [])):
            if c["id"] == correction_id:
                correction = ProposedCorrection.from_dict(c)
                correction.mark_reviewed(
                    reviewer_id, CorrectionStatus.REJECTED, reason
                )
                data["proposed_corrections"][i] = correction.to_dict()
                self._save_learned_phrases(data)
                return True

        return False

    def get_approved_phrases(
        self, context_filter: Optional[str] = None
    ) -> List[ApprovedPhrase]:
        """
        Obtener todas las frases aprobadas.
        
        Args:
            context_filter: si se proporciona, filtrar por contexto
            
        Returns:
            List[ApprovedPhrase]: frases aprobadas
        """
        data = self._load_learned_phrases()
        phrases = [
            ApprovedPhrase.from_dict(p)
            for p in data.get("approved_phrases", [])
        ]

        if context_filter:
            phrases = [p for p in phrases if p.context == context_filter]

        return phrases

    def get_stats(self) -> dict:
        """
        Obtener estadísticas del flujo de correcciones.
        
        Returns:
            dict con:
            - total_proposed: total de correcciones propuestas
            - pending: pendientes de revisión
            - approved: aprobadas
            - rejected: rechazadas
            - added_to_catalog: ya incorporadas al catálogo
        """
        data = self._load_learned_phrases()

        proposed = [
            ProposedCorrection.from_dict(c)
            for c in data.get("proposed_corrections", [])
        ]

        pending = sum(
            1 for c in proposed if c.status == CorrectionStatus.PENDING
        )
        approved = sum(
            1 for c in proposed if c.status == CorrectionStatus.APPROVED
        )
        rejected = sum(
            1 for c in proposed if c.status == CorrectionStatus.REJECTED
        )

        approved_phrases = data.get("approved_phrases", [])
        added_to_catalog = sum(
            1 for p in approved_phrases if p.get("added_to_catalog", False)
        )

        return {
            "total_proposed": len(proposed),
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "added_to_catalog": added_to_catalog,
            "approval_rate": (
                round(approved / len(proposed), 2)
                if proposed
                else 0
            ),
        }

    def create_batch_for_review(
        self, batch_size: int = 10
    ) -> Optional[CorrectionBatch]:
        """
        Crear un lote de correcciones pendientes para revisión.
        
        Args:
            batch_size: cuántas correcciones agrupar
            
        Returns:
            CorrectionBatch: lote creado, o None si no hay pendientes
        """
        pending = self.get_pending_corrections()

        if not pending:
            return None

        batch_id = f"batch_{uuid4().hex[:8]}"
        batch = CorrectionBatch(
            batch_id=batch_id,
            created_at=datetime.now().isoformat(),
            corrections=pending[:batch_size],
        )

        return batch
