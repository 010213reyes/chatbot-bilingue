# Fase 1: Base Contextual del Chatbot

## ✅ Completado

### Arquitectura
- **ContextManager**: Gestiona contextos, frases y búsquedas
- **SpanishChatbot**: Responde en español, enseña inglés contextualmente

### Contextos Implementados
1. **Videojuegos - General**: Frases básicas (5 frases)
2. **Videojuegos - Batalla**: Comunicación en combate (5 frases)
3. **Videojuegos - Coordinación**: Estrategia y táctica (5 frases)
4. **Saludos Básicos**: Presentaciones y despedidas (5 frases)

### Funcionalidades Base
✅ Buscar traducción de frases españolas al inglés  
✅ Traducir frases en inglés al español  
✅ Practicar con frases aleatorias  
✅ Visualizar lecciones de vocabulario por contexto  
✅ Sistema de contextos extensible  

### Estructura de Datos (contexts.json)
Cada frase incluye:
- Español
- Inglés principal
- Alternativas en inglés
- Contexto de uso

### Ejemplo de Funcionamiento

```
👤 Usuario: ¿Cómo digo 'Necesito ayuda' en inglés?
🤖 Bot: En Videojuegos - General, para decir 'Necesito ayuda', 
        puedes usar: 'I need help'. Uso: Pedir asistencia en el juego

👤 Usuario: ¿Qué significa 'Nice job'?
🤖 Bot: 'Nice job' significa 'Muy bien hecho'. 
        Se usa en: Felicitar a un compañero
```

## 📁 Archivos Creados
- `data/contexts.json` - Base de contextos y frases
- `src/models/context_manager.py` - Gestor de contextos
- `src/chatbot.py` - Lógica principal del chatbot

## 🎯 Próxima Fase

**Red Neuronal para enseñanza progresiva**
- Evaluar nivel del usuario
- Adaptar dificultad de frases
- Rastrear palabras aprendidas
- Sistema de repaso espaciado

## 🔧 Para Correr

```powershell
cd "c:\Users\REYES\OneDrive\Desktop\chatbot-bilingue"
venv\Scripts\python.exe src/chatbot.py
```
