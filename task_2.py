import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Аналізує текст і генерує всі дійсні числа, відокремлені пробілами з обох боків.
    """
    # Шукаємо числа, перед якими і після яких стоїть пробіл або межа рядка
    pattern = r"(?<=\s)\d+(?:\.\d+)?(?=\s)|^\d+(?:\.\d+)?(?=\s)|(?<=\s)\d+(?:\.\d+)?$"
    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Підсумовує всі дійсні числа у тексті, використовуючи передану функцію-генератор.
    """
    return sum(func(text))


# Приклад перевірки:
if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # Виведе: Загальний дохід: 1351.46
