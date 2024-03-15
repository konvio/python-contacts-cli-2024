from contacts24.errors import input_error, AddNoteInputError, ChangeNoteError
from contacts24.models.notes import Notes



@input_error
def show_all_notes(args, notes: Notes) -> str:
    """Shows all notes from the notebook."""
    if not notes:
        return "No notes stored"
    
    return "\n".join([str(note) for note in notes.data.values()])


@input_error
def add_note(args, notes):
    """Adds a note to the notebook."""
    if args is None or len(args) < 1:
        raise AddNoteInputError()

    text = " ".join(args)
    notes.add_note(text)
    
    return "Note added."


@input_error
def change_note(args, notes: Notes):
    """Changes the text of an existing note."""
    if args is None or len(args) < 2:
        raise ChangeNoteError()
    
    key = args[0]
    new_text = " ".join(args[1:])
    
    notes.change_note(int(key), new_text)
    
    return "Note changed."





@input_error
def delete_note(args, notes):
    """Deletes a note from the notebook."""
    
    key, = args
    notes.delete_note(int(key))
    
    return "Note deleted."


@input_error
def search_text(args, notes):
    """Searches for notes by a text query."""
    
    search_query, = args
    found_notes = notes.search_text(search_query)
    
    if found_notes:
        return "\n----------------------------\n".join([str(note) for note in found_notes])
    else:
        return "No notes found."