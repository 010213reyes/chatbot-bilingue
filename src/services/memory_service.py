"""
Servicio de memoria conversacional para Fase 4.

Gestiona la persistencia de conversaciones y mensajes por usuario.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from uuid import uuid4

from src.models.memory import (
    Message,
    MessageRole,
    Conversation,
    UserConversationHistory,
    FeedbackType,
)


class MemoryService:
    """
    Servicio para gestionar la memoria conversacional de usuarios.
    
    Persistencia:
    - Cada usuario tiene su propia carpeta: data/user_conversations/{user_id}/
    - Archivo principal: history.json
    - Formato: JSON con historial de conversaciones
    """

    def __init__(self, base_path: str = "data/user_conversations"):
        """
        Inicializar el servicio de memoria.
        
        Args:
            base_path: ruta base donde se almacenan las conversaciones
        """
        self.base_path = base_path
        Path(base_path).mkdir(parents=True, exist_ok=True)

    def _get_user_path(self, user_id: str) -> Path:
        """Obtener la ruta del usuario."""
        return Path(self.base_path) / user_id

    def _get_history_file(self, user_id: str) -> Path:
        """Obtener la ruta del archivo history.json del usuario."""
        return self._get_user_path(user_id) / "history.json"

    def create_or_load_history(
        self,
        user_id: str,
        language_level: str = "A1"
    ) -> UserConversationHistory:
        """
        Crear o cargar el historial de conversaciones de un usuario.
        
        Args:
            user_id: identificador único del usuario
            language_level: nivel de idioma (A1, A2, B1, etc.)
            
        Returns:
            UserConversationHistory: historial cargado o creado
        """
        history_file = self._get_history_file(user_id)

        if history_file.exists():
            # Cargar historial existente
            with open(history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return UserConversationHistory.from_dict(data)
        else:
            # Crear nuevo historial
            user_dir = self._get_user_path(user_id)
            user_dir.mkdir(parents=True, exist_ok=True)

            history = UserConversationHistory(
                user_id=user_id,
                created_at=datetime.now().isoformat(),
                language_level=language_level,
                conversations=[],
            )
            self._save_history(history)
            return history

    def _save_history(self, history: UserConversationHistory) -> None:
        """Guardar historial a archivo JSON."""
        history_file = self._get_history_file(history.user_id)
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history.to_dict(), f, ensure_ascii=False, indent=2)

    def start_conversation(
        self,
        user_id: str,
        context_focus: Optional[str] = None,
        language_level: Optional[str] = None,
    ) -> Conversation:
        """
        Iniciar una nueva sesión de conversación.
        
        Args:
            user_id: identificador del usuario
            context_focus: contexto principal de la sesión (ej: "videojuegos_coordinacion")
            language_level: nivel del usuario en esta sesión
            
        Returns:
            Conversation: nueva conversación vacía
        """
        session_id = f"session_{uuid4().hex[:8]}"
        conversation = Conversation(
            session_id=session_id,
            user_id=user_id,
            timestamp=datetime.now().isoformat(),
            messages=[],
            language_level=language_level,
            context_focus=context_focus,
        )
        return conversation

    def save_message(
        self,
        user_id: str,
        conversation: Conversation,
        role: MessageRole,
        content: str,
        detected_intention: Optional[str] = None,
        detected_context: Optional[str] = None,
        confidence: float = 0.0,
        suggested_phrases: Optional[List[str]] = None,
        is_correction: bool = False,
        feedback_type: Optional[FeedbackType] = None,
    ) -> Message:
        """
        Guardar un mensaje en la conversación.
        
        Args:
            user_id: identificador del usuario
            conversation: conversación a actualizar
            role: rol del que envía
            content: texto del mensaje
            detected_intention: intención detectada
            detected_context: contexto detectado
            confidence: confianza de la detección
            suggested_phrases: frases sugeridas (si es ASSISTANT)
            is_correction: si el usuario está corrigiendo
            feedback_type: tipo de retroalimentación
            
        Returns:
            Message: el mensaje guardado
        """
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            detected_intention=detected_intention,
            detected_context=detected_context,
            confidence=confidence,
            suggested_phrases=suggested_phrases or [],
            is_correction=is_correction,
            feedback_type=feedback_type,
        )

        conversation.add_message(message)

        # Cargar historial, actualizar y guardar
        history = self.create_or_load_history(user_id)
        existing_conv = history.get_conversation(conversation.session_id)

        if existing_conv:
            # Reemplazar la conversación existente
            history.conversations = [
                c for c in history.conversations
                if c.session_id != conversation.session_id
            ]

        history.add_conversation(conversation)
        self._save_history(history)

        return message

    def end_conversation(self, user_id: str, conversation: Conversation) -> None:
        """
        Finalizar una conversación (marca timestamp de cierre).
        
        Args:
            user_id: identificador del usuario
            conversation: conversación a cerrar
        """
        history = self.create_or_load_history(user_id)
        existing_conv = history.get_conversation(conversation.session_id)

        if existing_conv:
            # La conversación ya está guardada
            pass
        self._save_history(history)

    def get_conversation_history(
        self,
        user_id: str,
        limit: int = 50,
    ) -> List[Conversation]:
        """
        Obtener el historial de conversaciones de un usuario.
        
        Args:
            user_id: identificador del usuario
            limit: máximo de conversaciones a retornar (más recientes)
            
        Returns:
            List[Conversation]: últimas N conversaciones
        """
        history = self.create_or_load_history(user_id)
        return history.get_latest_conversations(limit=limit)

    def get_last_conversation(self, user_id: str) -> Optional[Conversation]:
        """Obtener la última conversación del usuario."""
        history = self.create_or_load_history(user_id)
        conversations = history.get_latest_conversations(limit=1)
        return conversations[0] if conversations else None

    def get_user_stats(self, user_id: str) -> dict:
        """
        Obtener estadísticas del usuario.
        
        Returns:
            dict con:
            - total_conversations: número total de sesiones
            - total_messages: total de mensajes intercambiados
            - average_messages_per_session: promedio
            - most_used_context: contexto más frecuente
            - language_level: nivel actual
        """
        history = self.create_or_load_history(user_id)
        total_conversations = history.total_conversations

        total_messages = sum(
            len(c.messages) for c in history.conversations
        )

        average_messages = (
            total_messages / total_conversations
            if total_conversations > 0
            else 0
        )

        # Contexto más usado
        context_counts = {}
        for conv in history.conversations:
            if conv.context_focus:
                context_counts[conv.context_focus] = (
                    context_counts.get(conv.context_focus, 0) + 1
                )

        most_used_context = (
            max(context_counts, key=context_counts.get)
            if context_counts
            else None
        )

        return {
            "user_id": user_id,
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "average_messages_per_session": round(average_messages, 2),
            "most_used_context": most_used_context,
            "language_level": history.language_level,
            "created_at": history.created_at,
        }

    def clear_old_conversations(
        self,
        user_id: str,
        keep_last_n: int = 30,
    ) -> int:
        """
        Limpiar conversaciones antiguas, manteniendo las últimas N.
        
        Args:
            user_id: identificador del usuario
            keep_last_n: cuántas conversaciones mantener
            
        Returns:
            int: número de conversaciones eliminadas
        """
        history = self.create_or_load_history(user_id)
        original_count = len(history.conversations)

        if original_count > keep_last_n:
            # Mantener solo las últimas
            history.conversations = history.get_latest_conversations(
                limit=keep_last_n
            )
            self._save_history(history)

        return original_count - len(history.conversations)
