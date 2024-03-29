from collections import UserDict
from contacts24.errors import NonExistingNote
from contacts24.config import NOTES_FILE
from contacts24.models.note import Note


class Notes(UserDict):
    """This class provides functionality for working with notes"""
    
    def add_note(self, text: str) -> int:
        """Adds a new note to the notebook."""
        
        index = self._get_new_note_index()
        
        self.add_note_byid(Note(index, text))
        
        return index
        
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

    def is_note_exists(self, id: int) -> bool:
        """Is note exists by id"""
        
        return id in self.data.keys()

    def delete_note(self, id: int) -> None:
        """Deletes a note by its id."""
        
        if id not in self.data:
            raise NonExistingNote()
        
        del self.data[id]

    def search_text(self, search_query: str) -> list[Note]:
        """Searches for notes by a text query."""
        
        found_notes = []
        
        for note_id, note_data in self.data.items():
            if search_query.lower() in note_data.text.value.lower():
                found_notes.append(note_data)
        return found_notes 
        

    def add_tag(self, id: int, tag: str) -> None:
        """Add tag to note by id."""
        
        if id not in self.data:
            raise NonExistingNote()
        
        self.data[id].add_tag(tag)

    def delete_tag(self, id: int, tag: str) -> None:
        """Delete tag from note by id."""
        
        if id not in self.data:
            raise NonExistingNote()
        
        self.data[id].delete_tag(tag)


    def save_to_file(self, filepath: str = NOTES_FILE) -> None:
        from contacts24.db import save_notes
        if filepath:
            save_notes(self, filepath)
        else:
            save_notes(self)
            
    @staticmethod
    def load_from_file(filepath: str = NOTES_FILE) -> "Notes":
        from contacts24.db import get_notes
        if filepath:
            return get_notes(filepath)
        else:
            return get_notes()
