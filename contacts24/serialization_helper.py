from contacts24.models.record import Record
from contacts24.models.note import Note

#region Record serialization

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

#region Note serialization

def note_serialization(note: Note) -> dict:
    """Note to dictionary

    Args:
        note (Note): input

    Returns:
        dict: dictionary based on input record
    """
    return {
        "id": note.name.value,
        "text": note.text.value,
    }

def note_deserialization(data: dict) -> Note:
    """Deserialization Note from json

    Args:
        data (dict): Note in json

    Returns:
        Note: instance of class Note
    """
    note = Note()
    
    note.add_text(data["text"], data["id"])
    
    return note

#endregion
