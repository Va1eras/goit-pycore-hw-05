import sys
from collections import Counter


def parse_log_line(line: str) -> dict[str, str]:
    """
    Парсить рядок логу у словник із ключами: date, time, level, message.
    """
    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"Некоректний формат рядка логу: '{line.strip()}'")

    date, time, level, message = parts
    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
    }


def load_logs(file_path: str) -> list[dict[str, str]]:
    """
    Завантажує логи з файлу та повертає список розпарсених записів.
    """
    logs: list[dict[str, str]] = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    logs.append(parse_log_line(line))
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдено.")
        sys.exit(1)
    except ValueError as e:
        print(f"Помилка читання логів: {e}")
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: list[dict[str, str]], level: str) -> list[dict[str, str]]:
    """
    Фільтрує список логів за вказаним рівнем логування (використано filter та lambda).
    """
    target_level = level.upper()
    return list(filter(lambda log: log["level"] == target_level, logs))


def count_logs_by_level(logs: list[dict[str, str]]) -> dict[str, int]:
    """
    Підраховує кількість записів для кожного рівня логування.
    """
    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict[str, int]) -> None:
    """
    Виводить статистику за рівнями логування у вигляді форматованої таблиці.
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16} | {count}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Використання: python task_3.py <шлях_до_файлу_логів> [рівень_логування]")
        sys.exit(1)

    file_path = sys.argv[1]
    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # Якщо передано другий аргумент — виводимо деталі за вказаним рівнем
    if len(sys.argv) >= 3:
        level = sys.argv[2].upper()
        filtered_logs = filter_logs_by_level(logs, level)
        print(f"\nДеталі логів для рівня '{level}':")
        if filtered_logs:
            for log in filtered_logs:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print(f"Записів із рівнем '{level}' не знайдено.")


if __name__ == "__main__":
    main()
