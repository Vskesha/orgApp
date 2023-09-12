from classes_ab import AddressBook, Record, AddressBookFileHandler, Phone, Email, Birthday, Name
from functools import wraps
from colorama import init as init_colorama, Fore, Style
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt
from pathlib import Path


ADDRESSBOOK_LOGO = """
                .o8        .o8                                       
               "888       "888                                       
 .oooo.    .oooo888   .oooo888  oooo d8b  .ooooo.   .oooo.o  .oooo.o 
`P  )88b  d88' `888  d88' `888  `888""8P d88' `88b d88(  "8 d88(  "8 
 .oP"888  888   888  888   888   888     888ooo888 `"Y88b.  `"Y88b.  
d8(  888  888   888  888   888   888     888    .o o.  )88b o.  )88b 
`Y888""8o `Y8bod88P" `Y8bod88P" d888b    `Y8bod8P' 8""888P' 8""888P' 

             .o8                           oooo        
            "888                           `888        
             888oooo.   .ooooo.   .ooooo.   888  oooo  
             d88' `88b d88' `88b d88' `88b  888 .8P'   
             888   888 888   888 888   888  888888.    
             888   888 888   888 888   888  888 `88b.  
             `Y8bod8P' `Y8bod8P' `Y8bod8P' o888o o888o 
"""

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
    'help': ['help']
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
    'Список іменнинників за N днів': ['get_list'],
    'Завантажити з файлу': ['load'],
    'Видалити адресу електронної пошти': ['remove_email'],
    'Видалити номер телефону': ['remove_phone'],
    'Видалити контакт': ['remove'],
    'Зберегти до файлу': ['save'],
    'Вивести цю довідку': ['help']
}

FILE_PATH = Path.home() / "orgApp" / "address_book.json"  # for working on different filesystems
FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

class RainbowLexer(Lexer):
    """
    Lexer for rainbow syntax highlighting.

    This lexer assigns colors to characters based on the rainbow spectrum.
    """

    def lex_document(self, document):
        colors = list(sorted({"Teal": "#028000"}, key=NAMED_COLORS.get))

        def get_line(lineno):
            return [
                (colors[i % len(colors)], c)
                for i, c in enumerate(document.lines[lineno])
            ]

        return get_line

def print_command_list():
    """
    Generate a formatted list of available commands with their descriptions.
    This function formats the list of available commands and their descriptions
    in a user-friendly way for display.
    """
    print(Fore.GREEN, "Доступні команди:")
    separator = '|----------------------|-----------------------------------------|'
    print(separator, f'\n|       Команди        |      Опис {" ":30}|\n', separator, sep='')
    for description, commands in COMMAND_DESCRIPTIONS.items():
        print(f"| {Fore.WHITE} {', '.join(commands):<20}{Fore.GREEN}| {description:<40}|")
    print(separator, '\n')


def command_parser(user_input: str) -> tuple[callable, str]:
    """
    Parse user input to determine the corresponding command and data.
    This function parses the user's input to identify the command they want to
    execute and the associated data, if any..
    """
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


def validate_input(prompt, validator=None, error_message=None, final_error_message=None, transform_func=None):
    """
    Prompt the user for input and validate it using a specified validator function.
    This function prompts the user for input, checks it, and if it doesn't pass
    the validation check, it prompts the user for input again. If no validator is
    provided, any non-empty input is considered valid.
    """
    user_input = input(prompt).strip()
    if not user_input:
        return None
    if validator:
        attempts = 2
        while not validator(user_input):
            if error_message:
                print(error_message)
            attempts -= 1
            if attempts == 0:
                if final_error_message:
                    print(final_error_message)
                return None
            user_input = input(prompt).strip()  # Перепитати користувача
    if transform_func:
        user_input = transform_func(user_input)
    return user_input

validation_info = {
    "name": {
        "prompt": "Введіть ім'я контакту: ",
        "validator": lambda x: Name(x).validate(x),
        "error_message": "Недійсне ім'я. Будь ласка, використовуйте лише букви і більше однієї. Спробуйте знову!!!",
        "final_error_message": "Спроби закінчилися при введенні імені.",
        "transform_func": lambda x: x.lower().strip()

    },
    "phone": {
        "prompt": "Введіть номер телефону (+380________): ",
        "validator": lambda x: not x or Phone(x).validate(x),
        "error_message": "Телефон не відповідає формату (+380________). Спробуйте ще раз!!!",
        "final_error_message": "Спроби закінчилися при введенні телефону.",
        "transform_func": lambda x: x.strip()
    },
    "email": {
        "prompt": "Введіть електронну пошту у прийнятному форматі: ",
        "validator": lambda x: not x or Email(x).validate(x),
        "error_message": "Формат пошти не прийнятyний. Спобуй знову!!!",
        "final_error_message": "Спроби закінчилися при введенні електронної пошти.",
        "transform_func": lambda x: x.strip()
    },
    "birthday": {
        "prompt": "Введіть день народження контакту у форматі (дд.мм.рррр): ",
        "validator": lambda x: not x or Birthday(x).validate(x),
        "error_message": "Формат дати народження має бути (дд.мм.рррр) або інша помилка. Спобуй знову!!!",
        "final_error_message": "Спроби закінчилися при введенні дня народження.",
        "transform_func": lambda x: x.strip()
    },
    }

# Функції-обробники команд
def handle_add_email(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'add_email' command. Adds an email
    address to a contact in the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не вдалося ввести ім'я щоб додати пошту."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        if contact.email:
            return f"Адреса електронної пошти для {name} вже існує: {contact.email.value}"
        else:
            print('Додати електронну пошту:')
            new_email = validate_input(**validation_info["email"])
            if contact.add_email(new_email):
                return f"Адресу електронної пошти успішно додано. \n{address_book.get_all_records()}"
            else:
                return "Електронна пошта не валідна."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."

def handle_add_phone_number(arg: str, address_book: AddressBook) -> str:
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не вдалося ввести ім'я щоб додати телефон."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print('Додати телефон:')
        new_phone = validate_input(**validation_info["phone"])
        if new_phone not in [record.value for record in contact.phones]:
            if contact.add_phone_number(new_phone):
                return f"Номер телефону успішно додано. \n{address_book.get_all_records()}"
            else:
                return "Номер не валідний."
        else:
            return f"Номер {new_phone} не додано, бо він вже існує у контакта {name}!!!"
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."

def handle_add_record(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'add_record' command. Adds a new contact to the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None or name.lower().strip() in [record.name.value.lower().strip() for record in address_book.data.values()]:
        return f"Не вдалося додати контакт!!!"
    else:
        phone = validate_input(**validation_info["phone"])
        email = validate_input(**validation_info["email"])
        birthday = validate_input(**validation_info["birthday"])
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
        return "Дані не валідні."

def handle_change_email(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'change_email' command. Changes the email address of a contact.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не далося ввести ім'я щоб змінити електронну пошту."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print("Стара електронна пошта:")
        old_email = validate_input(**validation_info["email"])
        if not old_email:
            return f'Cтара електронна пошта не введена або не валідна'
        else:
            if old_email != contact.email.value:
                return f'Не вдалося змінити електронну пошту.' \
                       f'Такої електронної пошти {old_email} у контакта {name} немає. \n{address_book.get_all_records()}'
            else:
                 print("Нова електронна пошта:")
                 new_email = validate_input(**validation_info["email"])
                 if new_email:
                    contact.change_email(old_email, new_email)
                    return f"Адресу електронної пошти успішно змінено з {old_email} на {new_email}. \n{address_book.get_all_records()}"
                 else:
                    return f'Нова електронна пошта не введена або не валідна'
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."

def handle_change_phone_number(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'change_phone_number' command. Changes the phone number of a contact.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не вдалося ввести ім'я для зміни номера телефону контакту."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print("Старий номер телефону:")
        old_phone = validate_input(**validation_info["phone"])
        if old_phone in [record.value for record in contact.phones]:
            print("Новий номер телефону:")
            new_phone = validate_input(**validation_info["phone"])
            if new_phone:
                if new_phone not in [record.value for record in contact.phones]:
                    contact.change_phone_number(old_phone, new_phone)
                    return f"Номер телефону {old_phone} успішно змінено {new_phone}. \n{address_book.get_all_records()}"
                else:
                    return f'Не вдалося замінити телефон {old_phone} на новий {new_phone}. Ви ввели такий же телефон'
            else:
                return 'Не вдалося замінити телефон на новий. Новий номер телефону відсутній або не валідний'
        else:
            return 'Старий номер телефону відсутній у книзі або не валідний'
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."

def handle_days_to_birthday(arg: str, address_book: AddressBook) -> str:
    """
     Command handler for 'days_to_birthday' command. Calculates the
     days until the birthday of a contact
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не вдалося ввести ім'я для того щоб дізнатися дань народження контакту."
    else:
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
    """
    Command handler for 'exit' command. Exits the address book application.
    """
    return 'Goodbye!'

def handle_find_records(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'find_records' command. Searches for contacts
    in the address book based on user-specified criteria.
    """
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
        return "Невірний вибір опції. Пошук скасовано."
    results = address_book.find_records(**search_criteria)
    if results:
        return f"Результати пошуку: \n{address_book.get_all_records()}"
    else:
        return "Контакт за вказаними критеріями не знайдений."

def handle_get_all_records(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'get_all_records' command. Retrieves and
    returns all records in the address book.
    """
    return address_book.get_all_records()

def handle_get_birthdays_per_week(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'get_birthdays_per_week' command. Retrieves birthdays
    for the specified number of days ahead.
    """
    num_str = input("Введіть кількість днів: ")
    if num_str.isdigit():
        num = int(num_str)
        birthdays_list = address_book.get_birthdays_per_week(num)
        if birthdays_list:
            return "\n".join(birthdays_list)
        else:
            return "Немає іменинників."
    else:
        return "Ви ввели не число. Попробуйте знову запустити команду!!!"

def handle_load_from_file(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'load_from_file' command. Loads the address
    book data from a file.
    """
    arg = arg.strip()
    file_handler = AddressBookFileHandler(FILE_PATH)
    loaded_address_book = file_handler.load_from_file()
    if loaded_address_book:
        return f"Адресну книгу завантажено з файлу, який знаходиться за шляхом {FILE_PATH}"
    else:
        return "Не вдалося завантажити адресну книгу з файлу."

def handle_remove_email(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'remove_email' command. Removes an email
    address from a contact in the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не вдалося ввести ім'я для видалення пошти!!!"
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print('Для видалення')
        email_to_remove = validate_input(**validation_info["email"])
        if email_to_remove and email_to_remove != contact.email.value:
            return f"Електронна пошта {email_to_remove} відсутня у контакту {name}!!!\n{address_book.get_all_records()}"
        if contact.remove_email(email_to_remove):
            return f"Адресу електронної пошти {email_to_remove} успішно видалено. \n{address_book.get_all_records()}"
        else:
            return "Не вдалося видалити електронну пошту."
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."

def handle_remove_phone_number(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'remove_phone_number' command. Removes a phone
    number from a contact in the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не вдалося ввести ім'я для видалення телефону!!!"
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print('Для видалення')
        phone_to_remove = validate_input(**validation_info["phone"])
        if phone_to_remove and phone_to_remove not in [phone.value for phone in contact.phones]:
            return f"Номер телефону {phone_to_remove} відсутній у контакту {name}!!!\n{address_book.get_all_records()}"
        if contact.remove_phone_number(phone_to_remove):
            return f"Номер телефону {phone_to_remove} успішно видалено. \n{address_book.get_all_records()}"
        else:
            return "Не вдалося видалити номер телефону"
    else:
        return f"Контакт з ім'ям {name} не знайдений в адресній книзі."

def handle_remove_record(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'remove_record' command. Removes a contact from
    the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Не вдалося ввести ім'я для видалення контакту!!!"
    if address_book.remove_record(name):
        return f"Контакт {name} успішно видалено з адресної книги. \n{address_book.get_all_records()}"
    else:
        return f"Контакт {name} не знайдено в адресній книзі або ще не додано книги."

def handle_help(arg: str, address_book: AddressBook) -> str:
    """Outputs the command menu"""
    print_command_list()
    return ''

def handle_save_to_file(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'save_to_file' command. Saves the address
    book data to a file.
    """
    file_handler = AddressBookFileHandler(str(FILE_PATH))
    file_handler.save_to_file(address_book)
    return f"Адресну книгу збережено за шляхом {str(FILE_PATH)}"

def input_error(func):
    """
    A decorator wrapper for error handling.

    Args:
        func (callable): The function to wrap with error handling.

    Returns:
        callable: The wrapped function with error handling.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except IndexError as e:
            print(Fore.RED, 'Not enough data.', str(e))
        except ValueError as e:
            print(Fore.RED, 'Wrong value.', str(e))
        except KeyError as e:
            print(Fore.RED, 'Wrong key.', str(e)[1:-1])
        except TypeError as e:
            print(Fore.RED, 'Wrong type of value.', str(e))
        except FileNotFoundError as e:
            print(Fore.RED, e)
        except Exception as e:
            print(Fore.RED, e)
    return wrapper

@input_error
def main_cycle(address_book: AddressBook) -> bool:
    """
    Return True if it needs to stop the program. False otherwise.
    """
    completer = NestedCompleter.from_nested_dict({command[0]: None for command in COMMANDS.values()})
    user_input = prompt('>>> ', completer=completer, lexer=RainbowLexer()).strip().lower()
    func, argument = command_parser(user_input)
    result = func(argument, address_book)  # Передаємо адресну книгу як аргумент
    print(Fore.WHITE, result)
    return result.endswith('Goodbye!')

def prepare() -> None:
    """
    Prints initial information to the user
    :return: None
    """
    init_colorama()
    print(Fore.BLUE + Style.BRIGHT + ADDRESSBOOK_LOGO)
    print(Fore.CYAN + "Welcome to your ADDRESS BOOK!")
    print()
    print_command_list()

def main():
    """
    Main entry point for the address book program.
    This function initializes the address book, prepares
    the environment, and enters the main program loop.
    """
    address_book = AddressBook()
    handle_load_from_file('', address_book)
    prepare()

    while True:
        if main_cycle(address_book):
            break


if __name__ == '__main__':
    main()


