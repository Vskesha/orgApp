import json


class Note:
    """Represents a note with a title and content."""

    def __init__(self, title: str, content: str, tags: set = None):
        """
        Initializes a new Note.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
            tags (list):  The tags of the note.
        """
        self.__title = None
        self.__content = None
        self.__tags = None
        self.title = title
        self.content = content
        self.tags = tags
    
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        if new_title.strip():   
            self.__title = new_title
        else:
            raise ValueError("Title cannot be empty.")

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, new_content):
        if new_content.strip():   
            self.__content = new_content
        else:
            raise ValueError("Content cannot be empty.")

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, new_tags):
        self.__tags = new_tags if len(new_tags) else set()


class NoteManager:
    """Manages a collection of notes."""

    def __init__(self):
        """Initializes a new NoteManager with an empty list of notes."""
        self.notes = []

    def add_note(self, title: str, content: str, tags: set = None) -> None:
        """
        Adds a new note to the collection.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
            tags(set(str)): list with tag words
        """
        note = Note(title, content, tags)
        self.notes.append(note)

    def add_notes(self, other) -> None:
        """
        Extends self.notes with notes from other NoteManager object
        """
        titles = set(note.title for note in self.notes)
        for note in other.notes:
            if note.title not in titles:
                self.notes.append(note)

    def add_tag_to_note(self, title: str, tag: str) -> bool:
        """
        Adds the tag to the note found by title.

        Args:
            title (str): The title of the note.
            tag (str): The tag of the note.
        """        
        
        for note in self.notes:
            if note.title == title:
                note.tags.add(tag)


    def delete_note(self, title: str) -> bool:
        """
        Deletes the note found by title.

        Args:
            title (str): The title of the note.
        """

        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)


    def delete_tag_from_note(self, title: str, tag: str) -> bool:
        """
        Deletes tag from the note found by title.

        Args:
            title (str): The title of the note.
            tag (str): The tag of the note.
        """

        for note in self.notes:
            if note.title == title:
                note.tags.discard(tag)
   

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
                    new_note_book.add_note(note_data["title"], note_data["content"], set(note_data["tags"]))
        except (FileNotFoundError, KeyError):
            pass

        return new_note_book

    def get_all_notes(self) -> list[Note]:
        """ Returns a list of all notes."""
        return self.notes


    def get_titles(self) -> list[str]:
        """Returns a list of all titles"""
        return [note.title for note in self.notes]


    def save_notes_to_json(self, filename: str) -> None:
        """
        Saves the notes to a JSON file.

        Args:
            filename (str): The name of the JSON file to save the notes to.
        """
        data = []
        for note in self.notes:
            data.append({"title": note.title, "content": note.content, "tags": list(note.tags)})

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

    @classmethod
    def string_from_list(cls, notes: list[Note]) -> str:
        """makes multiline string from given list of Notes"""
        result = ""
        for i, note in enumerate(notes, 1):
            result += f"{i:>3}. Title: {note.title}\n"
            result += f"     Content: {note.content}\n"
            if note.tags:
                result += f"     Tags: {', '.join(note.tags)}\n"
            result += "\n"
        return result
