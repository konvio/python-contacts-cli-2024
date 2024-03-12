import datetime
import json

from contacts24.model import AddressBook, Note
from contacts24.config import ADDRESSBOOK_FILE, NOTES_FILE
from contacts24.errors import AppError


#region AddressBook 

def get_contacts(filename: str = ADDRESSBOOK_FILE) -> AddressBook:
    """Get addressbook from json file (default config.ADDRESSBOOK_FILE)

    Raises:
        AppError: Any errors (incorrect json, etc.) wrapped in AppError

    Returns:
        AddressBook: AddressBook from json
    """
    address_book = AddressBook()
    
    try:
        with open(filename, "r") as file:
            records_list = json.load(file)
            
        for record_dict in records_list:
            record = record_deserialization(record_dict)
            address_book.add_record(record)
    except Exception as e:
        raise AppError(e)
    
    return address_book

def save_contacts(address_book: AddressBook, filename: str = ADDRESSBOOK_FILE) -> None:
    """Save contacts to json file (from config.ADDRESSBOOK_FILE)

    Args:
        address_book (AddressBook): Address Book to save
        filename (str): file name

    Raises:
        AppError: Any errors (missing file, incorrect json) wrapped in AppError
    """
    try:
        with open(filename, "w") as file:
            json.dump(contacts, file)
    except Exception as e:
        raise AppError(e)

#endregion

#region Record Serialization Helper

def record_serialization(record: Record) -> dict:
    """Record to dictionary

    Args:
        record (Record): input

    Returns:
        dict: dictionary based on input record
    """
    return {
        "name": record.name.value,
        "phones": [phone.value for phone in record.phones],
        "birthday": record.birthday.value if record.birthday else None,
    }

def record_deserialization(data: dict) -> Record:
    """Deserialization Record from json

    Args:
        data (dict): Record in json

    Returns:
        Record: instance of class Record
    """
    record = Record(data["name"])
    
    for phone in data["phones"]:
        record.add_phone(phone)
    
    if data["birthday"]:
        record.add_birthday(data["birthday"])
    
    return record

#endregion
