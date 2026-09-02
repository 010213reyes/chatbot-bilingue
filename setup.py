#!/usr/bin/env python
"""
Setup script para inicializar el entorno del chatbot bilingüe.
Instala dependencias, verifica la estructura y prepara el proyecto.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Imprime un encabezado formateado."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"✅ {text}")


def print_error(text):
    """Imprime un mensaje de error."""
    print(f"❌ {text}")


def check_python_version():
    """Verifica que Python 3.8+ esté instalado."""
    print_header("Verificando versión de Python")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Se requiere Python 3.8+, tienes {version.major}.{version.minor}")
        sys.exit(1)
    print_success(f"Python {version.major}.{version.minor}.{version.micro}")


def create_directories():
    """Crea las directorios necesarios."""
    print_header("Creando estructura de directorios")
    dirs = [
        "data/user_progress",
        "data/user_conversations",
        "data/levels",
        "logs",
        "models/trained",
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print_success(f"Directorio: {dir_path}/")


def create_env_file():
    """Crea el archivo .env desde .env.example si no existe."""
    print_header("Configurando archivo .env")
    if Path(".env").exists():
        print_success(".env ya existe")
        return
    
    if Path(".env.example").exists():
        with open(".env.example", "r") as src:
            content = src.read()
        with open(".env", "w") as dst:
            dst.write(content)
        print_success(".env creado desde .env.example")
    else:
        print_error(".env.example no encontrado")


def install_dependencies():
    """Instala las dependencias de Python."""
    print_header("Instalando dependencias")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print_success("Dependencias instaladas")
    except subprocess.CalledProcessError:
        print_error("Error al instalar dependencias")
        sys.exit(1)


def run_tests():
    """Ejecuta los tests del proyecto."""
    print_header("Ejecutando tests")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            capture_output=False,
        )
        if result.returncode == 0:
            print_success("Todos los tests pasaron")
        else:
            print_error(f"Tests fallaron con código {result.returncode}")
    except FileNotFoundError:
        print_error("pytest no encontrado. Salta esta verificación.")


def verify_imports():
    """Verifica que los módulos principales se puedan importar."""
    print_header("Verificando importaciones")
    try:
        from src.storage import SQLiteUserRepository
        print_success("SQLiteUserRepository importado")
        
        from src.advanced_chatbot import AdvancedBilingualChatbot
        print_success("AdvancedBilingualChatbot importado")
        
        from src.services import (
            ContextualLessonService,
            MemoryService,
            IntentionDetectorService,
            CorrectionValidatorService,
        )
        print_success("Todos los servicios importados")
    except ImportError as e:
        print_error(f"Error de importación: {e}")
        sys.exit(1)


def print_summary():
    """Imprime un resumen de la configuración."""
    print_header("Resumen de configuración")
    print("✅ Proyecto listo para usar")
    print("\n📝 Próximos pasos:")
    print("  1. Editar .env si es necesario")
    print("  2. Ejecutar: python src/advanced_chatbot.py")
    print("  3. O revisar: python demo_interactive.py")
    print()


def main():
    """Ejecuta el setup completo."""
    try:
        check_python_version()
        create_directories()
        create_env_file()
        verify_imports()
        print("\n" + "="*60)
        print("  Instalar dependencias? (pip install -r requirements.txt)")
        print("  Ejecuta: python setup.py --install")
        print("="*60 + "\n")
        
        if len(sys.argv) > 1 and sys.argv[1] == "--install":
            install_dependencies()
            run_tests()
        
        print_summary()
    except Exception as e:
        print_error(f"Error no controlado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
