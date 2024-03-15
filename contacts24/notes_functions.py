

from contacts24.errors import input_error



@input_error
def add_note(args, note_book):
    """Adds a note to the notebook."""
    
    note_id, text = args
    note_book.add_note(note_id, text)
    
    return "Note added."


@input_error
def change_note(args, note_book):
    """Changes the text of an existing note."""
    
    key, new_text = args
    note_book.change_note(int(key), new_text)
    
    return "Note changed."


@input_error
def get_notes(note_book):
    """Shows all notes from the notebook."""
    
    notes = note_book.get_notes()
    
    return "\n".join([str(note) for note in notes])


@input_error
def delete_note(args, note_book):
    """Deletes a note from the notebook."""
    
    key, = args
    note_book.delete_note(int(key))
    
    return "Note deleted."


@input_error
def search_text(args, note_book):
    """Searches for notes by a text query."""
    
    search_query, = args
    found_notes = note_book.search_text(search_query)
    
    if found_notes:
        return "\n----------------------------\n".join([str(note) for note in found_notes])
    else:
        return "No notes found."