


from collections import UserDict
from contacts24.errors import NonExistingNote



class Notes(UserDict):
    """This class provides functionality for working with notes"""
    def add_note(self, title, text):
        """Adds a new note to the notebook."""
        max_index = max(self.data.keys()) if self.data else 0
        note_id = max_index + 1  # Generates a unique identifier for the note
        self.data[note_id] = {'note_id': note_id, 'title': title, 'text': text}

    def change_note(self, key, new_text):
        """Changes the text of an existing note by its key."""
        if key in self.data:
            self.data[key]['text'] = new_text
        else:
            raise NonExistingNote()

    def get_notes(self):
        """Returns all notes from the notebook."""
        return self.data.values()

    def delete_note(self, key):
        """Deletes a note by its key."""
        if key in self.data:
            del self.data[key]
        else:
            raise NonExistingNote()

    def search_text(self, search_query):
        """Searches for notes by a text query."""
        found_notes = []
        for note_id, note_data in self.data.items():
            if search_query in note_data['text']:
                found_notes.append((note_id, note_data))
        return found_notes