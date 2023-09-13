from .classes_ab import AddressBook, Record, AddressBookFileHandler, Phone, Email, Birthday, Name
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
    'add an email': ['add_email'],
    'add a phone number': ['add_phone'],
    'add contact to AdressBook ': ['add'],
    'change an email ': ['change_email'],
    'change phone number': ['change_phone'],
    'return days until birthday': ['when_birthday'],
    'exit from AdressBook ': ['exit'],
    'find contact in AdressBook': ['find'],
    'display all contacts': ['all'],
    'return list of birthdays': ['get_list'],
    'load information about contacts from file': ['load'],
    'remove an email': ['remove_email'],
    'remove phone number': ['remove_phone'],
    'remove contact from AdressBook': ['remove'],
    'save information about contacts to file': ['save'],
    'display help': ['help']
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
    print(Fore.GREEN, "Available commands:")
    separator = '|----------------------|--------------------------------------------|'
    print(separator, f'\n|  Commands            |  Description {" ":30}|\n', separator, sep='')
    for description, commands in COMMAND_DESCRIPTIONS.items():
        print(f"| {Fore.WHITE} {', '.join(commands):<20}{Fore.GREEN}| {description:<43}|")
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
        "prompt": "Enter a contact name: ",
        "validator": lambda x: Name(x).validate(x),
        "error_message": "Invalid name. Please use only letters and more than one. Try again!!!",
        "final_error_message": "Attempts ended when entering a name.",
        "transform_func": lambda x: x.lower().strip()

    },
    "phone": {
        "prompt": "Enter the phone number (+380________): ",
        "validator": lambda x: not x or Phone(x).validate(x),
        "error_message": "The phone does not match the format (+380________). Try again!!!",
        "final_error_message": "The attempts ended when the phone was entered.",
        "transform_func": lambda x: x.strip()
    },
    "email": {
        "prompt": "Enter an email in an acceptable format: ",
        "validator": lambda x: not x or Email(x).validate(x),
        "error_message": "The mail format is not acceptable. Try again!!!",
        "final_error_message": "Attempts ended when email was entered.",
        "transform_func": lambda x: x.strip()
    },
    "birthday": {
        "prompt": "Enter the contact's birthday in the format (dd.mm.yyyy): ",
        "validator": lambda x: not x or Birthday(x).validate(x),
        "error_message": "Date of birth format should be (dd.mm.yyyy) or another error. Try again!!!",
        "final_error_message": "Attempts ended when birthday was entered.",
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
        return "Failed to enter name to add mail."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        if contact.email:
            return f"An email address for {name} already exists: {contact.email.value}"
        else:
            print('Add email:')
            new_email = validate_input(**validation_info["email"])
            if contact.add_email(new_email):
                return f"Email added successfully. \n{address_book.get_all_records()}"
            else:
                return "Email is not valid."
    else:
        return f"The contact with the name {name} was not found in the address book."


def handle_add_phone_number(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'add_phone' command. Adds phone
    to a contact in the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Failed to enter name to add phone."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print('Add phone:')
        new_phone = validate_input(**validation_info["phone"])
        if new_phone not in [record.value for record in contact.phones]:
            if contact.add_phone_number(new_phone):
                return f"Phone number successfully added. \n{address_book.get_all_records()}"
            else:
                return "The phone number is not valid."
        else:
            return f"The number {new_phone} has not been added because it already exists in the contact {name}!!!"
    else:
        return f"The contact with the name {name} was not found in the address book."


def handle_add_record(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'add' command. Adds a new contact to the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return f"Failed to add contact!!!"
    if name.lower().strip() in [record.name.value.lower().strip() for record in address_book.data.values()]:
        return f"A contact with that name already exists!!!"
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
        return f"The contact has been successfully added to the address book. \n{address_book.get_all_records()}"
    else:
        return "The data is not valid."


def handle_change_email(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'change_email' command. Changes the email address of a contact.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Failed to enter name to change email."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print("The old email:")
        old_email = validate_input(**validation_info["email"])
        if not old_email:
            return f'The old email address was not entered or is not valid'
        else:
            if old_email != contact.email.value:
                return f'Unable to change the email address.' \
                       f'There is no email address {old_email} in the contact {name}.\n{address_book.get_all_records()}'
            else:
                 print("The new email:")
                 new_email = validate_input(**validation_info["email"])
                 if new_email:
                    contact.change_email(old_email, new_email)
                    return f"The email has been successfully changed from {old_email} to {new_email}.\n{address_book.get_all_records()}"
                 else:
                    return f'New email is not entered or is not valid'
    else:
        return f"The contact with the name {name} was not found in the address book."


def handle_change_phone_number(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'change_phone' command. Changes the phone number of a contact.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "You failed to enter a name to change the contact's phone number."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print("The old phone number:")
        old_phone = validate_input(**validation_info["phone"])
        if old_phone in [record.value for record in contact.phones]:
            print("The new phone number:")
            new_phone = validate_input(**validation_info["phone"])
            if new_phone:
                if new_phone not in [record.value for record in contact.phones]:
                    contact.change_phone_number(old_phone, new_phone)
                    return f"The phone number {old_phone} has been successfully updated to {new_phone}.\n{address_book.get_all_records()}"
                else:
                    return f'Failed to replace the phone {old_phone} with the new one {new_phone}. You entered the same phone number.'
            else:
                return 'Failed to replace the phone number with a new one. The new phone number is missing or not valid'
        else:
            return 'The old phone number is not found in the address book or is not valid.'
    else:
        return f"The contact with the name {name} was not found in the address book."


def handle_days_to_birthday(arg: str, address_book: AddressBook) -> str:
    """
     Command handler for 'when_birthday' command. Calculates the
     days until the birthday of a contact
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "You failed to enter a name to find out the contact's birthday."
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        if contact.birthday:
            days = contact.days_to_birthday()
            return f"Name {name} has {days} days left until their birthday."
        else:
            return f"The contact {name} does not have a birth date specified."
    else:
        return f"Contact with the name {name} was not found in the address book."


def handle_exit(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'exit' command. Exits the address book application.
    """
    return handle_save_to_file(arg, address_book) + '\nGoodbye!'


def handle_find_records(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'find' command. Searches for contacts
    in the address book based on user-specified criteria.
    """
    search_criteria = {}
    print("What criteria would you like to search by?\n1. Search by name\n2. Search by phone number.")
    search_option = input("Select an option (1 or 2): ")
    if search_option == "1":
        search_name = input("Enter a name to search for (minimum 2 characters): ").strip().lower()
        if len(search_name) >= 2:
            search_criteria['name'] = search_name
        else:
            return "You entered too few characters for the name. Name search canceled."
    elif search_option == "2":
        search_phones = input("Please enter a part of the phone number for the search (minimum 5 characters): ").strip()
        if len(search_phones) >= 5:
            search_criteria['phones'] = search_phones
        else:
            return "You entered too few characters for a phone number. Phone number search canceled."
    else:
        return "Invalid option selected. Search canceled."
    results = address_book.find_records(**search_criteria)
    if results:
        return f"Search results: \n{address_book.get_all_records()}"
    else:
        return "The contact meeting the specified criteria was not found."


def handle_get_all_records(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'all' command. Retrieves and
    returns all records in the address book.
    """
    return address_book.get_all_records()


def handle_get_birthdays_per_week(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'get_list' command. Retrieves birthdays
    for the specified number of days ahead.
    """
    num_str = input("Enter the number of days: ")
    if num_str.isdigit():
        num = int(num_str)
        birthdays_list = address_book.get_birthdays_per_week(num)
        if birthdays_list:
            return "\n".join(birthdays_list)
        else:
            return "No birthdays today."
    else:
        return "You entered a non-number. Please try running the command again!!!"


def handle_load_from_file(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'load_from_file' command. Loads the address
    book data from a file.
    """
    arg = arg.strip()
    if arg and (not Path(arg).exists() or not Path(arg).is_file()):
        return f"Шлях до файлу не існує"
    arg = arg if arg else str(FILE_PATH)
    file_handler = AddressBookFileHandler(arg)
    loaded_address_book = file_handler.load_from_file()
    address_book.data.update(loaded_address_book.data)
    return f"Адресну книгу завантажено з файлу {arg}"


def handle_remove_email(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'remove_email' command. Removes an email
    address from a contact in the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Failed to enter a name for email removal!!!"
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print('To delete')
        email_to_remove = validate_input(**validation_info["email"])
        if email_to_remove and email_to_remove != contact.email.value:
            return f"The email {email_to_remove} is not present in the contact {name}!!!\n{address_book.get_all_records()}"
        if contact.remove_email(email_to_remove):
            return f"The email {email_to_remove} has been successfully deleted. \n{address_book.get_all_records()}"
        else:
            return "Failed to delete the email."
    else:
        return f"The contact with the name {name} was not found in the address book."


def handle_remove_phone_number(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'remove_phone' command. Removes a phone
    number from a contact in the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Failed to enter a name for phone number deletion!!!"
    else:
        contact = address_book.get_record_by_name(name)
    if contact is not None:
        print('To delete')
        phone_to_remove = validate_input(**validation_info["phone"])
        if phone_to_remove and phone_to_remove not in [phone.value for phone in contact.phones]:
            return f"The phone number {phone_to_remove} is not found in the contact {name}!!!\n{address_book.get_all_records()}"
        if contact.remove_phone_number(phone_to_remove):
            return f"The phone number {phone_to_remove} has been successfully deleted.\n{address_book.get_all_records()}"
        else:
            return "Failed to delete the phone number."
    else:
        return f"The contact {name} was not found in the address book or the address book has not been created yet."


def handle_remove_record(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'remove' command. Removes a contact from
    the address book.
    """
    name = validate_input(**validation_info["name"])
    if name is None:
        return "Could not enter name to delete contact!!!"
    if address_book.remove_record(name):
        return f"Contact {name} has been successfully removed from the address book. \n{address_book.get_all_records()}"
    else:
        return f"The contact {name} is not found in the address book or the book has not yet been added."


def handle_help(arg: str, address_book: AddressBook) -> str:
    """Outputs the command menu"""
    print_command_list()
    return ''


def handle_save_to_file(arg: str, address_book: AddressBook) -> str:
    """
    Command handler for 'save' command. Saves the address
    book data to a file.
    """
    FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_handler = AddressBookFileHandler(str(FILE_PATH))
    file_handler.save_to_file(address_book)
    return f"The address book has been saved at the following path {str(FILE_PATH)}"


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
    result = func(argument, address_book)
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
    print(handle_load_from_file('', address_book))
    prepare()

    while True:
        if main_cycle(address_book):
            break


if __name__ == '__main__':
    main()
