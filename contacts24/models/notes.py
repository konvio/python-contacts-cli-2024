from collections import UserDict
from contacts24.errors import NonExistingNote
from contacts24.models.note import Note


class Notes(UserDict):
    """This class provides functionality for working with notes"""
    
    def add_note(self, text: str) -> None:
        """Adds a new note to the notebook."""
        
        index = self._get_new_note_index()
        
        self.add_note_byid(Note(index, text))
        
    def add_note_byid(self, note: Note) -> None:
        """Adds a new note to the notebook by id"""
    
        self.data[note.id.value] = note

    def _get_new_note_index(self) -> int:
        """Get new index for new note"""
        
        max_index = max(self.data.keys()) if len(self.data) > 0 else 0
        return max_index + 1

    def change_note(self, id: int, new_text: str) -> None:
        """Changes the text of an existing note by its id."""
        
        if id not in self.data:
            raise NonExistingNote()
        
        self.data[id] = Note(id, new_text)

    def get_notes(self) -> list[Note]:
        """Returns all notes from the notebook."""
        
        return list(self.data.values())

    def delete_note(self, id: int) -> None:
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
        