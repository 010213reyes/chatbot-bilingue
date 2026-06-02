"""
Gestor de contextos para el chatbot.
Maneja carga de contextos, búsqueda de frases y exposición de vocabulario.
"""

import json
import os
from typing import Dict, List, Optional


class ContextManager:
    """Gestiona contextos y frases para aprendizaje contextual."""
    
    def __init__(self, contexts_file: str):
        """
        Inicializa el gestor de contextos.
        
        Args:
            contexts_file: Ruta al archivo JSON de contextos
        """
        self.contexts_file = contexts_file
        self.contexts = self._load_contexts()
    
    def _load_contexts(self) -> Dict:
        """Carga contextos desde archivo JSON."""
        if not os.path.exists(self.contexts_file):
            raise FileNotFoundError(f"Archivo de contextos no encontrado: {self.contexts_file}")
        
        with open(self.contexts_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('contexts', {})
    
    def get_context(self, context_id: str) -> Optional[Dict]:
        """Obtiene un contexto específico."""
        return self.contexts.get(context_id)
    
    def list_contexts(self) -> List[str]:
        """Lista todos los contextos disponibles."""
        return list(self.contexts.keys())
    
    def get_context_info(self, context_id: str) -> Optional[Dict]:
        """Obtiene información sobre un contexto."""
        context = self.get_context(context_id)
        if context:
            return {
                'id': context_id,
                'nombre': context.get('nombre'),
                'descripcion': context.get('descripcion'),
                'cantidad_frases': len(context.get('frases', []))
            }
        return None
    
    def get_phrases_by_context(self, context_id: str) -> List[Dict]:
        """Obtiene todas las frases de un contexto."""
        context = self.get_context(context_id)
        return context.get('frases', []) if context else []
    
    def search_phrase_by_spanish(self, spanish_phrase: str, context_id: Optional[str] = None) -> List[Dict]:
        """
        Busca frases por texto en español.
        
        Args:
            spanish_phrase: Frase en español (búsqueda parcial)
            context_id: Contexto específico (opcional)
        
        Returns:
            Lista de frases que coinciden
        """
        results = []
        contexts_to_search = {context_id: self.contexts[context_id]} if context_id else self.contexts
        
        spanish_lower = spanish_phrase.lower()
        
        for ctx_id, ctx_data in contexts_to_search.items():
            for phrase in ctx_data.get('frases', []):
                if spanish_lower in phrase.get('es', '').lower():
                    results.append({
                        'contexto_id': ctx_id,
                        'contexto_nombre': ctx_data.get('nombre'),
                        **phrase
                    })
        
        return results
    
    def search_phrase_by_english(self, english_phrase: str, context_id: Optional[str] = None) -> List[Dict]:
        """
        Busca frases por texto en inglés.
        
        Args:
            english_phrase: Frase en inglés (búsqueda parcial)
            context_id: Contexto específico (opcional)
        
        Returns:
            Lista de frases que coinciden
        """
        results = []
        contexts_to_search = {context_id: self.contexts[context_id]} if context_id else self.contexts
        
        english_lower = english_phrase.lower()
        
        for ctx_id, ctx_data in contexts_to_search.items():
            for phrase in ctx_data.get('frases', []):
                en_text = phrase.get('en', '').lower()
                en_alts = [alt.lower() for alt in phrase.get('en_alt', [])]
                
                if english_lower in en_text or any(english_lower in alt for alt in en_alts):
                    results.append({
                        'contexto_id': ctx_id,
                        'contexto_nombre': ctx_data.get('nombre'),
                        **phrase
                    })
        
        return results
    
    def get_random_phrase(self, context_id: Optional[str] = None) -> Optional[Dict]:
        """Obtiene una frase aleatoria para práctica."""
        import random
        
        if context_id:
            phrases = self.get_phrases_by_context(context_id)
        else:
            # Obtener de todos los contextos
            phrases = []
            for ctx in self.contexts.values():
                phrases.extend(ctx.get('frases', []))
        
        return random.choice(phrases) if phrases else None
    
    def get_vocabulary_by_context(self, context_id: str) -> Dict[str, List[str]]:
        """Obtiene vocabulario organizado por contexto."""
        phrases = self.get_phrases_by_context(context_id)
        
        vocabulary = {
            'español': [],
            'ingles': [],
            'palabras_clave': []
        }
        
        for phrase in phrases:
            vocabulary['español'].append(phrase.get('es'))
            vocabulary['ingles'].append(phrase.get('en'))
            
            # Extraer palabras clave (primeras 2-3 palabras)
            words = phrase.get('en', '').split()[:3]
            vocabulary['palabras_clave'].extend(words)
        
        return vocabulary
