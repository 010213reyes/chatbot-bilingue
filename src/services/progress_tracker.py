"""
Servicio de rastreo de progreso del usuario.
Mantiene historial, estadísticas y genera recomendaciones.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from src.config.settings import DATA_PATHS


class ProgressTracker:
    """Rastrea y persiste el progreso del usuario."""
    
    def __init__(self, user_id: str, user_dir: str = DATA_PATHS['user_progress']):
        """
        Inicializa el tracker.
        
        Args:
            user_id: ID único del usuario
            user_dir: Directorio de datos de usuario
        """
        self.user_id = user_id
        self.user_dir = user_dir
        self.user_file = os.path.join(user_dir, f"{user_id}.json")
        self.data = self._load_or_create()
    
    def _load_or_create(self) -> Dict:
        """Carga datos existentes o crea nuevos."""
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Crear estructura base
        return {
            'user_id': self.user_id,
            'fecha_creacion': datetime.now().isoformat(),
            'nivel_actual': 'A1',
            'nivel_maximo': 'A1',
            'puntuacion_total': 0,
            'sesiones': [],
            'frases_aprendidas': [],
            'estadisticas': {
                'total_sesiones': 0,
                'total_preguntas': 0,
                'aciertos_totales': 0,
                'accuracy_promedio': 0,
            }
        }
    
    def save(self):
        """Guarda datos al archivo."""
        os.makedirs(self.user_dir, exist_ok=True)
        with open(self.user_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_session(self, sesion_data: Dict):
        """
        Agrega una sesión de práctica.
        
        Args:
            sesion_data: Diccionario con datos de sesión
        """
        sesion = {
            'fecha': datetime.now().isoformat(),
            'duracion_minutos': sesion_data.get('duracion', 0),
            'frases_practicadas': sesion_data.get('frases', []),
            'aciertos': sesion_data.get('aciertos', 0),
            'total': sesion_data.get('total', 0),
            'accuracy': sesion_data.get('aciertos', 0) / sesion_data.get('total', 1),
            'contextos': sesion_data.get('contextos', []),
        }
        
        self.data['sesiones'].append(sesion)
        self._update_statistics()
        self.save()
    
    def mark_phrase_learned(self, phrase_en: str, nivel: str):
        """Marca una frase como aprendida."""
        if phrase_en not in self.data['frases_aprendidas']:
            self.data['frases_aprendidas'].append({
                'frase': phrase_en,
                'nivel': nivel,
                'fecha_aprendida': datetime.now().isoformat(),
                'repasadas': 0
            })
            self.save()
    
    def update_level(self, new_level: str):
        """Actualiza el nivel actual del usuario."""
        self.data['nivel_actual'] = new_level
        
        # Actualizar nivel máximo si es necesario
        levels_order = ['A1', 'A2', 'B1', 'B2']
        if levels_order.index(new_level) > levels_order.index(self.data.get('nivel_maximo', 'A1')):
            self.data['nivel_maximo'] = new_level
        
        self.save()
    
    def _update_statistics(self):
        """Recalcula estadísticas generales."""
        sesiones = self.data['sesiones']
        
        if not sesiones:
            return
        
        total_sesiones = len(sesiones)
        total_preguntas = sum(s.get('total', 0) for s in sesiones)
        aciertos_totales = sum(s.get('aciertos', 0) for s in sesiones)
        
        self.data['estadisticas'] = {
            'total_sesiones': total_sesiones,
            'total_preguntas': total_preguntas,
            'aciertos_totales': aciertos_totales,
            'accuracy_promedio': (aciertos_totales / total_preguntas) if total_preguntas > 0 else 0,
        }
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del usuario."""
        return self.data['estadisticas']
    
    def get_last_n_sessions(self, n: int = 5) -> List[Dict]:
        """Obtiene las últimas N sesiones."""
        return self.data['sesiones'][-n:]
    
    def get_progress_summary(self) -> Dict:
        """Resumen completo del progreso."""
        return {
            'user_id': self.user_id,
            'nivel_actual': self.data['nivel_actual'],
            'nivel_maximo': self.data['nivel_maximo'],
            'frases_aprendidas': len(self.data['frases_aprendidas']),
            'sesiones_completadas': self.data['estadisticas']['total_sesiones'],
            'accuracy_promedio': f"{self.data['estadisticas']['accuracy_promedio']*100:.1f}%",
            'dias_activo': self._days_active(),
        }
    
    def _days_active(self) -> int:
        """Calcula días desde que el usuario empezó."""
        fecha_creacion = datetime.fromisoformat(self.data['fecha_creacion'])
        return (datetime.now() - fecha_creacion).days
    
    def get_next_review_phrases(self) -> List[Dict]:
        """Obtiene frases que necesitan repaso (spaced repetition)."""
        frases = self.data['frases_aprendidas']
        review_schedule = [1, 3, 7, 14]  # Días
        
        to_review = []
        for frase in frases:
            last_reviewed = datetime.fromisoformat(frase.get('fecha_aprendida', datetime.now().isoformat()))
            days_since = (datetime.now() - last_reviewed).days
            repasadas = frase.get('repasadas', 0)
            
            if repasadas < len(review_schedule):
                next_review_day = review_schedule[repasadas]
                if days_since >= next_review_day:
                    to_review.append(frase)
        
        return to_review
