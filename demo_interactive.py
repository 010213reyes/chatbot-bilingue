"""
Script de demostración interactiva del chatbot.
Simula un flujo completo: evaluación → sesión → progresión.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.advanced_chatbot import AdvancedBilingualChatbot
from src.models.levels.level_manager import level_manager


def demo_interactive():
    """Demostración completa del flujo."""
    
    print("\n" + "="*70)
    print("🎮 DEMOSTRACIÓN INTERACTIVA DEL CHATBOT")
    print("="*70 + "\n")
    
    # Crear chatbot con usuario demo
    # Usar la carpeta actual como base
    contexts_file = 'data/contexts.json'
    
    bot = AdvancedBilingualChatbot(contexts_file, user_id="demo_user_interactive")
    
    print("✅ Orquestador inicializado\n")
    
    # Paso 1: Mostrar niveles
    print("─" * 70)
    print("PASO 1: Niveles Disponibles")
    print("─" * 70)
    for info in level_manager.list_all_levels():
        print(f"  {info['code']}: {info['nombre']}")
        print(f"    • Rango: {info['rango_puntaje'][0]}-{info['rango_puntaje'][1]}%")
        print(f"    • Contextos: {', '.join(info['contextos'])}\n")
    
    # Paso 2: Información de nivel actual
    print("─" * 70)
    print("PASO 2: Información del Nivel Actual")
    print("─" * 70)
    nivel_info = bot.get_level_info()
    print(f"  Nivel: {nivel_info['nivel']} ({nivel_info['nombre']})")
    print(f"  Rango: {nivel_info['rango_puntaje'][0]}-{nivel_info['rango_puntaje'][1]}%")
    print(f"  Contextos: {', '.join(nivel_info['contextos'])}")
    print(f"  Frases disponibles: {nivel_info['frases_disponibles']}\n")
    
    # Paso 3: Iniciar sesión de práctica
    print("─" * 70)
    print("PASO 3: Iniciando Sesión de Práctica")
    print("─" * 70)
    sesion = bot.start_practice_session()
    print(f"  ✅ Sesión iniciada")
    print(f"  Contexto: {sesion['contexto']['nombre']}")
    print(f"  Frases disponibles: {sesion['frases_totales']}\n")
    
    # Paso 4: Practicar 3 frases
    print("─" * 70)
    print("PASO 4: Practicando 3 Frases")
    print("─" * 70)
    
    respuestas = [
        ("¿Cómo digo 'Hola, ¿cómo estás?' en inglés?", "Hi, how are you?", True),
        ("¿Cómo digo 'Necesito ayuda' en inglés?", "I need help", True),
        ("¿Cómo digo 'Muy bien hecho' en inglés?", "Nice job", True),
    ]
    
    for pregunta, respuesta, es_demo in respuestas:
        frase_es = pregunta.replace("¿Cómo digo '", "").replace("' en inglés?", "")
        
        print(f"\n  👤 Pregunta: {pregunta}")
        print(f"  🤖 Respuesta usuario: {respuesta}")
        
        resultado = bot.submit_practice_answer(frase_es, respuesta)
        
        if resultado.get('correcto'):
            print(f"  ✅ CORRECTO!")
            print(f"     Significado: {resultado['respuesta_correcta']}")
        else:
            print(f"  ❌ Incorrecto")
            print(f"     Respuesta correcta: {resultado['respuesta_correcta']}")
        
        print(f"     Uso: {resultado['uso']}")
        
        if 'milestone' in resultado:
            print(f"  🎯 Hito: {resultado['milestone']['preguntas']} preguntas")
            print(f"     Accuracy: {resultado['milestone']['accuracy']}")
    
    # Paso 5: Finalizar sesión
    print("\n" + "─" * 70)
    print("PASO 5: Finalizando Sesión")
    print("─" * 70)
    
    result_sesion = bot.end_session()
    
    print(f"  Duración: {result_sesion['duracion_minutos']} minutos")
    print(f"  Preguntas: {result_sesion['preguntas_totales']}")
    print(f"  Aciertos: {result_sesion['aciertos']}/{result_sesion['preguntas_totales']}")
    print(f"  Accuracy: {result_sesion['accuracy']}")
    print(f"  Frases aprendidas: {result_sesion['frases_aprendidas']}\n")
    
    # Paso 6: Verificar progreso
    print("─" * 70)
    print("PASO 6: Resumen de Progreso")
    print("─" * 70)
    
    progreso = result_sesion['resumen']
    print(f"  Usuario: {progreso['user_id']}")
    print(f"  Nivel actual: {progreso['nivel_actual']}")
    print(f"  Nivel máximo alcanzado: {progreso['nivel_maximo']}")
    print(f"  Frases aprendidas: {progreso['frases_aprendidas']}")
    print(f"  Sesiones: {progreso['sesiones_completadas']}")
    print(f"  Accuracy promedio: {progreso['accuracy_promedio']}")
    print(f"  Días activo: {progreso['dias_activo']}\n")
    
    # Paso 7: Información de progresión
    print("─" * 70)
    print("PASO 7: Información de Progresión")
    print("─" * 70)
    
    adv = result_sesion['advancement']
    print(f"  ¿Puede avanzar?: {adv['puede_avanzar']}")
    print(f"  Motivo: {adv['motivo']}")
    if adv.get('siguiente_nivel'):
        print(f"  Siguiente nivel: {adv['siguiente_nivel']}")
    print()
    
    # Paso 8: Datos persistidos
    print("─" * 70)
    print("PASO 8: Datos Persistidos en JSON")
    print("─" * 70)
    print(f"  Ubicación: data/user_progress/demo_user_interactive.json")
    print(f"  ✅ Progreso guardado automáticamente")
    
    # Leer archivo generado
    import json
    user_file = os.path.join(
        os.path.dirname(__file__),
        f'../data/user_progress/demo_user_interactive.json'
    )
    
    if os.path.exists(user_file):
        with open(user_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
        
        print(f"\n  Datos guardados:")
        print(f"    • nivel_actual: {user_data['nivel_actual']}")
        print(f"    • sesiones: {len(user_data['sesiones'])}")
        print(f"    • frases_aprendidas: {len(user_data['frases_aprendidas'])}")
        print(f"    • accuracy_promedio: {user_data['estadisticas']['accuracy_promedio']:.2%}\n")
    
    print("="*70)
    print("✨ DEMOSTRACIÓN COMPLETA - PROYECTO FUNCIONAL 100%")
    print("="*70 + "\n")


if __name__ == '__main__':
    demo_interactive()
