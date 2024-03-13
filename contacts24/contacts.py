"""CLI assistant functions"""

from typing import Optional

from contacts24.config import ADDRESSBOOK_FILE
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
        contacts = AddressBook.load_from_file(ADDRESSBOOK_FILE)
    except FileNotFoundError:
        print("File 'address_book.json' not found. Initializing an empty AddressBook.")
        contacts = AddressBook()
    return contacts


@input_error
def add_contact(args: CommandArguments, contacts: AddressBook) -> str:
    if args is None or len(args) < 4:
        raise AddContactInputError()

    name, phone, email, address = args[:4]
    new_contact = Record(name)
    new_contact.add_phone(phone)
    new_contact.add_email(email)
    new_contact.add_address(address)
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
    if args is None or len(args) < 4:
        raise ChangeInputError()

    name, phone, email, address = args[:4]
    contact = contacts.find(name)
    if not contact:
        raise NonExistingContact()

    contact.edit_phone(contact.phones[0].value, phone)
    contact.edit_email(contact.emails[0].value, email)
    contact.add_address(address)
    return f"Phone number, email and address for {name} updated."


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
