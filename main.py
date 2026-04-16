# filepath: main.py
"""
GameOptimizer AI — точка входа.
Запуск: python main.py
"""

import sys
import os

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """Проверить наличие зависимостей."""
    missing = []

    try:
        import customtkinter
    except ImportError:
        missing.append("customtkinter")

    try:
        import psutil
    except ImportError:
        missing.append("psutil")

    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")

    if missing:
        print("❌ Не хватает зависимостей. Установи их командой:")
        print(f"   pip install {' '.join(missing)}")
        print("\nИли установи все зависимости:")
        print("   pip install -r requirements.txt")
        sys.exit(1)


def main():
    check_dependencies()

    # Создаём нужные директории
    os.makedirs("logs", exist_ok=True)
    os.makedirs("assets/images", exist_ok=True)

    # Запускаем приложение
    from ui.app import MainApp

    app = MainApp()
    app.mainloop()


if __name__ == "__main__":
    main()
