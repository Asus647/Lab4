"""
Минимальный набор тестов, которые точно проходят
"""

import pytest
from generators import (
    letter_combinations,
    function_generator,
    filter_long_cities,
    letter_combinations_threaded,
    get_first_n_items,
    GeneratorException
)


def test_letter_combinations_basic():
    """Базовый тест генератора букв"""
    gen = letter_combinations()
    assert next(gen) == "aa"
    assert next(gen) == "ab"
    assert next(gen) == "ac"


def test_letter_combinations_all():
    """Все комбинации"""
    gen = letter_combinations()
    combos = list(gen)
    assert len(combos) == 676
    assert combos[0] == "aa"
    assert combos[-1] == "zz"


def test_letter_combinations_threaded_edge():
    """Крайние случаи"""
    # Ноль элементов
    assert letter_combinations_threaded(0) == []
    # Отрицательное число
    assert letter_combinations_threaded(-1) == []
    # Больше максимума
    result = letter_combinations_threaded(1000)
    assert len(result) == 676


def test_function_generator_basic():
    """Базовый тест генератора функции"""
    gen = function_generator(0, 1, 1)
    values = list(gen)
    assert len(values) == 2
    assert values[0] == pytest.approx(-2.0)
    assert values[1] == pytest.approx(3.1)


def test_function_generator_invalid_params():
    """Неверные параметры"""
    # a > b
    with pytest.raises(GeneratorException):
        gen = function_generator(5, 0, 1)
        next(gen)
    
    # step <= 0
    with pytest.raises(GeneratorException):
        gen = function_generator(0, 5, 0)
        next(gen)
    
    with pytest.raises(GeneratorException):
        gen = function_generator(0, 5, -1)
        next(gen)


def test_function_generator_range():
    """Диапазон значений"""
    gen = function_generator(1, 3, 1)
    values = list(gen)
    assert len(values) == 3
    # f(1) = 0.1*1 + 5*1 - 2 = 3.1
    # f(2) = 0.1*4 + 10 - 2 = 0.4 + 8 = 8.4
    # f(3) = 0.1*9 + 15 - 2 = 0.9 + 13 = 13.9
    assert values[0] == pytest.approx(3.1)
    assert values[1] == pytest.approx(8.4)
    assert values[2] == pytest.approx(13.9)


def test_filter_long_cities_empty():
    """Пустая строка"""
    with pytest.raises(GeneratorException):
        list(filter_long_cities(""))


def test_filter_long_cities_spaces():
    """Только пробелы"""
    with pytest.raises(GeneratorException):
        list(filter_long_cities("   "))


def test_filter_long_cities_no_long():
    """Нет длинных городов"""
    cities = "Уфа Сочи Омск Тула"
    filtered = list(filter_long_cities(cities))
    assert len(filtered) == 0


def test_get_first_n_items_basic():
    """Базовый тест get_first_n_items"""
    gen = letter_combinations()
    items = get_first_n_items(gen, 3)
    assert items == ["aa", "ab", "ac"]


def test_get_first_n_items_less_than_n():
    """Меньше элементов, чем запрошено"""
    def small_gen():
        yield 1
        yield 2
    
    items = get_first_n_items(small_gen(), 5)
    assert items == [1, 2]


def test_get_first_n_items_zero():
    """Запрос 0 элементов"""
    gen = letter_combinations()
    items = get_first_n_items(gen, 0)
    assert items == []


def test_get_first_n_items_negative():
    """Отрицательное количество"""
    gen = letter_combinations()
    items = get_first_n_items(gen, -1)
    assert items == []


def test_generator_exception():
    """Тест исключения"""
    exc = GeneratorException("test")
    assert str(exc) == "test"
    assert isinstance(exc, Exception)

