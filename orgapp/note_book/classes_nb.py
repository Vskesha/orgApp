import json


class Note:
    """Represents a note with a title and content."""

    def __init__(self, title: str, content: str, tags: list = None):
        """
        Initializes a new Note.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
            tags (list):  The tags of the note.
        """
        self.title = title
        self.content = content
        self.tags = tags if tags else []


class NoteManager:
    """Manages a collection of notes."""

    def __init__(self):
        """Initializes a new NoteManager with an empty list of notes."""
        self.notes = []

    def add_note(self, title: str, content: str, tags: list = None) -> None:
        """
        Adds a new note to the collection.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
            tags(list[str]): list with tag words
        """
        note = Note(title, content, tags)
        self.notes.append(note)

    def add_notes(self, other) -> None:
        """
        Extends self.notes with notes from other NoteManager object
        """
        self.notes.extend(other.notes)

    def add_tag_to_note(self, title: str, tag: str) -> bool:
        """
        Adds the tag to the note found by title.

        Args:
            title (str): The title of the note.
            tag (str): The tag of the note.
        """        
        
        for note in self.notes:
            if note.title == title:
                note.tags.append(tag)
                return True
        return False

    def delete_note(self, title: str) -> bool:
        """
        Deletes the note found by title.

        Args:
            title (str): The title of the note.
        """

        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                return True
        return False

    def edit_note(self, title: str, content: str) -> bool:
        """
        Edits the note found by title.

        Args:
            title (str): The title of the note.
            content (str): New content.
        """

        for note in self.notes:
            if note.title == title:
                note.content = content
                return True
        return False

    @classmethod
    def load_notes_from_json(cls, filename: str):
        """
        Loads notes from a JSON file and replaces the current collection.
        returns NoteManager object
        Args:
            filename (str): The name of the JSON file to load notes from.
        """
        new_note_book = NoteManager()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                for note_data in data:
                    new_note_book.add_note(note_data["title"], note_data["content"], note_data["tags"])
        except (FileNotFoundError, KeyError):
            pass

        return new_note_book

    def get_all_notes(self) -> list[Note]:
        """ Returns a list of all notes."""
        return self.notes

    def save_notes_to_json(self, filename: str) -> None:
        """
        Saves the notes to a JSON file.

        Args:
            filename (str): The name of the JSON file to save the notes to.
        """
        data = []
        for note in self.notes:
            data.append({"title": note.title, "content": note.content, "tags": note.tags})

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def search_by_tag(self, tag: str) -> list[Note]:
        """
        Searches for notes by tag.

        Args:
            tag (str): The tag to search for.

        Returns:
            list: A list of notes having the tag.
        """
        results = []
        for note in self.notes:
            if tag in note.tags:
                results.append(note)
        return results    
    
    def search_notes(self, keyword: str) -> list[Note]:
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

    def string_from_list(self, nodes: list[Note]) -> str:
        """makes multiline string from given list of Notes"""
        pass