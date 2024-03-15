from collections import UserDict
from contacts24.errors import NonExistingNote
from contacts24.models.note import Note


class Notes(UserDict):
    """This class provides functionality for working with notes"""
    
    def add_note(self, text: str):
        """Adds a new note to the notebook."""
        
        try:
            max_index = max(self.data.keys())
            note_id = max_index + 1  # Generates a unique identifier for the note
        except ValueError:
            note_id = 1
    
        self.data[note_id] = Note(note_id, text)

    def change_note(self, id: int, new_text: str):
        """Changes the text of an existing note by its id."""
        
        if id not in self.data:
            raise NonExistingNote()
        
        self.data[id].text = new_text

    def get_notes(self):
        """Returns all notes from the notebook."""
        
        return list(self.data.values())

    def delete_note(self, id: int):
        """Deletes a note by its id."""
        
        if id not in self.data:
            raise NonExistingNote()
        
        del self.data[id]

    def search_text(self, search_query: str) -> list[Note]:
        """Searches for notes by a text query."""
        
        found_notes = []
        
        for note_id, note_data in self.data.items():
            if search_query in note_data.text:
                found_notes.append(note_data)
        return found_notes 
        