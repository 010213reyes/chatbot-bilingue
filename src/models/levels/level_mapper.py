"""
Mapeo de frases de contextos a niveles de inglés.
Facilita la asignación automática y búsqueda por nivel.
"""

from typing import Dict, List, Optional
import json
import os


class LevelMapper:
    """Mapea frases a niveles de dificultad."""
    
    def __init__(self, contexts_file: str):
        """
        Inicializa el mapeador.
        
        Args:
            contexts_file: Ruta al archivo contexts.json
        """
        self.contexts_file = contexts_file
        self.mapped_phrases = self._load_and_map()
    
    def _load_and_map(self) -> Dict:
        """Carga contextos y mapea frases a niveles."""
        if not os.path.exists(self.contexts_file):
            raise FileNotFoundError(f"No encontrado: {self.contexts_file}")
        
        with open(self.contexts_file, 'r', encoding='utf-8') as f:
            contexts = json.load(f)
        
        # Mapeo automático basado en contexto
        mapping = {
            'A1': [],
            'A2': [],
            'B1': [],
            'B2': []
        }
        
        # Contextos por nivel (definido en settings)
        context_levels = {
            'saludo_basico': 'A1',
            'videojuegos_general': 'A1',
            'videojuegos_batalla': 'A2',
            'videojuegos_coordinacion': 'B1',
        }
        
        for context_id, context_data in contexts.get('contexts', {}).items():
            level = context_levels.get(context_id, 'A1')
            
            for phrase in context_data.get('frases', []):
                phrase_with_level = {
                    'nivel': level,
                    'contexto_id': context_id,
                    'contexto_nombre': context_data.get('nombre'),
                    **phrase
                }
                mapping[level].append(phrase_with_level)
        
        return mapping
    
    def get_phrases_by_level(self, level: str) -> List[Dict]:
        """Obtiene todas las frases de un nivel."""
        return self.mapped_phrases.get(level, [])
    
    def get_phrase_by_level_and_spanish(self, spanish: str, level: str) -> Optional[Dict]:
        """Busca una frase específica en un nivel."""
        phrases = self.get_phrases_by_level(level)
        spanish_lower = spanish.lower()
        
        for phrase in phrases:
            if spanish_lower in phrase.get('es', '').lower():
                return phrase
        return None
    
    def count_phrases_by_level(self) -> Dict[str, int]:
        """Cuenta frases por nivel."""
        return {
            level: len(phrases) 
            for level, phrases in self.mapped_phrases.items()
        }
    
    def get_progressive_phrases(self, start_level: str, limit: int = None) -> List[Dict]:
        """
        Obtiene frases en orden progresivo desde un nivel.
        
        Args:
            start_level: Nivel inicial (A1, A2, B1, B2)
            limit: Límite de frases (None = todas)
        
        Returns:
            Lista de frases en orden de dificultad
        """
        levels_order = ['A1', 'A2', 'B1', 'B2']
        start_idx = levels_order.index(start_level) if start_level in levels_order else 0
        
        result = []
        for level in levels_order[start_idx:]:
            result.extend(self.get_phrases_by_level(level))
            if limit and len(result) >= limit:
                return result[:limit]
        
        return result if not limit else result[:limit]
    
    def get_vocabulary_by_level(self, level: str) -> Dict[str, List[str]]:
        """Extrae vocabulario clave por nivel."""
        phrases = self.get_phrases_by_level(level)
        
        vocab = {
            'español': [],
            'ingles': [],
            'palabras_clave': set()
        }
        
        for phrase in phrases:
            vocab['español'].append(phrase.get('es'))
            vocab['ingles'].append(phrase.get('en'))
            
            # Extraer palabras clave principales
            words = phrase.get('en', '').split()
            vocab['palabras_clave'].update(words[:2])
        
        vocab['palabras_clave'] = list(vocab['palabras_clave'])
        return vocab
