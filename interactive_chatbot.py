#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHATBOT BILINGÜE INTERACTIVO
Versión completamente interactiva - El usuario responde en tiempo real
"""

import os
import sys
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models.context_manager import ContextManager
from models.levels.level_manager import level_manager
from models.levels.level_mapper import LevelMapper
from models.neural.level_classifier import LevelClassifier
from services.evaluation_service import EvaluationService
from services.progress_tracker import ProgressTracker


class InteractiveBilingualChatbot:
    """Chatbot interactivo que responde en tiempo real"""

    def __init__(self, contexts_file="data/contexts.json"):
        self.contexts_file = contexts_file
        self.user_id = None
        
        # Cargar componentes comunes (sin ProgressTracker)
        self.context_manager = ContextManager(contexts_file)
        self.level_manager = level_manager  # Usar la instancia global
        self.level_mapper = LevelMapper(contexts_file)  # Pasar la ruta, no el objeto
        self.level_classifier = LevelClassifier()
        self.evaluation_service = EvaluationService(self.level_mapper)
        self.progress_tracker = None  # Se inicializa cuando se obtiene el user_id
        
        # Estado de sesión
        self.current_level = None
        self.current_context = None
        self.session_stats = {}
        self.current_user = None
    
    def init_user(self, user_id: str):
        """Inicializar ProgressTracker con el user_id"""
        self.user_id = user_id
        self.progress_tracker = ProgressTracker(user_id)

    def display_banner(self):
        """Mostrar banner inicial"""
        print("\n" + "="*70)
        print("🌍 CHATBOT BILINGÜE - MODO INTERACTIVO 🌍".center(70))
        print("Aprende inglés de forma adaptativa".center(70))
        print("="*70 + "\n")

    def get_or_create_user(self):
        """Obtener nombre del usuario"""
        print("👤 Bienvenido al Chatbot Bilingüe de Inglés\n")
        user_id = input("¿Cuál es tu nombre? (o presiona Enter para usuario demo): ").strip()
        
        if not user_id:
            user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Inicializar ProgressTracker con el user_id
        self.init_user(user_id)
        
        # Los datos del usuario ya están cargados en self.progress_tracker.data
        self.current_user = self.progress_tracker.data
        
        # Verificar si el usuario es nuevo (sin sesiones) o existente
        if len(self.current_user.get('sesiones', [])) > 0:
            print(f"✅ Bienvenido de vuelta, {user_id}!")
            print(f"   Tu nivel actual: {self.current_user.get('nivel_actual', 'A1')}")
            self.current_level = self.current_user.get('nivel_actual', 'A1')
        else:
            print(f"\n📝 Hola {user_id}, vamos a comenzar tu evaluación inicial...")
            self.current_level = 'A1'
        
        return user_id

    def initial_evaluation(self):
        """Realizar evaluación inicial interactiva"""
        print("\n" + "="*70)
        print("🧪 PRUEBA DE NIVEL INICIAL".center(70))
        print("="*70)
        print("\nResponde las siguientes preguntas en inglés.")
        print("(No importa si no es perfecto - es para calibrar tu nivel)\n")
        
        evaluation = self.evaluation_service.create_initial_evaluation()
        questions = evaluation.get('questions', [])
        
        correct_answers = 0
        user_answers = []
        
        for idx, question in enumerate(questions):
            print(f"\n📌 Pregunta {idx + 1}/{len(questions)}")
            print(f"Español: {question['es']}")
            print(f"Contexto: {question.get('contexto', 'general')}")
            
            user_answer = input("\nTu respuesta en inglés: ").strip()
            
            if not user_answer:
                print("⚠️  Respuesta vacía, intentando de nuevo...")
                user_answer = input("Tu respuesta en inglés: ").strip()
            
            result = self.evaluation_service.check_answer(idx, user_answer)
            is_correct = result.get('correcto', False)
            
            user_answers.append({
                'question': question['es'],
                'expected': question['en_correcta'],
                'user_answer': user_answer,
                'correct': is_correct
            })
            
            if is_correct:
                print("✅ ¡Correcto!")
                correct_answers += 1
            else:
                print(f"❌ Incorrecto. La respuesta correcta era: {result.get('respuesta_correcta')}")
        
        # Calcular nivel
        accuracy = (correct_answers / len(questions)) * 100
        assigned_level = self.level_manager.get_level_by_score(accuracy)
        
        print("\n" + "="*70)
        print("📊 RESULTADOS DE LA EVALUACIÓN".center(70))
        print("="*70)
        print(f"\nRespuestas correctas: {correct_answers}/{len(questions)}")
        print(f"Accuracy: {accuracy:.1f}%")
        print(f"\n🎯 Nivel asignado: {assigned_level.code}")
        
        # Descripción del nivel
        level_info = self.level_manager.get_level_by_code(assigned_level.code)
        print(f"   {level_info.nombre}\n")
        
        self.current_level = assigned_level.code
        self.progress_tracker.update_level(assigned_level.code)
        return assigned_level.code

    def practice_session(self):
        """Sesión de práctica interactiva"""
        print("\n" + "="*70)
        print("🎓 SESIÓN DE PRÁCTICA".center(70))
        print("="*70 + "\n")
        
        # Seleccionar contexto
        print("📚 Contextos disponibles para tu nivel:\n")
        phrases_by_level = self.level_mapper.get_phrases_by_level(self.current_level)
        
        if not phrases_by_level:
            print("⚠️  No hay frases disponibles para tu nivel.")
            return
        
        # Agrupar por contexto
        contexts = {}
        for phrase in phrases_by_level:
            ctx = phrase.get('contexto', 'general')
            if ctx not in contexts:
                contexts[ctx] = []
            contexts[ctx].append(phrase)
        
        context_list = list(contexts.keys())
        for idx, ctx in enumerate(context_list, 1):
            print(f"{idx}. {ctx} ({len(contexts[ctx])} frases)")
        
        while True:
            try:
                choice = int(input(f"\nElige un contexto (1-{len(context_list)}): "))
                if 1 <= choice <= len(context_list):
                    selected_context = context_list[choice - 1]
                    break
                else:
                    print(f"Por favor, elige entre 1 y {len(context_list)}")
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número.")
        
        selected_phrases = contexts[selected_context]
        
        # Práctica con frases
        print(f"\n✨ Practicando: {selected_context}")
        print(f"Total de frases: {len(selected_phrases)}\n")
        
        correct = 0
        practiced = 0
        
        for phrase in selected_phrases:
            print("-" * 70)
            spanish = phrase['es']
            english = phrase['en']
            
            print(f"\n🇪🇸 Español: {spanish}")
            print(f"💡 Contexto: {phrase.get('uso', 'uso general')}")
            
            user_answer = input("🇬🇧 ¿Cómo se dice en inglés?: ").strip()
            
            if not user_answer:
                print("⚠️  Respuesta vacía, saltando...")
                continue
            
            is_correct = self.evaluation_service.check_answer(english, user_answer)
            practiced += 1
            
            if is_correct:
                print(f"✅ ¡Correcto! '{english}'")
                correct += 1
            else:
                print(f"❌ Incorrecto.")
                print(f"   Respuesta correcta: {english}")
                if phrase.get('en_alt'):
                    print(f"   También aceptado: {', '.join(phrase['en_alt'])}")
        
        # Resumen
        print("\n" + "="*70)
        print("📊 RESUMEN DE LA SESIÓN".center(70))
        print("="*70)
        accuracy = (correct / practiced * 100) if practiced > 0 else 0
        print(f"\nFrases practicadas: {practiced}")
        print(f"Respuestas correctas: {correct}/{practiced}")
        print(f"Accuracy: {accuracy:.1f}%")
        
        if accuracy >= 70:
            print("\n🎉 ¡Muy bien! Consideras avanzar de nivel.")
        else:
            print("\n💪 Sigue practicando, lo harás mejor.")
        
        # Guardar progreso
        self.progress_tracker.add_session(
            {
                'duracion': 0.0,
                'frases': practiced,
                'aciertos': correct,
                'total': practiced,
                'contextos': [selected_context]
            }
        )
        
        for phrase in selected_phrases[:correct]:
            self.progress_tracker.mark_phrase_learned(
                phrase['en'],
                self.current_level
            )
        
        if accuracy >= 70 and practiced >= 3:
            next_level = self.level_manager.get_next_level(self.current_level)
            if next_level:
                self.progress_tracker.update_level(next_level)
                print(f"\n🚀 ¡Subiste a nivel {next_level}!")
                self.current_level = next_level

    def show_progress(self):
        """Mostrar progreso del usuario"""
        print("\n" + "="*70)
        print("📈 TU PROGRESO".center(70))
        print("="*70 + "\n")
        
        user_data = self.progress_tracker.data
        
        if not user_data:
            print("No hay datos de progreso aún.")
            return
        
        print(f"Usuario: {user_data.get('user_id')}")
        print(f"Nivel actual: {user_data.get('nivel_actual', 'N/A')}")
        print(f"Nivel máximo: {user_data.get('nivel_maximo', 'N/A')}")
        print(f"\nEstadísticas:")
        stats = user_data.get('estadisticas', {})
        print(f"  - Sesiones completadas: {stats.get('total_sesiones', 0)}")
        print(f"  - Total de preguntas: {stats.get('total_preguntas', 0)}")
        print(f"  - Aciertos totales: {stats.get('aciertos_totales', 0)}")
        print(f"  - Accuracy promedio: {stats.get('accuracy_promedio', 0):.1%}")
        
        print(f"\nFrases aprendidas: {len(user_data.get('frases_aprendidas', []))}")
        
        # Mostrar frases para repasar
        next_review = self.progress_tracker.get_next_review_phrases()
        if next_review:
            print(f"\n📅 Frases para repasar hoy: {len(next_review)}")

    def main_menu(self):
        """Menú principal interactivo"""
        self.display_banner()
        self.get_or_create_user()
        
        # Primera vez: evaluación inicial
        if not self.current_user:
            self.initial_evaluation()
        
        # Menú principal
        while True:
            print("\n" + "="*70)
            print(f"NIVEL ACTUAL: {self.current_level}".center(70))
            print("="*70)
            print("\n¿Qué deseas hacer?\n")
            print("1. 🎓 Practicar frases")
            print("2. 📈 Ver mi progreso")
            print("3. 🧪 Hacer evaluación de nivel")
            print("4. ❌ Salir")
            
            choice = input("\nTu opción (1-4): ").strip()
            
            if choice == "1":
                self.practice_session()
            elif choice == "2":
                self.show_progress()
            elif choice == "3":
                self.initial_evaluation()
            elif choice == "4":
                print("\n👋 ¡Gracias por usar el Chatbot Bilingüe!")
                print("   Sigue practicando y mejorarás cada día.\n")
                break
            else:
                print("❌ Opción no válida. Por favor, elige entre 1 y 4.")


def main():
    try:
        bot = InteractiveBilingualChatbot()
        bot.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario.")
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Asegúrate de ejecutar el script desde la carpeta raíz del proyecto.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
