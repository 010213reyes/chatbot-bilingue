"""
Chatbot base - Responde en español.
Gestor de conversaciones contextual.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.context_manager import ContextManager
from src.services.contextual_lesson_service import ContextualLessonService
from typing import Dict, Optional, List


class SpanishChatbot:
    """Chatbot que responde en español, enseñando inglés contextualmente."""
    
    def __init__(self, contexts_file: str):
        """
        Inicializa el chatbot.
        
        Args:
            contexts_file: Ruta al archivo de contextos JSON
        """
        self.context_manager = ContextManager(contexts_file)
        self.contextual_lesson_service = ContextualLessonService(contexts_file)
        self.current_context = None
        self.conversation_history = []
    
    def set_context(self, context_id: str) -> bool:
        """Establece el contexto actual."""
        if context_id in self.context_manager.list_contexts():
            self.current_context = context_id
            return True
        return False
    
    def get_available_contexts(self) -> List[Dict]:
        """Obtiene lista de contextos disponibles con información."""
        contexts = []
        for ctx_id in self.context_manager.list_contexts():
            info = self.context_manager.get_context_info(ctx_id)
            contexts.append(info)
        return contexts
    
    def ask_for_phrase(self, question: str) -> Dict:
        """
        Usuario pregunta por una frase en español.
        Retorna la frase en inglés con explicación.
        
        Args:
            question: Pregunta en español
        
        Returns:
            Respuesta con frases en inglés
        """
        # Buscar frases relacionadas
        results = self.context_manager.search_phrase_by_spanish(question, self.current_context)
        
        if results:
            phrase = results[0]  # Mejor coincidencia
            response = {
                'tipo': 'frase_encontrada',
                'pregunta': question,
                'contexto': phrase.get('contexto_nombre'),
                'respuesta_es': phrase.get('es'),
                'respuesta_en': phrase.get('en'),
                'alternativas_en': phrase.get('en_alt', []),
                'uso': phrase.get('uso'),
                'explicacion': f"En {phrase.get('contexto_nombre')}, para decir '{phrase.get('es')}', "
                             f"puedes usar: '{phrase.get('en')}'. "
                             f"Uso: {phrase.get('uso')}"
            }
        else:
            response = {
                'tipo': 'no_encontrada',
                'pregunta': question,
                'explicacion': "No encontré una frase exacta. ¿Puedes dar más detalles? "
                             "Por ejemplo, ¿en qué contexto la necesitas?"
            }
        
        # Guardar en historial
        self.conversation_history.append({
            'tipo': 'usuario',
            'contenido': question,
            'respuesta': response
        })
        
        return response
    
    def get_phrase_explanation(self, english_phrase: str) -> Dict:
        """
        Usuario pregunta qué significa una frase en inglés.
        
        Args:
            english_phrase: Frase en inglés
        
        Returns:
            Explicación y traducción
        """
        results = self.context_manager.search_phrase_by_english(english_phrase, self.current_context)
        
        if results:
            phrase = results[0]
            response = {
                'tipo': 'traduccion',
                'ingles': phrase.get('en'),
                'spanish': phrase.get('es'),
                'contexto': phrase.get('contexto_nombre'),
                'uso': phrase.get('uso'),
                'explicacion': f"'{phrase.get('en')}' significa '{phrase.get('es')}'. "
                             f"Se usa en: {phrase.get('uso')}"
            }
        else:
            response = {
                'tipo': 'no_encontrada',
                'ingles': english_phrase,
                'explicacion': "No conozco esa frase aún. Pero ¡estamos aprendiendo!"
            }
        
        self.conversation_history.append({
            'tipo': 'usuario_en',
            'contenido': english_phrase,
            'respuesta': response
        })
        
        return response
    
    def practice_context(self, context_id: Optional[str] = None) -> Dict:
        """
        Obtiene una frase para practicar.
        
        Args:
            context_id: Contexto específico (usa el actual si no se especifica)
        
        Returns:
            Frase para practicar
        """
        ctx = context_id or self.current_context
        phrase = self.context_manager.get_random_phrase(ctx)
        
        if phrase:
            response = {
                'tipo': 'practica',
                'pregunta': f"¿Cómo se dice esto en inglés?: '{phrase.get('es')}'",
                'respuesta_correcta': phrase.get('en'),
                'alternativas': phrase.get('en_alt', []),
                'uso': phrase.get('uso')
            }
        else:
            response = {
                'tipo': 'error',
                'explicacion': "No hay frases para practicar. Primero selecciona un contexto."
            }
        
        return response
    
    def get_vocabulary_lesson(self, context_id: Optional[str] = None) -> Dict:
        """
        Obtiene una lección de vocabulario por contexto.
        
        Args:
            context_id: Contexto específico
        
        Returns:
            Datos de lección
        """
        ctx = context_id or self.current_context
        
        if not ctx:
            return {
                'tipo': 'error',
                'explicacion': 'Debes seleccionar un contexto primero.'
            }
        
        context_info = self.context_manager.get_context_info(ctx)
        vocab = self.context_manager.get_vocabulary_by_context(ctx)
        phrases = self.context_manager.get_phrases_by_context(ctx)
        
        response = {
            'tipo': 'leccion_vocabulario',
            'contexto': context_info.get('nombre'),
            'descripcion': context_info.get('descripcion'),
            'frases': phrases,
            'cantidad_frases': len(phrases)
        }
        
        return response

    def get_contextual_lesson(self, context_id: Optional[str] = None) -> List[str]:
        """Obtiene una lección textual completa por contexto."""
        ctx = context_id or self.current_context

        if not ctx:
            return ["Debes seleccionar un contexto primero."]

        return self.contextual_lesson_service.get_text_lesson(ctx)
    
    def show_menu(self) -> str:
        """Muestra menú de opciones en español."""
        menu = """
╔════════════════════════════════════════════════╗
║     CHATBOT BILINGÜE - ENSEÑA INGLÉS          ║
╚════════════════════════════════════════════════╝

Opciones:
  1. Ver contextos disponibles
  2. Seleccionar contexto
  3. Preguntar cómo decir algo en inglés
  4. Pregunta por significado en inglés
  5. Practicar frase aleatoria
  6. Ver lección de vocabulario
    7. Ver lección contextual
    8. Salir

Selecciona una opción (1-8):
"""
        return menu


def main():
    """Función principal para pruebas."""
    import os
    
    # Ruta a contextos
    contexts_file = os.path.join(
        os.path.dirname(__file__),
        '../data/contexts.json'
    )
    
    # Inicializar chatbot
    bot = SpanishChatbot(contexts_file)
    
    print(bot.show_menu())
    
    # Ejemplo de uso
    print("\n📍 Contextos disponibles:")
    for ctx in bot.get_available_contexts():
        print(f"  - {ctx['nombre']} ({ctx['cantidad_frases']} frases)")
    
    # Seleccionar contexto
    bot.set_context('videojuegos_general')
    print(f"\n✅ Contexto seleccionado: Videojuegos - General")
    
    # Ejemplo: Usuario pregunta
    print("\n👤 Usuario: ¿Cómo digo 'Necesito ayuda' en inglés?")
    response = bot.ask_for_phrase("Necesito ayuda")
    print(f"🤖 Bot: {response['explicacion']}")
    
    # Ejemplo: Traducir del inglés
    print("\n👤 Usuario: ¿Qué significa 'Nice job'?")
    response = bot.get_phrase_explanation("Nice job")
    print(f"🤖 Bot: {response['explicacion']}")
    
    # Ejemplo: Practicar
    print("\n🎮 Practicando...")
    response = bot.practice_context()
    print(f"🤖 Bot: {response['pregunta']}")
    print(f"   Respuesta correcta: {response['respuesta_correcta']}")

    # Ejemplo: Lección contextual textual
    print("\n📘 Lección contextual:")
    lesson_lines = bot.get_contextual_lesson()
    for line in lesson_lines[:8]:
        print(f"   {line}")


if __name__ == '__main__':
    main()
