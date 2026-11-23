from functools import wraps
from typing import Callable


def input_error(func: Callable) -> Callable:
    """
    Декоратор для обробки помилок введення користувача (KeyError, ValueError, IndexError).
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found."

    return inner


def parse_input(user_input: str) -> tuple[str, ...]:
    """
    Розбирає введений рядок на команду (у нижньому регістрі) та список аргументів.
    """
    parts = user_input.strip().split()
    if not parts:
        return ("",)
    cmd, *args = parts
    return cmd.lower(), *args


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Додає новий контакт у словник."""
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """Оновлює номер телефону для існуючого контакту."""
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """Повертає номер телефону за вказаним ім'ям."""
    name = args[0]
    return contacts[name]


@input_error
def show_all(contacts: dict[str, str]) -> str:
    """Повертає всі збережені контакти у вигляді відформатованого рядка."""
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


def main() -> None:
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
