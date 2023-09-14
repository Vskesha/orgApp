from .classes_nb import NoteManager
from colorama import init as init_colorama, Fore, Back, Style
from functools import wraps
from pathlib import Path
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import prompt
from faker import Faker


FILE_PATH = Path.home() / "orgApp" / "notes.json"  # for working on different filesystems
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
    lower_input_end_spaced = user_input.lower() + " "
    for command in COMMANDS:
        if lower_input_end_spaced.startswith(command + " "):
            func = COMMANDS[command]
            data = user_input[len(command) + 1:].strip()

    if not func:
        raise ValueError(f"There is no such command {user_input.split()[0]}")

    return func, data


def handle_add_note(args: str) -> str:
    """adds note to your NoteBook"""
    title = input("Enter note title: ")
    if not title.strip():
        raise ValueError('Title cannot be empty')
    if title in NOTE_MANAGER.get_titles():
        raise ValueError(f'Note with title "{title}" already exist')
    content = input("Enter note text: ")
    tags = input("Enter note tags: ")
    NOTE_MANAGER.add_note(title, content, set(tags.split()))
    return "Note added successfully."


def handle_add_tags(agrs: str) -> str:
    """add tag to note"""
    title = input("Enter note title: ")
    if title not in NOTE_MANAGER.get_titles():
        raise KeyError(f'Note with title "{title}" not found')
    tags = input("Enter tag: ").split()
    result = False
    for tag in tags:
        result = NOTE_MANAGER.add_tag_to_note(title, tag)
    return "Tags added successfully."
    

def handle_delete_note(args: str) -> str:
    """deletes note from NoteBook"""
    title = input("Enter note title: ")
    if title not in NOTE_MANAGER.get_titles():
        raise KeyError(f'Note with title "{title}" not found')
    NOTE_MANAGER.delete_note(title)
    return "Note deleted successfully."


def handle_delete_tag_from_note(args: str) -> str:
    """deletes tag from note in NoteBook"""
    title = input("Enter note title: ")
    if title not in NOTE_MANAGER.get_titles():
        raise KeyError(f'Note with title "{title}" not found')
    tag = input("Enter tag: ")
    NOTE_MANAGER.delete_tag_from_note(title, tag)
    return "Tag deleted successfully."


def handle_edit_note(args: str) -> str:
    """edit a note content in the NoteBook"""
    title = input("Enter note title: ")
    if title not in NOTE_MANAGER.get_titles():
        raise KeyError(f'Note with title "{title}" not found')
    content = input("Enter new note text: ")
    NOTE_MANAGER.edit_note(title, content)
    return "Note edited successfully."


def handle_exit(args: str) -> str:
    """exits the program"""
    return handle_save_notes("") + "\nGoodbye!"


def handle_fill_with_random_notes(args: str) -> str:
    """adds fdke data to the notebook"""
    count_notes = int(input("Enter the number of notes: "))
    faker = Faker()
    for i in range(count_notes):
        NOTE_MANAGER.add_note(title=faker.name(), content=faker.sentence(nb_words=15), tags=set(faker.words(2 + i % 2)))
    return "Random notes added successfully."     


def handle_help(args: str) -> str:
    """outputs this list of commands"""
    print_menu()
    return ''


def handle_load_notes(args: str) -> str:
    """loads notes from the given file"""
    filename = args if args else input("Enter the filename to load: ")
    new_notes = NoteManager.load_notes_from_json(filename)
    NOTE_MANAGER.add_notes(new_notes)
    return f"Notes loaded from {filename}"


def handle_save_notes(args: str) -> str:
    """saves notes to file"""
    FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_MANAGER.save_notes_to_json(str(FILE_PATH))
    return f"Notes saved to {str(FILE_PATH)}"


def handle_find_by_tag(args: str) -> str:
    """returns notes with given tags"""
    tag = args.split()[0] if args else input("Enter a tag to search: ")
    search_results = NOTE_MANAGER.search_by_tag(tag)
    if search_results:
        result_str = "Search results:\n\n"
        result_str += NoteManager.string_from_list(search_results)
        return result_str
    else:
        return "No notes found for this tag." 
    

def handle_search_notes(args: str) -> str:
    """returns notes with given keyword"""
    keyword = args[0] if args else input("Enter a keyword to search: ")
    search_results = NOTE_MANAGER.search_notes(keyword)
    if search_results:
        result_str = "Search results:\n\n"
        result_str += NoteManager.string_from_list(search_results)
        return result_str
    else:
        return "No notes found for this keyword."


def handle_view_all_notes(args: str) -> str:
    """displays all notes."""
    all_notes = NOTE_MANAGER.get_all_notes()
    if all_notes:
        result_str = "All notes:\n\n"
        result_str += NoteManager.string_from_list(all_notes)
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
        except Exception as e:
            print(Fore.RED, e)
    return wrapper


@input_error
def main_cycle() -> bool:
    """
    return True if it needs to stop program. False otherwise.
    """
    completer = NestedCompleter.from_nested_dict({command: None for command in COMMANDS.keys()})
    user_input = prompt('>>> ', completer=completer, lexer=RainbowLexer())
    func, argument = command_parser(user_input)
    result = func(argument)
    print(Fore.WHITE, result)
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
    print(Fore.BLUE + Style.BRIGHT + NOTEBOOK_LOGO)
    print(Fore.CYAN + "Welcome to your note-taking app!")
    print()
    print_menu()  # Display the menu with commands


def print_menu():
    print(Fore.GREEN, "Available commands:")
    separator = '|--------------------------------|-----------------------------------------|'
    print(separator, f'\n|           Commands             |     Action{" ":30}|\n', separator, sep='')
    for func, commands in COMMANDS_LISTS.items():  # generic way when we add new action
        print(f"| {Fore.WHITE} {', '.join(commands):<30}{Fore.GREEN}| {func.__doc__:<40}|")
    print(separator, '\n')


# Map of commands and their corresponding handler functions
COMMANDS_LISTS = {
    handle_add_note: ["add", 'plus'],
    handle_add_tags: ["add_tags"],
    handle_fill_with_random_notes: ["add_fake_notes"],
    handle_view_all_notes: ['all', 'all_notes', 'view'],
    handle_edit_note: ['edit'],
    handle_exit: ["bye", 'close', 'exit', 'goodbye'],
    handle_delete_note: ["delete"],
    handle_delete_tag_from_note: ["delete_tag"],
    handle_find_by_tag: ['tag', "find_tag", 'search_tag'],
    handle_help: ['help'],
    handle_load_notes: ["load"],
    handle_save_notes: ['save'],
    handle_search_notes: ['find', 'search'],
}
COMMANDS = {command: func for func, commands in COMMANDS_LISTS.items() for command in commands}


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


if __name__ == "__main__":
    main()
