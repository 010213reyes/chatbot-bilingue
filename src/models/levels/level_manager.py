"""
Definición y gestión de niveles de inglés (A1 a B2).
"""

from typing import Dict, List, Optional
from src.config.settings import ENGLISH_LEVELS, CONTEXTS_BY_LEVEL


class Level:
    """Representa un nivel de inglés."""
    
    def __init__(self, code: str, nombre: str, rango: tuple):
        self.code = code
        self.nombre = nombre
        self.rango = rango  # (score_min, score_max)
    
    def __repr__(self):
        return f"Level({self.code}: {self.nombre})"
    
    def in_range(self, score: int) -> bool:
        """Verifica si un puntaje está en este nivel."""
        return self.rango[0] <= score < self.rango[1]


class LevelManager:
    """Gestiona transiciones y evaluaciones de niveles."""
    
    def __init__(self):
        """Inicializa los niveles."""
        self.levels = self._initialize_levels()
        self.level_order = list(ENGLISH_LEVELS.keys())
    
    def _initialize_levels(self) -> Dict[str, Level]:
        """Crea objetos Level."""
        levels = {}
        for code, info in ENGLISH_LEVELS.items():
            levels[code] = Level(code, info['nombre'], info['rango'])
        return levels
    
    def get_level_by_code(self, code: str) -> Optional[Level]:
        """Obtiene un nivel por código."""
        return self.levels.get(code)
    
    def get_level_by_score(self, score: int) -> Level:
        """Obtiene el nivel correspondiente a un puntaje."""
        for code in self.level_order:
            level = self.levels[code]
            if level.in_range(score):
                return level
        # Si el score es mayor que el máximo, retorna el nivel más alto
        return self.levels[self.level_order[-1]]
    
    def get_next_level(self, current_level: str) -> Optional[str]:
        """Obtiene el siguiente nivel."""
        try:
            idx = self.level_order.index(current_level)
            if idx < len(self.level_order) - 1:
                return self.level_order[idx + 1]
        except ValueError:
            pass
        return None
    
    def get_previous_level(self, current_level: str) -> Optional[str]:
        """Obtiene el nivel anterior."""
        try:
            idx = self.level_order.index(current_level)
            if idx > 0:
                return self.level_order[idx - 1]
        except ValueError:
            pass
        return None
    
    def list_all_levels(self) -> List[Dict]:
        """Lista todos los niveles con información."""
        result = []
        for code in self.level_order:
            level = self.levels[code]
            result.append({
                'code': level.code,
                'nombre': level.nombre,
                'rango_puntaje': level.rango,
                'contextos': CONTEXTS_BY_LEVEL.get(code, [])
            })
        return result
    
    def get_contexts_for_level(self, level: str) -> List[str]:
        """Obtiene contextos asociados a un nivel."""
        return CONTEXTS_BY_LEVEL.get(level, [])
    
    def is_max_level(self, level: str) -> bool:
        """Verifica si es el nivel máximo (B2)."""
        return level == self.level_order[-1]


# Singleton para acceso global
level_manager = LevelManager()
