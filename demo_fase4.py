"""
Demo de Fase 4: Memoria Conversacional y Aprendizaje Guiado

Demuestra:
1. Crear/cargar historial de un usuario
2. Iniciar una conversación
3. Guardar mensajes con detección de intención
4. Proponer correcciones
5. Validar y aprobar correcciones
"""

from datetime import datetime
from src.services import (
    MemoryService,
    IntentionDetectorService,
    CorrectionValidatorService,
)
from src.models.memory import MessageRole, FeedbackType


def demo_memory_service():
    """Demo del servicio de memoria."""
    print("\n" + "="*60)
    print("DEMO 1: Servicio de Memoria Conversacional")
    print("="*60)

    memory_service = MemoryService()

    # Crear/cargar historial
    user_id = "demo_user"
    history = memory_service.create_or_load_history(
        user_id=user_id,
        language_level="A2"
    )
    print(f"\n✓ Historial cargado para usuario: {user_id}")
    print(f"  - Nivel: {history.language_level}")
    print(f"  - Creado: {history.created_at}")

    # Iniciar conversación
    conversation = memory_service.start_conversation(
        user_id=user_id,
        context_focus="videojuegos_coordinacion",
        language_level="A2",
    )
    print(f"\n✓ Conversación iniciada: {conversation.session_id}")
    print(f"  - Contexto: {conversation.context_focus}")

    # Mensaje 1: Usuario pregunta
    msg1 = memory_service.save_message(
        user_id=user_id,
        conversation=conversation,
        role=MessageRole.USER,
        content="¿cómo se dice sígueme?",
        detected_intention="translation_request",
        detected_context="videojuegos_coordinacion",
        confidence=0.92,
    )
    print(f"\n✓ Mensaje 1 guardado (Usuario):")
    print(f"  - Contenido: {msg1.content}")
    print(f"  - Intención: {msg1.detected_intention} ({msg1.confidence})")

    # Mensaje 2: Chatbot responde
    msg2 = memory_service.save_message(
        user_id=user_id,
        conversation=conversation,
        role=MessageRole.ASSISTANT,
        content="Follow me",
        suggested_phrases=["Follow me", "Come with me", "Let's go"],
    )
    print(f"\n✓ Mensaje 2 guardado (Chatbot):")
    print(f"  - Contenido: {msg2.content}")
    print(f"  - Variantes: {msg2.suggested_phrases}")

    # Estadísticas
    stats = memory_service.get_user_stats(user_id)
    print(f"\n✓ Estadísticas del usuario:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")

    return user_id, conversation


def demo_intention_detector(user_id: str):
    """Demo del detector de intención."""
    print("\n" + "="*60)
    print("DEMO 2: Detector de Intención")
    print("="*60)

    detector = IntentionDetectorService()

    # Test 1
    message = "¿cómo se dice 'hola'?"
    intention1 = detector.detect_intention(message)
    print(f"\nMensaje: '{message}'")
    print(f"✓ Intención detectada: {intention1.intention}")
    print(f"  - Contexto: {intention1.context}")
    print(f"  - Confianza: {intention1.confidence:.2f}")
    print(f"  - Explicación: {intention1.explanation}")

    # Test 2
    message = "no, se dice así"
    intention2 = detector.detect_intention(message)
    print(f"\nMensaje: '{message}'")
    print(f"✓ Intención detectada: {intention2.intention}")
    print(f"  - Contexto: {intention2.context}")
    print(f"  - Confianza: {intention2.confidence:.2f}")

    # Test 3
    message = "quiero aprender más sobre videojuegos"
    intention3 = detector.detect_intention(
        message, previous_context="videojuegos_general"
    )
    print(f"\nMensaje: '{message}'")
    print(f"✓ Intención detectada: {intention3.intention}")
    print(f"  - Contexto: {intention3.context}")
    print(f"  - Confianza: {intention3.confidence:.2f}")


def demo_correction_validator():
    """Demo del validador de correcciones."""
    print("\n" + "="*60)
    print("DEMO 3: Validador de Correcciones")
    print("="*60)

    validator = CorrectionValidatorService()

    # Proponer corrección válida
    correction1 = validator.propose_correction(
        user_id="demo_user",
        session_id="session_demo1",
        original_chatbot_response="Follow me",
        user_correction="Come with me, let's go",
        context="videojuegos_coordinacion",
        intention="translation_request",
        confidence=0.85,
    )
    print(f"\n✓ Corrección propuesta:")
    print(f"  - ID: {correction1.id}")
    print(f"  - Status: {correction1.status.value}")
    print(f"  - Válida: {correction1.is_valid}")
    if not correction1.is_valid:
        print(f"  - Problemas: {[i.value for i in correction1.validation_issues]}")

    # Proponer corrección inválida (vacía)
    correction2 = validator.propose_correction(
        user_id="demo_user",
        session_id="session_demo1",
        original_chatbot_response="Test",
        user_correction="",  # ¡Vacía!
        context="videojuegos_coordinacion",
        intention="correction",
    )
    print(f"\n✓ Corrección inválida propuesta:")
    print(f"  - ID: {correction2.id}")
    print(f"  - Válida: {correction2.is_valid}")
    print(f"  - Problemas: {[i.value for i in correction2.validation_issues]}")

    # Obtener pendientes
    pending = validator.get_pending_corrections()
    print(f"\n✓ Correcciones pendientes: {len(pending)}")
    for corr in pending[:3]:
        print(f"  - {corr.id}: {corr.user_correction[:30]}...")

    # Aprobar la válida
    if correction1.is_valid:
        approved = validator.approve_correction(
            correction_id=correction1.id,
            reviewer_id="admin",
            notes="Buena variante",
        )
        if approved:
            print(f"\n✓ Corrección aprobada:")
            print(f"  - Frase: {approved.en}")
            print(f"  - Contexto: {approved.context}")
            print(f"  - Aprobada por: {approved.approved_by_user}")
            print(f"  - Fuente: {approved.source_correction_id}")

    # Rechazar la inválida
    validator.reject_correction(
        correction_id=correction2.id,
        reviewer_id="admin",
        reason="La corrección está vacía",
    )
    print(f"\n✓ Corrección rechazada: {correction2.id}")

    # Estadísticas
    stats = validator.get_stats()
    print(f"\n✓ Estadísticas de correcciones:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")

    # Frases aprobadas
    approved_phrases = validator.get_approved_phrases()
    print(f"\n✓ Frases aprobadas: {len(approved_phrases)}")
    for phrase in approved_phrases[:3]:
        print(f"  - {phrase.en} ({phrase.context})")


def main():
    """Ejecutar todas las demos."""
    print("\n" + "#"*60)
    print("# DEMO: FASE 4 - Memoria Conversacional y Aprendizaje Guiado")
    print("#"*60)

    # Demo 1: Memoria
    user_id, conversation = demo_memory_service()

    # Demo 2: Intención
    demo_intention_detector(user_id)

    # Demo 3: Correcciones
    demo_correction_validator()

    print("\n" + "#"*60)
    print("# ✓ Todas las demos completadas exitosamente")
    print("#"*60)
    print("\nArchivos generados:")
    print("  - data/user_conversations/demo_user/history.json")
    print("  - data/learned_phrases.json")


if __name__ == "__main__":
    main()
