
from contacts24.errors import (
    input_error,
    AddNoteInputError,
    ChangeNoteError,
    FindNoteInputError,
    DeleteNoteError
)
from contacts24.models.notes import Notes


def load_notes(filepath: str) -> Notes:
    try:
        notes = Notes.load_from_file(filepath)
    except FileNotFoundError:
        print(f"File {filepath} not found. Initializing an empty Notes.")
        notes = Notes()
    except AppError:
        print(f"File {filepath} cannot be loaded. Initializing an empty Notes.")
        notes = Notes()
    return notes


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
    index = notes.add_note(text)
    
    return f"Note added (by #{index})."


@input_error
def change_note(args, notes: Notes):
    """Changes the text of an existing note."""
    if args is None or len(args) < 2:
        raise ChangeNoteError()
    
    key = args[0]
    new_text = " ".join(args[1:])
    
    notes.change_note(int(key), new_text)
    
    return f"Note changed (by #{key})."


@input_error
def delete_note(args, notes):
    """Deletes a note from the notebook."""
    if args is None or len(args) < 1:
        raise DeleteNoteError()
    
    key = args[0]
    notes.delete_note(int(key))
    
    return "Note deleted."


@input_error
def search_text(args, notes: Notes):
    """Searches for notes by a text query."""
    if args is None or len(args) < 1:
        raise FindNoteInputError()
    
    search_query = " ".join(args)
    found_notes = notes.search_text(search_query)
    
    if found_notes:
        return "\n----------------------------\n".join([str(note) for note in found_notes])
    else:
        return f"No notes found by the following text `{search_query}`."