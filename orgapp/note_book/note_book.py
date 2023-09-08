"""
Також файл для Олі і Олега
Оля перероби не через іфи а через виклик окремих функцій-хендлерів,
які є ключами для команд (Приблизно кожен if є окремою функцією handle_XXX()
додайте відповідні команди до COMMANDS і реалізуйте відповідні handler
Хендлер приймає строку (все, що введено в консолі після назви команди) і повертає строку
"""

from functools import wraps 
from classes_nb import NoteManager  # Імпорт класу NoteManager з іншого файлу
from classes_nb import Note

def add_note_handler(note_manager, argument):
    title = input("Enter note title: ")
    content = input("Enter note text: ")
    note_manager.add_note(title, content)
    return "Note added successfully."

def save_notes_handler(note_manager, args):
    filename = args[0] if args else input("Enter the filename to save: ")
    note_manager.save_notes_to_json(filename)
    return f"Notes saved to {filename}"

def load_notes_handler(note_manager, args):
    filename = args[0] if args else input("Enter the filename to load: ")
    note_manager.load_notes_from_json(filename)
    return f"Notes loaded from {filename}"

def search_notes_handler(note_manager, args):
    keyword = args[0] if args else input("Enter a keyword to search: ")
    search_results = note_manager.search_notes(keyword)
    if search_results:
        result_str = "Search results:\n"
        for idx, result in enumerate(search_results, 1):
            result_str += f"{idx}. Title: {result.title}\n"
            result_str += f"   Text: {result.content}\n"
        return result_str
    else:
        return "No notes found for this keyword."

def exit_handler(note_manager, args):
    filename = args[0] if args else input("Enter the filename to save: ")
    note_manager.save_notes_to_json(filename)
    return 'Goodbye!'

# Map of commands and their corresponding handler functions
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

# Input error handler
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

# Command parser to get the appropriate handler and argument
def command_parser(user_input: str) -> tuple[callable, str]:
    """
    Selects and returns the appropriate handler and its argument
    from user_input according to COMMANDS
    :param user_input: The string that should start with a command, followed by a name and phone number if needed
    :return: Tuple of function and string argument
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
        return None, data  # Return None to handle "Command does not exist"

    return func, data

def print_menu():
    print("Available commands:")
    for command in COMMANDS:
        print(f"- {command}")

def prepare() -> None:
    """
    Displays initial information to the user
    :return: None
    """
    print("Welcome to your note-taking app!")
    print_menu()  # Display the menu with commands

# Main program function
def main_cycle(note_manager, filename) -> bool:
    """
    Returns True if the program should exit. False otherwise.
    """
    user_input = input('>>> ')
    func, argument = command_parser(user_input)
    if func is None:
        print("Command does not exist")
        return False
    result = func(note_manager, argument)
    print(result)
    return result.endswith('Goodbye!')

# Initial initialization
if __name__ == '__main__':
    filename = "my_notes.json"  # Filename for saving notes
    note_manager = NoteManager()  # Create an object to manage notes
    note_manager.load_notes_from_json(filename)  # Load notes from file
    prepare()  # Display initial information to the user
    while True:
        if main_cycle(note_manager, filename):
            break