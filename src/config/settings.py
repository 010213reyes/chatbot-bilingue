"""
Configuración centralizada del chatbot bilingüe.
"""

# Niveles de inglés soportados
ENGLISH_LEVELS = {
    'A1': {'nombre': 'Principiante', 'rango': (0, 20)},
    'A2': {'nombre': 'Elemental', 'rango': (20, 40)},
    'B1': {'nombre': 'Intermedio', 'rango': (40, 70)},
    'B2': {'nombre': 'Intermedio-Alto', 'rango': (70, 100)},
}

# Máximo nivel soportado
MAX_LEVEL = 'B2'

# Configuración de red neuronal
NEURAL_CONFIG = {
    'input_size': 50,  # Embeddings
    'hidden_layers': [128, 64],
    'output_size': len(ENGLISH_LEVELS),  # Clasificar a qué nivel
    'dropout': 0.2,
    'learning_rate': 0.001,
    'batch_size': 32,
    'epochs': 50,
}

# Configuración de evaluación
EVALUATION_CONFIG = {
    'preguntas_por_nivel': 5,  # 5 preguntas para evaluar
    'puntaje_minimo_progreso': 70,  # 70% para subir de nivel
    'sesiones_para_consolidar': 3,  # 3 sesiones exitosas para consolidar nivel
}

# Configuración de progresión
PROGRESSION_CONFIG = {
    'frases_nuevas_por_sesion': 3,
    'repeticion_espaciada_dias': [1, 3, 7, 14],  # Días para repasar
    'duracion_sesion_minutos': 15,
}

# Rutas de datos
DATA_PATHS = {
    'contexts': 'data/contexts.json',
    'levels': 'data/levels',
    'user_progress': 'data/user_progress',
}

# Contextos disponibles por nivel
CONTEXTS_BY_LEVEL = {
    'A1': ['saludo_basico', 'videojuegos_general', 'vida_cotidiana', 'ayuda_general'],
    'A2': ['videojuegos_general', 'videojuegos_batalla', 'emociones'],
    'B1': ['videojuegos_batalla', 'videojuegos_coordinacion'],
    'B2': ['videojuegos_coordinacion'],
}

# Idiomas soportados
LANGUAGES = {
    'es': 'Español',
    'en': 'English',
}

# Logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'file': 'logs/chatbot.log',
}
