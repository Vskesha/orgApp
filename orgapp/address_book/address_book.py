from classes_ab import AddressBook, Record, AddressBookFileHandler, Phone, Email, Birthday, Name
from functools import wraps

# Команди та описи для користувача
COMMANDS = {
    'add_email': ['add_email'],
    'add_phone_number': ['add_phone'],
    'add_record': ['add'],
    'change_email': ['change_email'],
    'change_phone_number': ['change_phone'],
    'days_to_birthday': ['when_birthday'],
    'exit': ['exit'],
    'find_records': ['find'],
    'get_all_records': ['all'],
    'get_birthdays_per_week': ['get_list'],
    'load_from_file': ['load'],
    'remove_email': ['remove_email'],
    'remove_phone_number': ['remove_phone'],
    'remove_record': ['remove'],
    'save_to_file': ['save'],
}

COMMAND_DESCRIPTIONS = {
    'Додати адресу електронної пошти': ['add_email'],
    'Додати номер телефону': ['add_phone'],
    'Додати контакт': ['add'],
    'Змінити адресу електронної пошти': ['change_email'],
    'Змінити номер телефону': ['change_phone'],
    'Дні до дня народження': ['when_birthday'],
    'Вийти': ['exit'],
    'Знайти контакт': ['find'],
    'Вивести всі контакти': ['all'],
    'Список іменнинників': ['get_birthdays_list'],
    'Завантажити з файлу': ['load'],
    'Видалити адресу електронної пошти': ['remove_email'],
    'Видалити номер телефону': ['remove_phone'],
    'Видалити контакт': ['remove'],
    'Зберегти до файлу': ['save'],
}


def print_command_list():
    num_columns = 2
    column_width = 50
    commands_list = list(COMMAND_DESCRIPTIONS.keys())
    formatted_commands = [f"{command} [{', '.join(COMMAND_DESCRIPTIONS[command])}]" for command in commands_list]
    middle = len(formatted_commands) // 2
    left_column = formatted_commands[:middle]
    right_column = formatted_commands[middle:]
    formatted_output = "\n".join(f"{left:<{column_width}} {right}" for left, right in zip(left_column, right_column))
    return formatted_output


def command_parser(user_input: str) -> tuple[callable, str]:
    if not user_input:
        raise IndexError("Nothing was entered ...")

    func, data = None, []
    lower_input_end_spaced = user_input.lower() + ' '

    for command, aliases in COMMANDS.items():
        for alias in aliases:
            if lower_input_end_spaced.startswith(alias + ' '):
                func = globals()[f'handle_{command}']
                data = user_input[len(alias) + 1:].strip()
                break
        if func:
            break

    if not func:
        raise ValueError(f"There is no such command {user_input.split()[0]}")

    return func, data


def validate_input(prompt, validator=None):
    while True:
        user_input = input(prompt).strip()
        if validator and not validator(user_input):
            continue
        return user_input


# Функції-обробники команд
def handle_add_email(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту: ").strip().lower()
    contact = address_book.get_record_by_name(name)

    if contact is not None:
        if contact.email:
            return f"Адреса електронної пошти для {name} вже існує: {contact.email.value}"
        else:
            new_email = input("Введіть нову адресу електронної пошти: ").strip()
            if contact.add_email(new_email):
                return f"Адресу електронної пошти успішно додано. \n{address_book.get_all_records()}"
            else:
                return "Не вдалося додати адресу електронної пошти. Адреса не валідна."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."


def handle_add_phone_number(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту: ").strip().lower()
    contact = address_book.get_record_by_name(name)

    if contact is not None:
        new_phone = input("Введіть новий номер телефону: ").strip()
        if contact.add_phone_number(new_phone):
            return f"Номер телефону успішно додано. \n{address_book.get_all_records()}"
        else:
            return "Не вдалося додати номер телефону. Номер не валідний."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."


def handle_add_record(arg: str, address_book: AddressBook) -> str:
    name = validate_input("Введіть ім'я контакту: ", lambda x: Name(x).validate(x))
    phone = validate_input("Введіть номер телефону контакту (+380________): ", lambda x: not x or Phone(x).validate(x))
    birthday = validate_input("Введіть день народження контакту (дд.мм.рррр): ",
                              lambda x: not x or Birthday(x).validate(x))
    email = validate_input("Введіть електронну пошту: ", lambda x: not x or Email(x).validate(x))

    new_record = Record(name)
    if phone:
        new_record.phones = [Phone(phone)]
    if birthday:
        new_record.birthday = Birthday(birthday)
    if email:
        new_record.email = Email(email)

    if address_book.add_record(new_record):
        return f"Контакт успішно додано до адресної книги. \n{address_book.get_all_records()}"
    else:
        return "Не вдалося додати контакт. Дані не валідні."


def handle_change_email(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту: ").strip().lower()
    contact = address_book.get_record_by_name(name)

    if contact is not None:
        old_email = validate_input("Введіть стару адресу електронної пошти: ")
        new_email = validate_input("Введіть нову адресу електронної пошти: ")

        if contact.change_email(old_email, new_email):
            return f"Адресу електронної пошти успішно змінено. \n{address_book.get_all_records()}"
        else:
            return "Не вдалося змінити адресу електронної пошти. Стара адреса не знайдена або нова адреса не валідна."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."


def handle_change_phone_number(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту: ").strip().lower()
    contact = address_book.get_record_by_name(name)

    if contact is not None:
        old_phone = validate_input("Введіть старий номер телефону: ")
        new_phone = validate_input("Введіть новий номер телефону: ")

        if not Phone(new_phone).validate(new_phone):
            return "Новий номер телефону не валідний."

        if contact.change_phone_number(old_phone, new_phone):
            return f"Номер телефону успішно змінено. \n{address_book.get_all_records()}"
        else:
            return "Не вдалося змінити номер телефону. Старий номер не знайдений або новий номер не валідний."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."


def handle_days_to_birthday(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту: ").strip().lower()
    contact = address_book.get_record_by_name(name)

    if contact is not None:
        if contact.birthday:
            days = contact.days_to_birthday()
            return f"До дня народження для {name} залишилося {days} днів."
        else:
            return f"Для контакта {name} не вказана дата народження."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."


def handle_exit(arg: str, address_book: AddressBook) -> str:
    return 'Goodbye!'


def handle_find_records(arg: str, address_book: AddressBook) -> str:
    search_criteria = {}

    print("За якими критеріями ви хочете здійснити пошук?\n1. Шукати за ім'ям\n2. Шукати за номером телефону")
    search_option = input("Виберіть опцію (1 або 2): ")

    if search_option == "1":
        search_name = input("Введіть ім'я для пошуку (мінімум 2 символи): ").strip().lower()
        if len(search_name) >= 2:
            search_criteria['name'] = search_name
        else:
            return "Ви ввели замало символів для імені. Пошук за іменем скасовано."
    elif search_option == "2":
        search_phones = input("Введіть частину номеру телефону для пошуку (мінімум 5 символів): ").strip()
        if len(search_phones) >= 5:
            search_criteria['phones'] = search_phones
        else:
            return "Ви ввели замало символів для номеру телефону. Пошук за номером телефону скасовано."
    else:
        return "Невірний вибір опціaї. Пошук скасовано."
    results = address_book.find_records(**search_criteria)
    if results:
        return f"Результати пошуку: \n{address_book.get_all_records()}"
    else:
        return "Контакти за вказаними критеріями не знайдені."


def handle_get_all_records(arg: str, address_book: AddressBook) -> str:
    return address_book.get_all_records()


def handle_get_birthdays_per_week(arg: str, address_book: AddressBook) -> str:
    while True:
        num_str = input("Введіть кількість днів: ")
        if num_str.isdigit():
            num = int(num_str)
            birthdays_list = address_book.get_birthdays_per_week(num)
            if birthdays_list:
                return "\n".join(birthdays_list)
            else:
                return "На цьому тижні немає іменнинників."
        else:
            print("Будь ласка, введіть ціле число.")
            continue


def handle_load_from_file(arg: str, address_book: AddressBook) -> str:
    file_handler = AddressBookFileHandler("address_book.json")
    loaded_address_book = file_handler.load_from_file()
    if loaded_address_book:
        address_book = loaded_address_book
        return "Адресну книгу завантажено з файлу."
    else:
        return "Не вдалося завантажити адресну книгу з файлу."


def handle_remove_email(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту: ").strip().lower()
    contact = address_book.get_record_by_name(name)

    if contact is not None:
        email_to_remove = validate_input("Введіть адресу електронної пошти для видалення: ")
        if contact.remove_email(email_to_remove):
            return f"Адресу електронної пошти успішно видалено. \n{address_book.get_all_records()}"
        else:
            return "Не вдалося видалити адресу електронної пошти. Адреса не знайдена."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."


def handle_remove_phone_number(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту: ").strip().lower()
    contact = address_book.get_record_by_name(name)

    if contact is not None:
        phone_to_remove = validate_input("Введіть номер телефону для видалення: ")
        if contact.remove_phone_number(phone_to_remove):
            return f"Номер телефону успішно видалено. \n{address_book.get_all_records()}"
        else:
            return "Не вдалося видалити номер телефону. Номер не знайдений."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."


def handle_remove_record(arg: str, address_book: AddressBook) -> str:
    name = input("Введіть ім'я контакту для видалення: ").strip().lower()
    if address_book.remove_record(name):
        return f"Контакт {name} успішно видалено з адресної книги. \n{address_book.get_all_records()}"
    else:
        return f"Контакт {name} не знайдено в адресній книзі або ще не додано жодного контакту."


def handle_save_to_file(arg: str, address_book: AddressBook) -> str:
    file_handler = AddressBookFileHandler("address_book.json")
    file_handler.save_to_file(address_book)
    return "Адресну книгу збережено у файл."


def input_error(func):
    """Wrapper for handling errors"""

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


def main_cycle(address_book: AddressBook) -> bool:
    """
    Return True if it needs to stop the program. False otherwise.
    """
    user_input = input('>>> ')
    func, argument = command_parser(user_input)
    result = func(argument, address_book)  # Передаємо адресну книгу як аргумент
    print(result)
    return result.endswith('Goodbye!')


def prepare() -> None:
    """
    Prints initial information to the user
    :return: None
    """
    print("Ласкаво просимо до адресної книги!")
    print(print_command_list())


def main():
    address_book = AddressBook()  # Створюємо об'єкт адресної книги

    prepare()

    while True:
        if main_cycle(address_book):
            break


if __name__ == '__main__':
    main()
