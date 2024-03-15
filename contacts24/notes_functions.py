
from contacts24.errors import (
    input_error,
    AddNoteInputError,
    ChangeNoteError,
    FindNoteInputError,
    DeleteNoteError,
    InvalidNoteIdError,
    NonExistingNote,
    AddTagError,
    AppError
)
from contacts24.models.notes import Notes

CommandArguments = list[str]


def load_notes(filepath: str) -> Notes:
    """Load notes from file

    Args:
        filepath (str): path to local file

    Returns:
        Notes: notes from file system or new instance in case of issues with local file
    """
    try:
        notes = Notes.load_from_file(filepath)
    except FileNotFoundError:
        print(f"File {filepath} not found. Initializing an empty Notes.")
        notes = Notes()
    except AppError:
        print(f"File {filepath} cannot be loaded. Initializing an empty Notes.")
        notes = Notes()
    return notes

def show_all_notes(args: CommandArguments, notes: Notes) -> str:
    """Shows all notes from the notebook.

    Args:
        args (CommandArguments): list of arguments from user
        notes (Notes): notes

    Returns:
        str: list of all notes or message for no notes
    """
    if not notes:
        return "You don't have any notes.\n\nUse `add-note` to create one.\n\n"
    
    return "\n".join([str(note) for note in notes.data.values()])


@input_error
def add_note(args: CommandArguments, notes: Notes) -> str:
    """Adds a note to the notebook.

    Args:
        args (CommandArguments): User parameters. Expected note text
        notes (Notes): Notes

    Raises:
        AddNoteInputError: if user doesn't provide necessary arguments

    Returns:
        str: message about successfully added note
    """
    if args is None or len(args) < 1:
        raise AddNoteInputError()

    text = " ".join(args)
    index = notes.add_note(text)
    
    return f"Note added (by #{index})."


@input_error
def change_note(args: CommandArguments, notes: Notes) -> str:
    """Changes the text of an existing note.

    Args:
        args (CommandArguments): User parameters. Expected note id and new note text
        notes (Notes): Notes

    Raises:
        ChangeNoteError: if user doesn't provide necessary arguments

    Returns:
        str: message about successfully changed note
    """
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
    
    try:
        key_int = int(key)
    except:
        raise InvalidNoteIdError()
    
    notes.delete_note(key_int)
    
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
    

@input_error
def add_tag(args: CommandArguments, notes: Notes) -> str:
    """Add tag to note

    Args:
        args (CommandArguments): User parameters. Expected note id and tag
        notes (Notes): Notes

    Raises:
        ChangeNoteError: if user doesn't provide necessary arguments

    Returns:
        str: message about successfully changed note
    """
    if args is None or len(args) < 2:
        raise AddTagError()
    
    key, tag = args[:2]
    
    try:
        key_int = int(key)
    except:
        raise InvalidNoteIdError()
    
    if not notes.is_note_exists(key_int):
        raise NonExistingNote()
    
    notes.add_tag(key_int, tag)
    
    return f"Tag added to note #{key}."

