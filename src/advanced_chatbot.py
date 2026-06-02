"""
Chatbot avanzado con red neuronal y progresión A1-B2.
Integra: LevelMapper, LevelClassifier, EvaluationService, ProgressTracker.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.context_manager import ContextManager
from src.models.levels.level_manager import level_manager
from src.models.levels.level_mapper import LevelMapper
from src.models.neural.level_classifier import LevelClassifier
from src.services.evaluation_service import EvaluationService
from src.services.progress_tracker import ProgressTracker
from src.config.settings import (
    DATA_PATHS, MAX_LEVEL, ENGLISH_LEVELS, 
    PROGRESSION_CONFIG, EVALUATION_CONFIG
)
from typing import Dict, Optional, Tuple
import time


class AdvancedBilingualChatbot:
    """
    Chatbot bilingüe avanzado con:
    - Evaluación adaptativa (A1-B2)
    - Red neuronal para clasificación
    - Progresión personalizada
    - Rastreo de progreso
    """
    
    def __init__(self, contexts_file: str, user_id: str = "user_001"):
        """
        Inicializa chatbot avanzado.
        
        Args:
            contexts_file: Ruta a contexts.json
            user_id: ID único del usuario
        """
        self.contexts_file = contexts_file
        self.user_id = user_id
        
        # Componentes principales
        self.context_manager = ContextManager(contexts_file)
        self.level_mapper = LevelMapper(contexts_file)
        self.level_classifier = LevelClassifier()
        self.evaluation_service = EvaluationService(self.level_mapper)
        self.progress_tracker = ProgressTracker(user_id)
        
        # Estado del usuario
        self.current_level = self.progress_tracker.data.get('nivel_actual', 'A1')
        self.current_context = None
        self.session_start = None
        self.session_stats = {
            'preguntas': 0,
            'aciertos': 0,
            'frases_nuevas': []
        }
    
    def initialize_user(self) -> Dict:
        """Inicia evaluación para nuevo usuario."""
        evaluation = self.evaluation_service.create_initial_evaluation()
        
        return {
            'tipo': 'evaluacion_inicial',
            'explicacion': 'Vamos a evaluar tu nivel de inglés con 5 preguntas simples.',
            'primera_pregunta': self._format_question(evaluation['questions'][0]),
            'total_preguntas': len(evaluation['questions'])
        }
    
    def _format_question(self, question: Dict) -> Dict:
        """Formatea pregunta para mostrar."""
        return {
            'id': question['id'],
            'pregunta': f"¿Cómo se dice '{question['es']}' en inglés?",
            'contexto': question['contexto'],
            'numero': f"{question['id'] + 1} de 5"
        }
    
    def submit_evaluation_answer(self, question_id: int, answer: str) -> Dict:
        """
        Procesa respuesta de evaluación.
        
        Args:
            question_id: ID de la pregunta
            answer: Respuesta del usuario
        
        Returns:
            Resultado y próxima pregunta si aplica
        """
        result = self.evaluation_service.check_answer(question_id, answer)
        
        # Obtener próxima pregunta si hay
        questions = self.evaluation_service.current_evaluation['questions']
        next_question_id = question_id + 1
        
        response = {
            'resultado': result,
            'es_correcto': result['correcto'],
        }
        
        if next_question_id < len(questions):
            response['proxima_pregunta'] = self._format_question(questions[next_question_id])
        else:
            # Evaluación completada
            eval_result = self.evaluation_service.get_evaluation_result()
            self.current_level = eval_result['nivel_recomendado']
            self.progress_tracker.update_level(self.current_level)
            
            response['evaluacion_completa'] = True
            response['resultado_final'] = eval_result
            response['mensaje'] = (
                f"¡Excelente! Tu nivel inicial es {eval_result['nivel_nombre']} ({eval_result['nivel_recomendado']}). "
                f"Accuracy: {eval_result['puntaje']:.1f}%"
            )
        
        return response
    
    def get_level_info(self) -> Dict:
        """Información del nivel actual del usuario."""
        level_obj = level_manager.get_level_by_code(self.current_level)
        contexts = level_manager.get_contexts_for_level(self.current_level)
        phrases_count = len(self.level_mapper.get_phrases_by_level(self.current_level))
        
        return {
            'nivel': self.current_level,
            'nombre': level_obj.nombre,
            'rango_puntaje': level_obj.rango,
            'contextos': contexts,
            'frases_disponibles': phrases_count,
            'es_nivel_maximo': level_manager.is_max_level(self.current_level),
        }
    
    def start_practice_session(self, context_id: Optional[str] = None) -> Dict:
        """Inicia sesión de práctica con frases del nivel actual."""
        # Seleccionar contexto si no se especifica
        if not context_id:
            contexts = level_manager.get_contexts_for_level(self.current_level)
            context_id = contexts[0] if contexts else 'saludo_basico'
        
        self.current_context = context_id
        self.session_start = time.time()
        self.session_stats = {'preguntas': 0, 'aciertos': 0, 'frases_nuevas': []}
        
        phrases = self.level_mapper.get_phrases_by_level(self.current_level)
        
        return {
            'tipo': 'sesion_practica',
            'nivel': self.current_level,
            'contexto': self.context_manager.get_context_info(context_id),
            'frases_totales': len(phrases),
            'explicacion': f"Practicando en contexto: {self.context_manager.get_context_info(context_id)['nombre']}"
        }
    
    def practice_phrase(self) -> Dict:
        """Obtiene frase para practicar."""
        phrases = self.level_mapper.get_phrases_by_level(self.current_level)
        
        if not phrases:
            return {'error': 'No hay frases para este nivel'}
        
        import random
        phrase = random.choice(phrases)
        
        return {
            'tipo': 'practica',
            'pregunta': f"¿Cómo se dice esto en inglés?: '{phrase['es']}'",
            'nivel': self.current_level,
            'contexto': phrase.get('contexto_nombre'),
            'uso': phrase.get('uso'),
            'respuesta_correcta_hint': f"Primera palabra: {phrase['en'].split()[0]}..."
        }
    
    def submit_practice_answer(self, phrase_es: str, user_answer_en: str) -> Dict:
        """Valida respuesta de práctica."""
        results = self.level_mapper.mapped_phrases.get(self.current_level, [])
        phrase = None
        
        for p in results:
            if p.get('es').lower() == phrase_es.lower():
                phrase = p
                break
        
        if not phrase:
            return {'error': 'Frase no encontrada'}
        
        en_correcta = phrase.get('en')
        is_correct = user_answer_en.lower().strip() == en_correcta.lower().strip()
        
        # Actualizar estadísticas
        self.session_stats['preguntas'] += 1
        if is_correct:
            self.session_stats['aciertos'] += 1
            self.session_stats['frases_nuevas'].append(phrase['es'])
        
        response = {
            'correcto': is_correct,
            'respuesta_correcta': en_correcta,
            'alternativas': phrase.get('en_alt', []),
            'uso': phrase.get('uso'),
        }
        
        # Verificar progresión
        if self.session_stats['preguntas'] % 5 == 0:
            accuracy = self.session_stats['aciertos'] / self.session_stats['preguntas']
            response['milestone'] = {
                'preguntas': self.session_stats['preguntas'],
                'accuracy': f"{accuracy*100:.1f}%",
                'progreso': "¡Vas muy bien!" if accuracy >= 0.7 else "Sigue practicando"
            }
        
        return response
    
    def end_session(self) -> Dict:
        """Finaliza sesión y actualiza progreso."""
        if not self.session_start:
            return {'error': 'No hay sesión activa'}
        
        duracion = (time.time() - self.session_start) / 60
        
        session_data = {
            'duracion': duracion,
            'frases': self.session_stats['frases_nuevas'],
            'aciertos': self.session_stats['aciertos'],
            'total': self.session_stats['preguntas'],
            'contextos': [self.current_context] if self.current_context else []
        }
        
        self.progress_tracker.add_session(session_data)
        
        # Marcar frases aprendidas
        for frase in self.session_stats['frases_nuevas']:
            phrase_obj = None
            for p in self.level_mapper.get_phrases_by_level(self.current_level):
                if p['es'] == frase:
                    phrase_obj = p
                    break
            
            if phrase_obj:
                self.progress_tracker.mark_phrase_learned(
                    phrase_obj['en'], 
                    self.current_level
                )
        
        # Verificar progresión a siguiente nivel
        stats = self.progress_tracker.get_statistics()
        next_level = level_manager.get_next_level(self.current_level)
        
        should_advance, reason = self._check_advancement(stats)
        
        return {
            'tipo': 'fin_sesion',
            'duracion_minutos': f"{duracion:.1f}",
            'preguntas_totales': self.session_stats['preguntas'],
            'aciertos': self.session_stats['aciertos'],
            'accuracy': f"{(self.session_stats['aciertos']/max(self.session_stats['preguntas'], 1))*100:.1f}%",
            'frases_aprendidas': len(self.session_stats['frases_nuevas']),
            'advancement': {
                'puede_avanzar': should_advance and next_level,
                'motivo': reason,
                'siguiente_nivel': next_level
            } if next_level else {'puede_avanzar': False, 'motivo': 'Ya estás en nivel máximo (B2)'},
            'resumen': self.progress_tracker.get_progress_summary()
        }
    
    def _check_advancement(self, stats: Dict) -> Tuple[bool, str]:
        """Verifica si usuario puede avanzar de nivel."""
        if level_manager.is_max_level(self.current_level):
            return False, "Ya alcanzaste el nivel máximo (B2)"
        
        accuracy = stats.get('accuracy_promedio', 0)
        min_accuracy = EVALUATION_CONFIG['puntaje_minimo_progreso'] / 100
        
        if accuracy >= min_accuracy:
            return True, f"Accuracy {accuracy*100:.1f}% ≥ {EVALUATION_CONFIG['puntaje_minimo_progreso']}%"
        
        return False, f"Necesitas {EVALUATION_CONFIG['puntaje_minimo_progreso']}% accuracy (tienes {accuracy*100:.1f}%)"
    
    def show_menu(self) -> str:
        """Menú principal."""
        return f"""
╔════════════════════════════════════════════════╗
║  CHATBOT BILINGÜE - NIVEL {self.current_level}                    ║
╚════════════════════════════════════════════════╝

📊 Tu progreso:
   {self.progress_tracker.get_progress_summary()}

Opciones:
  1. Ver información de tu nivel
  2. Iniciar sesión de práctica
  3. Ver estadísticas
  4. Ver frases para repasar
  5. Salir

Selecciona (1-5):
"""


def main():
    """Demo del chatbot avanzado."""
    contexts_file = os.path.join(
        os.path.dirname(__file__),
        '../data/contexts.json'
    )
    
    bot = AdvancedBilingualChatbot(contexts_file, "demo_user_001")
    
    print(bot.show_menu())
    print("\n" + "="*50)
    print("DEMO: Inicialización y Evaluación")
    print("="*50)
    
    # Mostrar información de niveles
    print("\n📚 Niveles disponibles:")
    for level_info in level_manager.list_all_levels():
        print(f"  {level_info['code']}: {level_info['nombre']}")
    
    # Mapeo de frases
    print("\n📖 Frases por nivel:")
    for level_code in ['A1', 'A2', 'B1', 'B2']:
        count = len(bot.level_mapper.get_phrases_by_level(level_code))
        print(f"  {level_code}: {count} frases")
    
    # Información de nivel actual
    print("\n" + "="*50)
    print("Nivel Actual del Usuario")
    print("="*50)
    print(bot.get_level_info())


if __name__ == '__main__':
    main()
