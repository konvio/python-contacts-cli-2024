"""CLI assistant functions"""

from typing import Optional

from .models.address_book import AddressBook
from .models.record import Record
from .birthdays import get_birthdays_within_days
from .errors import (
    AppError,
    AddBirthdayInputError,
    AddContactInputError,
    ChangeInputError,
    ChangeEmailInputError,
    FindContactsInputError,
    AddAddressInputError,
    GetBirthdayInputError,
    NonExistingContact,
    PhoneInputError,
    InAccurateBirthdaysCommand,
    DeleteContactError,
    input_error,
)

Contacts = dict[str, str]
CommandArguments = list[str]


def parse_input(user_input: str) -> tuple[str, Optional[CommandArguments]]:
    if not user_input.strip():
        return "", None

    cmd, *args = user_input.split(" ")
    cmd = cmd.strip().lower()

    if len(args) == 0:
        return cmd, None

    return cmd, args

def load_contacts_book(filepath: str) -> AddressBook:
    try:
        contacts = AddressBook.load_from_file(filepath)
    except FileNotFoundError:
        print(f"File {filepath} not found. Initializing an empty AddressBook.")
        contacts = AddressBook()
    except AppError:
        print(f"File {filepath} cannot be loaded. Initializing an empty AddressBook.")
        contacts = AddressBook()
    return contacts


@input_error
def add_contact(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None or len(args) < 2:
        raise AddContactInputError()

    name, phone = args[:2]
    new_contact = Record(name)
    new_contact.add_phone(phone)
    contacts.add_record(new_contact)
    return f"Contact {name} added."


@input_error
def add_birthday(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None or len(args) < 2:
        raise AddBirthdayInputError()

    name, date = args[:2]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    contact.add_birthday(date)
    return f"Birthday added for {name} updated."


@input_error
def change_contact(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None or len(args) < 2:
        raise ChangeInputError()

    name, phone = args[:2]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    contact.edit_phone(contact.phones[0].value, phone)
    return f"Phone number, email and address for {name} updated."


@input_error
def get_contact_phone(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None:
        raise PhoneInputError()

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    return contact.phones[0].value


@input_error
def get_contact_birthday(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None:
        raise GetBirthdayInputError()

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    return contact.birthday


@input_error
def delete_contact(args: CommandArguments, contacts: AddressBook) -> str:
    """Deletes a note from the notebook."""
    if args is None or len(args) < 1:
        raise DeleteContactError()
    
    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()
    contacts.delete(name)
    
    return "Contact deleted."


@input_error
def get_upcoming_birthdays(args: CommandArguments, contacts: AddressBook) -> str:
    try:
        n_days = int(args[0])
    except TypeError:
        raise InAccurateBirthdaysCommand()

    if n_days >= 0:
        return get_birthdays_within_days(contacts, n_days)
    else:
        raise InAccurateBirthdaysCommand()


def get_all_contacts(args: CommandArguments, contacts: AddressBook) -> str:
    if not contacts:
        return "No contacts stored."
    else:
        return str(contacts)


def find_contacts(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None or len(args) < 1:
        raise FindContactsInputError()

    name = args[0]
    result_book = AddressBook()

    for contact in contacts.data.values():
        if name in str(contact.name):
            result_book.add_record(contact)

    if len(result_book) == 0:
        return "No contacts found."
    elif len(result_book) == 1:
        contact = result_book.find(list(result_book.data.keys())[0])
        return contact
    else:
        return result_book
    

@input_error
def change_email(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None or len(args) < 2:
        raise ChangeEmailInputError()

    name, email = args[:2]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    if len(contact.emails):
        contact.edit_email(contact.emails[0].value, email)
    else:
        contact.add_email(email)

    return f"Email for {name} updated."

@input_error
def add_address(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None or len(args) < 2:
        raise AddAddressInputError()

    name, address = args[:2]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    contact.add_address(address)
    return f"Address for {name} updated."
