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

from functools import partial


contacts = load_contacts_book()

commands = {
    "hello": lambda x: "How can I help you?",
    "help": lambda x: f"Available commands: {HELP_ERROR_MESSAGE}",
    "add": partial(add_contact, contacts=contacts),
    "change-phone": partial(change_contact, contacts=contacts),
    "change-email": lambda x: "In development",
    "change-address": lambda x: "In development",
    "phone": partial(get_contact_phone, contacts=contacts),
    "add-birthday": partial(add_birthday, contacts=contacts),
    "show-birthday": partial(get_contact_birthday, contacts=contacts),
    "birthdays": partial(get_upcoming_birthdays, contacts=contacts),
    "all-contacts": partial(get_all_contacts, contacts=contacts),
    "add-note": lambda x: "In development",
    "change-note": lambda x: "In development",
    "find-note": lambda x: "In development",
    "get-all-notes": lambda x: "In development",
}


def start():
    print("Welcome to the assistant bot! Type 'help' to see available commands.")
    try:
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command == "exit":
                print("Good bye!")
                break

            if command in commands:
                print(commands[command](args))
            else:
                print(f"Unknown command '{command}', please try again.\n{HELP_ERROR_MESSAGE}")
    except Exception as e:
        print(f"Unexpected error occured {e}")
        contacts.save_to_file()
