from .classes_nb import NoteManager
from colorama import init as init_colorama, Fore, Back, Style
from functools import wraps
from pathlib import Path


FILE_PATH = Path.home() / 'orgApp' / 'notes.json'  # for working on different filesystems
FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
NOTE_MANAGER = NoteManager.load_notes_from_json(str(FILE_PATH))  # Create an object to manage notes from file
NOTEBOOK_LOGO = """
                          .                     
                        .o8                     
ooo. .oo.    .ooooo.  .o888oo  .ooooo.   
`888P"Y88b  d88' `88b   888   d88' `88b   
 888   888  888   888   888   888ooo888    
 888   888  888   888   888 . 888    .o  
o888o o888o `Y8bod8P'   "888" `Y8bod8P'  
 .o8                           oooo
"888                           `888
 888oooo.   .ooooo.   .ooooo.   888  oooo
 d88' `88b d88' `88b d88' `88b  888 .8P'
 888   888 888   888 888   888  888888.
 888   888 888   888 888   888  888 `88b.
 `Y8bod8P' `Y8bod8P' `Y8bod8P' o888o o888o
"""


def command_parser(user_input: str) -> tuple[callable, str]:
    """
    fetches and returns proper handler and argument of this handler
    from user_input accordingly to the COMMANDS
    :param user_input: str which must start with command followed by name and phone number if needed
    :return: tuple of function and str argument
    """
    if not user_input:
        raise IndexError("Nothing was entered ...")

    func, data = None, []
    lower_input_end_spaced = user_input.lower() + ' '
    for command in COMMANDS:
        if lower_input_end_spaced.startswith(command + ' '):
            func = COMMANDS[command]
            data = user_input[len(command) + 1:].strip()

    if not func:
        raise ValueError(f"There is no such command {user_input.split()[0]}")

    return func, data


def handle_add_note(args: str):
    """adds note to your NoteBook"""
    title = input("Enter note title: ")
    content = input("Enter note text: ")
    NOTE_MANAGER.add_note(title, content)
    return "Note added successfully."


def handle_exit(args: str):
    """exits the program"""
    return handle_save_notes('') + '\nGoodbye!'


def handle_load_notes(args: str):
    """loads notes from the given file"""
    filename = args if args else input("Enter the filename to load: ")
    new_notes = NoteManager.load_notes_from_json(filename)
    NOTE_MANAGER.add_notes(new_notes)
    return f"Notes loaded from {filename}"


def handle_save_notes(args: str):
    """saves notes to file"""
    NOTE_MANAGER.save_notes_to_json(str(FILE_PATH))
    return f"Notes saved to {str(FILE_PATH)}"


def handle_search_notes(args: str):
    """returns notes with given keyword"""
    keyword = args[0] if args else input("Enter a keyword to search: ")
    search_results = NOTE_MANAGER.search_notes(keyword)
    if search_results:
        result_str = "Search results:\n"
        for idx, result in enumerate(search_results, 1):
            result_str += f"{idx}. Title: {result.title}\n"
            result_str += f"   Text: {result.content}\n"
        return result_str
    else:
        return "No notes found for this keyword."


def handle_view_all_notes(args: str):
    """displays all notes."""
    all_notes = NOTE_MANAGER.get_all_notes()
    if all_notes:
        result_str = "All notes:\n"
        for idx, note in enumerate(all_notes, 1):
            result_str += f"{idx}. Title: {note.title}\n   Text: {note.content}\n"
        return result_str
    else:
        return " There are no notes."


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
    return wrapper


@input_error
def main_cycle() -> bool:
    """
    return True if it needs to stop program. False otherwise.
    """
    user_input = input(Fore.WHITE + '>>> ')
    func, argument = command_parser(user_input)
    result = func(argument)
    print(Fore.BLUE, result)
    return result.endswith('Goodbye!')


def main():
    prepare()
    while True:
        if main_cycle():
            break


def prepare() -> None:
    """
    Displays initial information to the user
    :return: None
    """
    init_colorama()
    print(Fore.BLUE + Back.BLACK + Style.BRIGHT + NOTEBOOK_LOGO)
    print("Welcome to your note-taking app!")
    print()
    print_menu()  # Display the menu with commands


def print_menu():
    print(Fore.GREEN, "Available commands:")
    for command, func in COMMANDS.items():
        print(f"-{Fore.WHITE} {command: <8} {Fore.GREEN + func.__doc__}")


# Map of commands and their corresponding handler functions
COMMANDS = {
    'add': handle_add_note,
    'plus': handle_add_note,
    'save': handle_save_notes,
    'load': handle_load_notes,
    'all': handle_view_all_notes,
    'search': handle_search_notes,
    'find': handle_search_notes,
    'exit': handle_exit,
    'close': handle_exit,
    'bye': handle_exit,
    'goodbye': handle_exit,
}


if __name__ == '__main__':
    main()
