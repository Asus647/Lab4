"""
Модуль генераторов для Варианта 2
"""

from string import ascii_lowercase
import random
from typing import Generator, List
from concurrent.futures import ThreadPoolExecutor, as_completed


class GeneratorException(Exception):
    """Пользовательское исключение для генераторов"""
    pass


def letter_combinations() -> Generator[str, None, None]:
    """
    Генератор всех сочетаний из двух латинских букв.
    Возвращает сочетания вида 'aa', 'ab', ..., 'zz'
    """
    try:
        for first in ascii_lowercase:
            for second in ascii_lowercase:
                yield f"{first}{second}"
    except Exception as e:
        raise GeneratorException(f"Ошибка в генераторе сочетаний: {e}")


def letter_combinations_threaded(count: int = 50) -> List[str]:
    """
    Многопоточная версия генератора сочетаний букв.
    
    Args:
        count: количество сочетаний для генерации
        
    Returns:
        Список сочетаний букв
    """
    if count <= 0:
        return []  # Возвращаем пустой список вместо исключения
    
    if count > 676:  # 26*26
        count = 676
    
    def generate_chunk(start_idx: int, end_idx: int) -> List[str]:
        """Генерация части сочетаний"""
        chunk = []
        for i in range(start_idx, end_idx):
            first = ascii_lowercase[i // 26]
            second = ascii_lowercase[i % 26]
            chunk.append(f"{first}{second}")
        return chunk
    
    total_combinations = 26 * 26
    chunk_size = total_combinations // 4  # 4 потока
    
    results = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        
        for start in range(0, total_combinations, chunk_size):
            end = min(start + chunk_size, total_combinations)
            futures.append(executor.submit(generate_chunk, start, end))
        
        for future in as_completed(futures):
            results.extend(future.result())
    
    return results[:count]


def function_generator(a: float, b: float, step: float = 0.01) -> Generator[float, None, None]:
    """
    Генератор значений функции f(x) = 0.1*x^2 + 5*x - 2
    
    Args:
        a: начальное значение x
        b: конечное значение x
        step: шаг изменения x
        
    Yields:
        Значения функции f(x) для каждого x
    """
    try:
        if a > b:
            raise ValueError("Начальное значение a должно быть меньше или равно b")
        
        if step <= 0:
            raise ValueError("Шаг должен быть положительным")
        
        x = a
        while x <= b + step/2:  # Добавляем половину шага для учета погрешности float
            yield 0.1 * x**2 + 5 * x - 2
            x += step
            
    except ValueError as e:
        raise GeneratorException(f"Некорректные параметры: {e}")
    except Exception as e:
        raise GeneratorException(f"Ошибка в генераторе функции: {e}")


def filter_long_cities(cities_str: str) -> Generator[str, None, None]:
    """
    Фильтр названий городов длиной более 5 символов.
    
    Args:
        cities_str: строка с названиями городов через пробел
        
    Yields:
        Названия городов длиной более 5 символов
    """
    try:
        if not cities_str.strip():
            raise ValueError("Строка с городами не может быть пустой")
        
        cities = cities_str.split()
        for city in cities:
            if len(city) > 5:
                yield city
                
    except Exception as e:
        raise GeneratorException(f"Ошибка в фильтре городов: {e}")


def get_first_n_items(generator, n: int):
    """
    Получение первых n элементов из генератора
    
    Args:
        generator: любой генератор или итератор
        n: количество элементов
        
    Returns:
        Список из n элементов
    """
    try:
        return [next(generator) for _ in range(n)]
    except StopIteration:
        return []
    except Exception as e:
        raise GeneratorException(f"Ошибка при получении элементов: {e}")

def get_first_n_items(generator, n: int):
    """
    Получение первых n элементов из генератора
    
    Args:
        generator: любой генератор или итератор
        n: количество элементов
        
    Returns:
        Список из n элементов
    """
    try:
        if n <= 0:
            return []
        
        result = []
        for _ in range(n):
            try:
                result.append(next(generator))
            except StopIteration:
                break
        return result
        
    except Exception as e:
        raise GeneratorException(f"Ошибка при получении элементов: {e}")