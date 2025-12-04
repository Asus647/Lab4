"""
Точка входа в приложение
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import GeneratorApp


def main():
    """Основная функция запуска приложения"""
    try:
        # Создание приложения
        app = QApplication(sys.argv)
        app.setApplicationName("Генераторы Python - Вариант 2")
        app.setOrganizationName("Python Lab")
        
        # Создание и отображение главного окна
        window = GeneratorApp()
        window.show()
        
        # Запуск цикла обработки событий
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}")
        return 1


if __name__ == "__main__":
    main()