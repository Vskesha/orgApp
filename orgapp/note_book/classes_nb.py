"""
Оля сюди скопіюй свої методи класів
Олег допишеш в ці класи свої методи
По можливості додавайте typehints для методів класу і докстрінги (якщо не знаєте що це
то скидайте як є і потім якось доробимо)
"""
 


FILE_NAME = ''  # for saving data

import json
from functools import wraps

class Note:
    """Represents a note with a title and content."""

    def __init__(self, title, content):
        """
        Initializes a new Note.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
        """
        self.title = title
        self.content = content

class NoteManager:
    """Manages a collection of notes."""

    def __init__(self):
        """Initializes a new NoteManager with an empty list of notes."""
        self.notes = []

    def add_note(self, title, content):
        """
        Adds a new note to the collection.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
        """
        note = Note(title, content)
        self.notes.append(note)

    def save_notes_to_json(self, filename):
        """
        Saves the notes to a JSON file.

        Args:
            filename (str): The name of the JSON file to save the notes to.
        """
        data = []
        for note in self.notes:
            data.append({
                "title": note.title,
                "content": note.content
            })

        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

    def load_notes_from_json(self, filename):
        """
        Loads notes from a JSON file and replaces the current collection.

        Args:
            filename (str): The name of the JSON file to load notes from.
        """
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                data = json.load(file)
                self.notes = []
                for note_data in data:
                    self.add_note(note_data["title"], note_data["content"])
        except FileNotFoundError:
            pass

    def search_notes(self, keyword):
        """
        Searches for notes containing a specific keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of notes containing the keyword in their title or content.
        """
        results = []
        for note in self.notes:
            if keyword in note.title or keyword in note.content:
                results.append(note)
        return results

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
            print('Not enough data.', str(e))
        except ValueError as e:
            print('Wrong value.', str(e))
        except KeyError as e:
            print('Wrong key.', str(e)[1:-1])
        except TypeError as e:
            print('Wrong type of value.', str(e))
    return wrapper