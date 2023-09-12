import sys
sys.path.extend(['sorter', 'note_book', 'address_book', 'tictactoe',
                 'bandergoose'])
from address_book import main as address_main
# from bandergoose import main as bandergoose_main
from colorama import init as init_colorama, Fore, Back, Style
from note_book import main as note_main
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from sorter import clean_folder
from snake import main as snake_main
from tictactoe import main as tictactoe_main


COMMAND_COLOR = Fore.WHITE
TEXT_COLOR = Fore.BLUE
ERROR_COLOR = Fore.RED
ORGAPP_LOGO = """
                                    .o.                             
                                   .888.                            
 .ooooo.  oooo d8b  .oooooooo     .8"888.     oo.ooooo.  oo.ooooo.  
d88' `88b `888""8P 888' `88b     .8' `888.     888' `88b  888' `88b 
888   888  888     888   888    .88ooo8888.    888   888  888   888 
888   888  888     `88bod8P'   .8'     `888.   888   888  888   888 
`Y8bod8P' d888b    `8oooooo.  o88o     o8888o  888bod8P'  888bod8P' 
================== d"     YD ================= 888 ====== 888 ===== 
                   "Y88888P'                  o888o      o888o      
"""


def close_program():
    print(f'{Fore.GREEN}Goodbye!')


COMMANDS = {
    'ab': address_main,
    'addressbook': address_main,
    # 'bandergoose': bandergoose_main,
    'exit': close_program,
    'note': note_main,
    'notebook': note_main,
    'quit': close_program,
    'sorter': clean_folder,
    'snake': snake_main,
    'tictactoe': tictactoe_main,
}


def get_command() -> str:
    """Gets and returns str command from user"""
    completer = NestedCompleter.from_nested_dict({command: None for command in COMMANDS.keys()}) 
    while True:
        command = prompt('>>>', completer=completer, lexer=RainbowLexer()).strip().lower()
        if command in COMMANDS:
            return command
        else:
            print(f'{ERROR_COLOR}There is no such command: {COMMAND_COLOR + command}\n'
                  f'{TEXT_COLOR}Try again:{COMMAND_COLOR}')


def main():
    """
    This is start point of our orgApp
    """
    init_colorama()
    print_menu()
    subprogram = COMMANDS[get_command()]
    subprogram()


def print_menu():
    """
    Prints initial menu of the program
    """
    print(Fore.GREEN+ Style.BRIGHT + ORGAPP_LOGO)
    print(f'{Fore.CYAN}{"":>35}YOUR FAVORITE ORGANIZER PROGRAM\n')
    print(Style.BRIGHT)
    print(TEXT_COLOR + 'With this app You can deal with your notes and contacts')
    print(f'Use {COMMAND_COLOR}note {TEXT_COLOR}or {COMMAND_COLOR}notebook '
          f'{TEXT_COLOR}command to open your notebook manager.')
    print(f'Type {COMMAND_COLOR}ab {TEXT_COLOR}or {COMMAND_COLOR}addressbook '
          f'{TEXT_COLOR}below to manage your contacts.')
    print(f'Also You are able to sort your files with {COMMAND_COLOR}sorter.')
    print(f'{TEXT_COLOR}And if you are tired you can play simple games:')
    print(f'{COMMAND_COLOR}tictactoe, bandergoose, hannoitower '
          f'{TEXT_COLOR}or {COMMAND_COLOR}snake.')
    print(f'exit, quit {TEXT_COLOR}to close the program')


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


if __name__ == '__main__':
    main()
