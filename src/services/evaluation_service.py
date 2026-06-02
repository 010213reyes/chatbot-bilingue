"""
Servicio de evaluación de usuario.
Determina el nivel inicial y ajusta progresión.
"""

from typing import Dict, List, Tuple
import time
from src.models.levels.level_manager import level_manager
from src.config.settings import EVALUATION_CONFIG


class EvaluationService:
    """Evalúa el nivel del usuario mediante quiz."""
    
    def __init__(self, level_mapper):
        """
        Inicializa el servicio.
        
        Args:
            level_mapper: Instancia de LevelMapper
        """
        self.level_mapper = level_mapper
        self.current_evaluation = None
    
    def create_initial_evaluation(self) -> Dict:
        """
        Crea quiz inicial para determinar nivel (A1-B2).
        
        Returns:
            Diccionario con preguntas de evaluación
        """
        # Obtener frases de A1 (nivel inicial)
        phrases_a1 = self.level_mapper.get_phrases_by_level('A1')
        
        num_questions = EVALUATION_CONFIG['preguntas_por_nivel']
        questions = []
        
        for i, phrase in enumerate(phrases_a1[:num_questions]):
            question = {
                'id': i,
                'nivel_esperado': 'A1',
                'tipo': 'traduccion',
                'es': phrase.get('es'),
                'en_correcta': phrase.get('en'),
                'alternativas_en': phrase.get('en_alt', []),
                'contexto': phrase.get('contexto_nombre'),
            }
            questions.append(question)
        
        self.current_evaluation = {
            'tipo': 'inicial',
            'fase': 1,  # A1-A2
            'questions': questions,
            'respuestas': []
        }
        
        return self.current_evaluation
    
    def check_answer(self, question_id: int, user_answer: str) -> Dict:
        """
        Verifica la respuesta del usuario.
        
        Args:
            question_id: ID de la pregunta
            user_answer: Respuesta del usuario
        
        Returns:
            Resultado de la respuesta
        """
        if not self.current_evaluation:
            return {'error': 'No hay evaluación en curso'}
        
        questions = self.current_evaluation['questions']
        if question_id >= len(questions):
            return {'error': 'Pregunta no encontrada'}
        
        question = questions[question_id]
        en_correcta = question['en_correcta']
        
        # Comparación simple (podría mejorarse con fuzzy matching)
        is_correct = user_answer.lower().strip() == en_correcta.lower().strip()
        
        result = {
            'correcto': is_correct,
            'respuesta_correcta': en_correcta,
            'alternativas': question['alternativas_en'],
        }
        
        self.current_evaluation['respuestas'].append({
            'question_id': question_id,
            'user_answer': user_answer,
            'correcto': is_correct
        })
        
        return result
    
    def get_evaluation_result(self) -> Dict:
        """Obtiene el resultado final de la evaluación."""
        if not self.current_evaluation:
            return {'error': 'No hay evaluación'}
        
        respuestas = self.current_evaluation['respuestas']
        total = len(respuestas)
        
        if total == 0:
            return {'error': 'Sin respuestas'}
        
        correctas = sum(1 for r in respuestas if r['correcto'])
        puntaje = (correctas / total) * 100
        
        # Determinar nivel basado en puntaje
        nivel_recomendado = level_manager.get_level_by_score(int(puntaje))
        
        return {
            'total_preguntas': total,
            'correctas': correctas,
            'puntaje': puntaje,
            'nivel_recomendado': nivel_recomendado.code,
            'nivel_nombre': nivel_recomendado.nombre,
        }
    
    def adaptive_difficulty_check(self, user_performance: Dict) -> Tuple[bool, str]:
        """
        Verifica si el usuario debe subir de nivel basado en desempeño.
        
        Args:
            user_performance: Diccionario con métricas de desempeño
        
        Returns:
            (debe_subir, motivo)
        """
        accuracy = user_performance.get('accuracy', 0)
        consecutive_correct = user_performance.get('consecutive_correct', 0)
        sessiones_exitosas = user_performance.get('sessiones_exitosas', 0)
        
        min_accuracy = EVALUATION_CONFIG['puntaje_minimo_progreso']
        min_sessiones = EVALUATION_CONFIG['sesiones_para_consolidar']
        
        if accuracy >= min_accuracy and sessiones_exitosas >= min_sessiones:
            return True, f"Accuracy {accuracy}% + {sessiones_exitosas} sesiones exitosas"
        
        return False, "Mantén la consistencia"
