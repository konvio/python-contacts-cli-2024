"""CLI assistant functions"""

from typing import Optional

from .models.address_book import AddressBook
from .models.record import Record
from .errors import (
    AddBirthdatInputError,
    AddContactInputError,
    ChangeInputError,
    GetBirthdayInputError,
    NonExistingContact,
    PhoneInputError,
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

    return cmd, *args


def load_contacts_book() -> AddressBook:
    try:
        contacts = AddressBook.load_from_file("address_book.json")
    except FileNotFoundError:
        print("File 'address_book.json' not found. Initializing an empty AddressBook.")
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
        raise AddBirthdatInputError()

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
    return f"Phone number for {name} updated."


@input_error
def get_contact_phone(args: CommandArguments, contacts: AddressBook) -> str:
    if args[0] is None:
        raise PhoneInputError()

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    return contact.phones[0].value


@input_error
def get_contact_birthday(args: CommandArguments, contacts: AddressBook) -> str:
    if args[0] is None:
        raise GetBirthdayInputError()

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    return contact.birthday


@input_error
def get_upcoming_birthdays(contacts: AddressBook) -> str:
    return contacts.get_birthdays_per_week()


def get_all_contacts(contacts: AddressBook) -> str:
    if not contacts:
        return "No contacts stored."
    else:
        return "\n".join([str(contact) for contact in contacts.data.values()])
