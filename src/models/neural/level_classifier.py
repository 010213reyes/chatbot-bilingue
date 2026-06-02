"""
Modelo de red neuronal para clasificación de nivel y predicción de progresión.
Basado en TensorFlow/Keras.
"""

import numpy as np
import os
from typing import Tuple, Dict, Optional
import pickle


class LevelClassifier:
    """
    Red neuronal para clasificar el nivel del usuario basado en su desempeño.
    
    Predice: A1, A2, B1, B2 basado en:
    - Accuracy en frases
    - Velocidad de respuesta
    - Patrones de error
    - Frases completadas
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Inicializa el clasificador.
        
        Args:
            model_path: Ruta a modelo guardado (opcional)
        """
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.levels = ['A1', 'A2', 'B1', 'B2']
        self.is_trained = False
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def create_model(self):
        """Crea arquitectura de red neuronal."""
        try:
            import tensorflow as tf
            from tensorflow import keras
            
            model = keras.Sequential([
                keras.layers.Dense(128, activation='relu', input_shape=(10,)),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dense(len(self.levels), activation='softmax')
            ])
            
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            self.model = model
            return model
        except ImportError:
            print("⚠️  TensorFlow no instalado. Usando clasificador simple.")
            return self._create_simple_classifier()
    
    def _create_simple_classifier(self):
        """Clasificador simple (sin TensorFlow)."""
        return SimpleClassifier(self.levels)
    
    def extract_features(self, user_data: Dict) -> np.ndarray:
        """
        Extrae features de datos del usuario.
        
        Features:
        1. Accuracy promedio
        2. Velocidad respuesta (caracteres/seg)
        3. Contextos completados
        4. Racha de aciertos
        5. Frases únicas aprendidas
        6. Sesiones completadas
        7. Días activo
        8. Errores retirados vs frases totales
        9. Velocidad lectura (palabras/seg)
        10. Consistencia (desv estándar accuracy)
        
        Args:
            user_data: Diccionario con datos del usuario
        
        Returns:
            Array de features normalizado
        """
        features = np.array([
            user_data.get('accuracy', 0.5),  # 0-1
            min(user_data.get('respuesta_velocidad', 1), 5),  # 0-5 car/seg
            user_data.get('contextos_completados', 0) / 5,  # 0-1
            user_data.get('racha_aciertos', 0) / 10,  # 0-1 (0-10 máx)
            min(user_data.get('frases_unicas', 0) / 50, 1),  # 0-1 (50 máx)
            min(user_data.get('sesiones', 0) / 10, 1),  # 0-1 (10 máx)
            min(user_data.get('dias_activo', 0) / 30, 1),  # 0-1 (30 días)
            user_data.get('ratio_error', 0.3),  # 0-1
            user_data.get('velocidad_lectura', 1) / 10,  # 0-1 (10 palabras/seg)
            user_data.get('consistencia', 0.5),  # 0-1
        ], dtype=np.float32)
        
        return features.reshape(1, -1)
    
    def predict_level(self, user_data: Dict) -> Tuple[str, float]:
        """
        Predice el nivel del usuario.
        
        Args:
            user_data: Diccionario con datos del usuario
        
        Returns:
            (nivel, confianza) - ej: ('B1', 0.85)
        """
        features = self.extract_features(user_data)
        
        if isinstance(self.model, SimpleClassifier):
            return self.model.predict(features)
        
        try:
            predictions = self.model.predict(features, verbose=0)
            level_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][level_idx])
            return self.levels[level_idx], confidence
        except Exception as e:
            print(f"Error en predicción: {e}")
            return 'A1', 0.5
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, epochs: int = 50):
        """Entrena el modelo."""
        if self.model is None:
            self.create_model()
        
        if isinstance(self.model, SimpleClassifier):
            self.model.fit(X_train, y_train)
        else:
            try:
                self.model.fit(X_train, y_train, epochs=epochs, batch_size=32, verbose=0)
                self.is_trained = True
            except Exception as e:
                print(f"Error al entrenar: {e}")
    
    def save_model(self, path: str):
        """Guarda el modelo entrenado."""
        try:
            if isinstance(self.model, SimpleClassifier):
                with open(path, 'wb') as f:
                    pickle.dump(self.model, f)
            else:
                self.model.save(path)
            print(f"✅ Modelo guardado en {path}")
        except Exception as e:
            print(f"Error guardando modelo: {e}")
    
    def load_model(self, path: str):
        """Carga un modelo guardado."""
        try:
            if path.endswith('.pkl'):
                with open(path, 'rb') as f:
                    self.model = pickle.load(f)
            else:
                from tensorflow import keras
                self.model = keras.models.load_model(path)
            self.is_trained = True
            print(f"✅ Modelo cargado desde {path}")
        except Exception as e:
            print(f"Error cargando modelo: {e}")


class SimpleClassifier:
    """Clasificador simple sin dependencias (fallback)."""
    
    def __init__(self, levels: list):
        self.levels = levels
        self.thresholds = [20, 40, 70, 100]  # Umbrales para cada nivel
    
    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        """Predice basado en accuracy (primer feature)."""
        accuracy = features[0][0] * 100  # Convertir a 0-100
        
        for i, threshold in enumerate(self.thresholds):
            if accuracy < threshold:
                # Confianza basada en distancia al umbral
                prev_threshold = self.thresholds[i-1] if i > 0 else 0
                confidence = (accuracy - prev_threshold) / (threshold - prev_threshold)
                return self.levels[i], min(max(confidence, 0.5), 0.99)
        
        return self.levels[-1], 0.95
    
    def fit(self, X, y):
        """Dummy fit (compatibilidad)."""
        pass
