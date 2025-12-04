"""
Главное окно приложения
"""

from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QTextEdit, QLineEdit, 
    QLabel, QGroupBox, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
import time

from generators import (
    letter_combinations, 
    function_generator, 
    filter_long_cities,
    letter_combinations_threaded,
    get_first_n_items
)


class GenerationThread(QThread):
    """Поток для генерации сочетаний букв"""
    progress = Signal(int)
    result = Signal(list)
    error = Signal(str)
    
    def __init__(self, count: int, use_threading: bool = False):
        super().__init__()
        self.count = count
        self.use_threading = use_threading
    
    def run(self):
        try:
            if self.use_threading:
                # Многопоточная генерация
                for i in range(10):
                    time.sleep(0.01)  # Имитация работы
                    self.progress.emit((i + 1) * 10)
                result = letter_combinations_threaded(self.count)
            else:
                # Однопоточная генерация
                gen = letter_combinations()
                result = []
                for i in range(self.count):
                    result.append(next(gen))
                    self.progress.emit(int((i + 1) / self.count * 100))
            
            self.result.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))


class GeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генераторы Python - Вариант 2")
        self.setGeometry(100, 100, 900, 700)
        
        # Установка стиля
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                font-family: 'Courier New';
                font-size: 12px;
            }
        """)
        
        self.init_ui()
        self.generation_thread = None
    
    def init_ui(self):
        """Инициализация интерфейса"""
        tabs = QTabWidget()
        
        # Вкладка 1: Сочетания букв
        tab1 = self.create_letters_tab()
        
        # Вкладка 2: Функция
        tab2 = self.create_function_tab()
        
        # Вкладка 3: Города
        tab3 = self.create_cities_tab()
        
        tabs.addTab(tab1, "🔤 Сочетания букв")
        tabs.addTab(tab2, "📈 Функция")
        tabs.addTab(tab3, "🏙️ Фильтр городов")
        
        self.setCentralWidget(tabs)
    
    def create_letters_tab(self) -> QWidget:
        """Создание вкладки с сочетаниями букв"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Генератор сочетаний из двух латинских букв")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Описание
        desc = QLabel("Генерирует все возможные сочетания от 'aa' до 'zz' (всего 676 комбинаций)")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Группа управления
        control_group = QGroupBox("Управление")
        control_layout = QVBoxLayout()
        
        # Кнопки
        btn_layout = QHBoxLayout()
        
        self.btn_generate_50 = QPushButton("Сгенерировать 50 сочетаний")
        self.btn_generate_50.clicked.connect(lambda: self.generate_letters(50, False))
        
        self.btn_generate_all = QPushButton("Сгенерировать все сочетания")
        self.btn_generate_all.clicked.connect(lambda: self.generate_letters(676, False))
        
        self.btn_threaded = QPushButton("Многопоточная генерация (50)")
        self.btn_threaded.clicked.connect(lambda: self.generate_letters(50, True))
        
        btn_layout.addWidget(self.btn_generate_50)
        btn_layout.addWidget(self.btn_generate_all)
        btn_layout.addWidget(self.btn_threaded)
        
        control_layout.addLayout(btn_layout)
        
        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        control_layout.addWidget(self.progress_bar)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Поле вывода
        self.text_output_letters = QTextEdit()
        self.text_output_letters.setReadOnly(True)
        layout.addWidget(self.text_output_letters)
        
        tab.setLayout(layout)
        return tab
    
    def create_function_tab(self) -> QWidget:
        """Создание вкладки с функцией"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Генератор значений функции f(x) = 0.1x² + 5x - 2")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Описание
        desc = QLabel("Диапазон: x ∈ [-5, 7], шаг: 0.01")
        layout.addWidget(desc)
        
        # Группа управления
        control_group = QGroupBox("Параметры")
        control_layout = QVBoxLayout()
        
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("Количество значений:"))
        
        self.spin_count = QLineEdit("20")
        self.spin_count.setMaximumWidth(100)
        param_layout.addWidget(self.spin_count)
        param_layout.addStretch()
        
        control_layout.addLayout(param_layout)
        
        self.btn_generate_function = QPushButton("Сгенерировать значения")
        self.btn_generate_function.clicked.connect(self.generate_function_values)
        control_layout.addWidget(self.btn_generate_function)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Поле вывода
        self.text_output_function = QTextEdit()
        self.text_output_function.setReadOnly(True)
        layout.addWidget(self.text_output_function)
        
        tab.setLayout(layout)
        return tab
    
    def create_cities_tab(self) -> QWidget:
        """Создание вкладки с фильтром городов"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Фильтр городов по длине названия")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Описание
        desc = QLabel("Фильтрует названия городов длиной более 5 символов")
        layout.addWidget(desc)
        
        # Поле ввода
        input_group = QGroupBox("Ввод данных")
        input_layout = QVBoxLayout()
        
        input_layout.addWidget(QLabel("Введите названия городов через пробел:"))
        
        self.input_cities = QLineEdit()
        self.input_cities.setPlaceholderText("Например: Москва Казань Санкт-Петербург Уфа Владивосток")
        self.input_cities.setText("Москва Казань Санкт-Петербург Уфа Владивосток Сочи")
        input_layout.addWidget(self.input_cities)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Кнопка
        self.btn_filter_cities = QPushButton("Отфильтровать города")
        self.btn_filter_cities.clicked.connect(self.filter_cities)
        layout.addWidget(self.btn_filter_cities)
        
        # Поле вывода
        self.text_output_cities = QTextEdit()
        self.text_output_cities.setReadOnly(True)
        layout.addWidget(self.text_output_cities)
        
        tab.setLayout(layout)
        return tab
    
    def generate_letters(self, count: int, use_threading: bool):
        """Генерация сочетаний букв"""
        if self.generation_thread and self.generation_thread.isRunning():
            return
        
        # Блокировка кнопок
        self.btn_generate_50.setEnabled(False)
        self.btn_generate_all.setEnabled(False)
        self.btn_threaded.setEnabled(False)
        
        # Показ прогресс-бара
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Создание потока
        self.generation_thread = GenerationThread(count, use_threading)
        self.generation_thread.progress.connect(self.progress_bar.setValue)
        self.generation_thread.result.connect(self.display_letters_result)
        self.generation_thread.error.connect(self.display_error)
        self.generation_thread.finished.connect(self.on_generation_finished)
        self.generation_thread.start()
    
    def display_letters_result(self, result):
        """Отображение результата генерации букв"""
        if len(result) <= 50:
            text = "\n".join(result)
        else:
            text = "\n".join(result[:50]) + f"\n\n... и еще {len(result) - 50} сочетаний"
        
        self.text_output_letters.setText(f"Всего сгенерировано: {len(result)} сочетаний\n\n{text}")
    
    def generate_function_values(self):
        """Генерация значений функции"""
        try:
            count = int(self.spin_count.text())
            if count <= 0:
                raise ValueError("Количество должно быть положительным")
            
            gen = function_generator(-5, 7, 0.01)
            values = get_first_n_items(gen, count)
            
            # Форматирование вывода
            formatted_values = []
            for i, value in enumerate(values, 1):
                formatted_values.append(f"{i:3d}. {value:10.4f}")
            
            self.text_output_function.setText("\n".join(formatted_values))
            
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректный ввод: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка генерации: {e}")
    
    def filter_cities(self):
        """Фильтрация городов"""
        try:
            cities_text = self.input_cities.text().strip()
            if not cities_text:
                raise ValueError("Введите названия городов")
            
            filtered = filter_long_cities(cities_text)
            cities_list = list(filtered)
            
            if not cities_list:
                self.text_output_cities.setText("Нет городов длиной более 5 символов")
                return
            
            # Получаем первые три города
            result = []
            filtered = filter_long_cities(cities_text)  # Создаем новый генератор
            for i in range(min(3, len(cities_list))):
                try:
                    result.append(next(filtered))
                except StopIteration:
                    break
            
            output = f"Найдено городов > 5 символов: {len(cities_list)}\n\n"
            output += "Первые три города:\n"
            output += "\n".join([f"{i+1}. {city}" for i, city in enumerate(result)])
            
            self.text_output_cities.setText(output)
            
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка фильтрации: {e}")
    
    def on_generation_finished(self):
        """Завершение генерации"""
        # Разблокировка кнопок
        self.btn_generate_50.setEnabled(True)
        self.btn_generate_all.setEnabled(True)
        self.btn_threaded.setEnabled(True)
        
        # Скрытие прогресс-бара
        self.progress_bar.setVisible(False)
        
        # Очистка потока
        self.generation_thread = None
    
    def display_error(self, error_msg):
        """Отображение ошибки"""
        QMessageBox.critical(self, "Ошибка", error_msg)
        self.on_generation_finished()
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.generation_thread and self.generation_thread.isRunning():
            self.generation_thread.terminate()
            self.generation_thread.wait()
        event.accept()