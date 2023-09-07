"""
Також файл для Олі і Олега
Оля перероби не через іфи а через виклик окремих функцій-хендлерів,
які є ключами для команд (Приблизно кожен if є окремою функцією handle_XXX()
додайте відповідні команди до COMMANDS і реалізуйте відповідні handler
Хендлер приймає строку (все, що введено в консолі після назви команди) і повертає строку
"""
from functools import wraps
import json

# Клас для представлення нотаток
class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

# Клас для управління нотатками
class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note(self, title, content):
        note = Note(title, content)
        self.notes.append(note)

    def save_notes_to_json(self, filename):
        data = []
        for note in self.notes:
            data.append({
                "title": note.title,
                "content": note.content
            })

        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

    def load_notes_from_json(self, filename):
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                data = json.load(file)
                self.notes = []
                for note_data in data:
                    self.add_note(note_data["title"], note_data["content"])
        except FileNotFoundError:
            pass

    def search_notes(self, keyword):
        results = []
        for note in self.notes:
            if keyword in note.title or keyword in note.content:
                results.append(note)
        return results

# Функція-хендлер для додавання нотатки
def add_note_handler(note_manager, args):
    title = input("Введіть заголовок нотатки: ")
    content = input("Введіть текст нотатки: ")
    note_manager.add_note(title, content)
    return "Нотатка додана успішно."

# Функція-хендлер для збереження нотаток в JSON-файл
def save_notes_handler(note_manager, args):
    filename = args[0] if args else input("Введіть ім'я файлу для збереження: ")
    note_manager.save_notes_to_json(filename)
    return f"Нотатки збережено в файлі {filename}"

# Функція-хендлер для завантаження нотаток з JSON-файлу
def load_notes_handler(note_manager, args):
    filename = args[0] if args else input("Введіть ім'я файлу для завантаження: ")
    note_manager.load_notes_from_json(filename)
    return f"Нотатки завантажено з файлу {filename}"

# Функція-хендлер для пошуку нотаток
def search_notes_handler(note_manager, args):
    keyword = args[0] if args else input("Введіть ключове слово для пошуку: ")
    search_results = note_manager.search_notes(keyword)
    if search_results:
        result_str = "Результати пошуку:\n"
        for idx, result in enumerate(search_results, 1):
            result_str += f"{idx}. Заголовок: {result.title}\n"
            result_str += f"   Текст: {result.content}\n"
        return result_str
    else:
        return "Нотатки не знайдено за цим ключовим словом."

# Функція-хендлер для виходу
def exit_handler(note_manager, args):
    filename = args[0] if args else input("Введіть ім'я файлу для збереження: ")
    note_manager.save_notes_to_json(filename)
    return 'Goodbye!'

# Карта команд і відповідних їм функцій-хендлерів
COMMANDS = {
    'add': add_note_handler,
    'save': save_notes_handler,
    'load': load_notes_handler,
    'search': search_notes_handler,
    'exit': exit_handler,
    'close': exit_handler,
    'bye': exit_handler,
    'goodbye': exit_handler,
}

# Обробник помилок для введення
def input_error(func):
    """Обгортка для обробки помилок"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except IndexError as e:
            print('Not enough data.', str(e))
        except ValueError as e:
            print('Wrong value.', str(e))
        except KeyError as e:
            print('Wrong key.', str(e)[1:-1])
        except TypeError as e:
            print('Wrong type of value.', str(e))
    return wrapper

# Парсер команд для отримання відповідного обробника і аргумента
def command_parser(user_input: str) -> tuple[callable, str]:
    """
    Вибирає і повертає відповідний обробник та аргумент цього обробника
    з user_input відповідно до COMMANDS
    :param user_input: Рядок, який повинен починатися з команди, за якою може слідувати ім'я та номер телефону, якщо потрібно
    :return: Кортеж функції та аргумента рядка
    """
    if not user_input:
        raise IndexError("Nothing was entered ...")

    func, data = None, []
    lower_input_end_spaced = user_input.lower() + ' '
    for command in COMMANDS:
        if lower_input_end_spaced.startswith(command.lower() + ' '):
            func = COMMANDS[command]
            data = user_input[len(command):].strip()

    if not func:
        return None, data  # Повертаємо None для обробки "Команда не існує"

    return func, data

# Функція для виведення меню з командами
def print_menu():
    print("Доступні команди:")
    for command in COMMANDS:
        print(f"- {command}")

# Підготовка до запуску програми
def prepare() -> None:
    """
    Виводить початкову інформацію користувачеві
    :return: None
    """
    print("Ласкаво просимо до вашого нотатникового застосунку!")
    print_menu()  # Виводимо меню з командами

# Основна функція програми
def main_cycle(note_manager, filename) -> bool:
    """
    Повертає True, якщо потрібно завершити програму. False в іншому випадку.
    """
    user_input = input('>>> ')
    func, argument = command_parser(user_input)
    if func is None:
        print("Команда не існує")
        return False
    result = func(note_manager, argument)
    print(result)
    return result.endswith('Goodbye!')

# Початкова ініціалізація
if __name__ == '__main__':
    filename = "my_notes.json"  # Ім'я файлу для збереження нотаток
    note_manager = NoteManager()  # Створення об'єкту для управління нотатками
    note_manager.load_notes_from_json(filename)  # Завантаження нотаток з файлу
    prepare()  # Виведення початкової інформації
    while True:
        if main_cycle(note_manager, filename):
            break

