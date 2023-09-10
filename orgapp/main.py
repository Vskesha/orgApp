import sys
sys.path.extend(['sorter', 'note_book', 'address_book'])
from colorama import init as init_colorama, Fore, Back, Style
from sorter import clean_folder
from note_book import main as note_main


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


def get_command() -> str:
    """Gets and returns str command from user"""
    while True:
        command = input('>>>').strip()
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
    print(Fore.GREEN + Back.BLACK + Style.BRIGHT + ORGAPP_LOGO)
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


COMMANDS = {
    'note': note_main,
    'notebook': note_main,
    'sorter': clean_folder,
    'exit': close_program,
    'quit': close_program,
}


if __name__ == '__main__':
    main()
