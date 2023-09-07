"""
Оля сюди скопіюй свої методи класів
Олег допишеш в ці класи свої методи
По можливості додавайте typehints для методів класу і докстрінги (якщо не знаєте що це
то скидайте як є і потім якось доробимо)
"""
from typing import List


FILE_NAME = ''  # for saving data


class Note:
    """Class representing the note"""
    #__init__(self, title: str, content: str) -> None
    #__str__(self) -> str
    pass


 
class NoteManager:
    def __init__(self):
        self.notes = []

    def add_note(self, title: str, content: str) -> None:
        """
        Додає нотатку з вказаним заголовком та вмістом.

        :param title: Заголовок нотатки.
        :param content: Вміст нотатки.
        :return: None
        """

    def save_notes_to_json(self, filename: str) -> None:
        """
        Зберігає нотатки у JSON-файл з вказаним ім'ям.

        :param filename: Ім'я файлу для збереження нотаток.
        :return: None
        """

    def load_notes_from_json(self, filename: str) -> None:
        """
        Завантажує нотатки з JSON-файлу з вказаним ім'ям.

        :param filename: Ім'я файлу для завантаження нотаток.
        :return: None
        """

    def search_notes(self, keyword: str) -> List[Note]:
        """
        Виконує пошук нотаток, що містять ключове слово.

        :param keyword: Ключове слово для пошуку.
        :return: Список нотаток, які відповідають критеріям пошуку.
        """
    
    def command_parser(user_input: str) -> tuple[callable, str]:
        """
        Вибирає і повертає відповідний обробник та аргумент цього обробника
        з user_input відповідно до COMMANDS
        :param user_input: Рядок, який повинен починатися з команди, за якою може слідувати ім'я та номер телефону, якщо потрібно
        :return: Кортеж функції та аргумента рядка
        """