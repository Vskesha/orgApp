"""
Також файл для Андрія
Якщо можеш, то перероби мейн не через іфи а через виклик окремих функцій,
які є ключами для команд (Приблизно кожен if є окремою функцією handle_XXX()
додай відповідні команди до COMMANDS і реалізуй відповідні handler
Хендлер приймає строку (все, що введено в консолі після назви команди) і повертає строку
"""
from functools import wraps


# зразок хендлера
# def handle_add_number(user_input: str) -> str:
#     """
#     adds name and phone number from given 'user_input' to PHONEBOOK.
#     :returns: str with the result of adding.
#     :raises: errors if given 'user_input' has no relevant arguments
#     """

def handle_exit():
    """
    Makes actions for closing the program (saving data, etc)
    :return: str with 'Goodbye'
    """
    return 'Goodbye!'


COMMANDS = {
    'goodbye': handle_exit,
    'close': handle_exit,
    'exit': handle_exit,
    'bye': handle_exit,
    # 'add_note': add_note_handler
    # де ключі це команди з консолі, а значення це функції хендлери
    #
}


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


@input_error
def main_cycle() -> bool:
    """
    return True if it needs to stop program. False otherwise.
    """
    user_input = input('>>> ')
    func, argument = command_parser(user_input)
    result = func(argument)
    print(result)
    return result.endswith('Goodbye!')


def prepare() -> None:
    """
    Prints initial information to user
    :return: None
    """
    pass


def main():
    prepare()
    while True:
        if main_cycle():
            break


if __name__ == '__main__':
    main()
