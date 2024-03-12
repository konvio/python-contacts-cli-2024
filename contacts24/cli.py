"""Prototype of CLI assistant"""

from .contacts import (
    add_birthday,
    add_contact,
    change_contact,
    get_all_contacts,
    get_contact_birthday,
    get_contact_phone,
    get_upcoming_birthdays,
    load_contacts_book,
    parse_input
)
from .errors import HELP_ERROR_MESSAGE


def start():
    contacts = load_contacts_book()
    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)
            if command in ["close", "exit"]:
                contacts.save_to_file()
                print("Contact book is saved, Good bye!")
                break
            if command in ["hello", "hi"]:
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, contacts))
            elif command == "add-birthday":
                print(add_birthday(args, contacts))
            elif command == "change":
                print(change_contact(args, contacts))
            elif command == "phone":
                print(get_contact_phone(args, contacts))
            elif command == "show-birthday":
                print(get_contact_birthday(args, contacts))
            elif command == "birthdays":
                print(get_upcoming_birthdays(contacts))
            elif command == "all":
                print(get_all_contacts(contacts))
            else:
                print(f"Unknown command '{command}', please try again.\n{HELP_ERROR_MESSAGE}")
    except Exception as e:
        print(f"Unexpected error occured {e}")
        contacts.save_to_file()
