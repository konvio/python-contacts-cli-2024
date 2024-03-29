import json

from contacts24.models.address_book import AddressBook
from contacts24.models.notes import Notes
from contacts24.config import ADDRESSBOOK_FILE, NOTES_FILE
from contacts24.errors import app_error_wrapper
from contacts24.serialization_helper import record_deserialization, record_serialization, note_deserialization, note_serialization


#region AddressBook

@app_error_wrapper
def get_contacts(filename: str = ADDRESSBOOK_FILE) -> AddressBook:
    """Get addressbook from json file (default config.ADDRESSBOOK_FILE)

    Returns:
        AddressBook: AddressBook from json
    """
    address_book = AddressBook()
    
    with open(filename, "r") as file:
        records_list = json.load(file)
        
    for record_dict in records_list:
        record = record_deserialization(record_dict)
        address_book.add_record(record)
    
    return address_book

@app_error_wrapper
def save_address_book(address_book: AddressBook, filename: str = ADDRESSBOOK_FILE) -> None:
    """Save address book to json file (from config.ADDRESSBOOK_FILE)

    Args:
        address_book (AddressBook): Address Book to save
        filename (str): file name

    """
    with open(filename, "w") as file:
        records_list = [record_serialization(record) for record in address_book.data.values()]
        json.dump(records_list, file)

#endregion

#region Notes

@app_error_wrapper
def get_notes(filename: str = NOTES_FILE) -> Notes:
    """Get notes from fixed json file (from config.NOTES_FILE)

    Returns:
        Notes: List of notes
    """
    notes = Notes()
    
    with open(filename, "r") as file:
        notes_list = json.load(file)
        for note_dict in notes_list:
            note = note_deserialization(note_dict)
            notes.add_note_byid(note)
    
    return notes

@app_error_wrapper
def save_notes(notes: Notes, filename: str = NOTES_FILE) -> None:
    """Save notes to json file (from config.NOTES_FILE)

    Args:
        notes (Notes): Notes to save
    """

    with open(filename, "w") as file:
        notes_list = [note_serialization(note) for note in notes.data.values()]
        json.dump(notes_list, file)

#endregion