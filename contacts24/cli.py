"""Prototype of CLI assistant"""

from functools import partial

from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from .cli_commands import Command, get_help

from .config import PROMPT_MESSAGE, PROMPT_STYLE
from .contacts import (
    add_birthday,
    add_contact,
    change_contact,
    change_email,
    add_address,
    get_all_contacts,
    find_contacts,
    get_contact_birthday,
    get_contact_phone,
    get_upcoming_birthdays,
    load_contacts_book,
    parse_input,
)

init(autoreset=True)


contacts = load_contacts_book()

commands = {
    "hello": Command("hello", lambda x: "How can I help you?", is_hidden = True),
    "help": Command("help",  lambda x: "\n\nAvailable commands: \n{0}\n".format(get_help(commands)), is_hidden=True),
    "add-contact": Command("add-contact",  partial(add_contact, contacts=contacts), "Adds a new contact", "add-contact <username> <phone>"),
    "change-phone": Command("change-phone", partial(change_contact, contacts=contacts), "Changes a contact's phone number", "change-phone <username> <phone>"), 
    "change-email": Command("change-email", partial(change_email, contacts=contacts), "Changes a contact's email", "change-email <username> <email>"),
    "change-address": Command("change-address", partial(add_address, contacts=contacts), "Changes a contact's address", "change-email <username> <address>"),
    "show-phone": Command("show-phone", partial(get_contact_phone, contacts=contacts), "Prints a contact's number", "show-phone <username>"), 
    "add-birthday": Command("add-birthday", partial(add_birthday, contacts=contacts),  "Adds a contact's birthday", "add-birthday <username> <date>"), 
    "show-birthday": Command("show-birthday", partial(get_contact_birthday, contacts=contacts),  "Prints a contact's birthday", "show-birthday <username>"), 
    "birthdays": Command("birthdays", partial(get_upcoming_birthdays, contacts=contacts), "Prints upcoming birthdays", "birthdays"), 
    "show-all-contacts": Command("show-all-contacts", partial(get_all_contacts, contacts=contacts), "Prints all contacts", "show-all-contacts"), 
    "find-contacts": Command("find-contact", partial(find_contacts, contacts=contacts), "Prints contacts by name", "find-contacts"),
    "add-note": Command("add-note", lambda x: "In development"),
    "change-note": Command("change-note", lambda x: "In development"), 
    "find-note": Command("find-note", lambda x: "In development"), 
    "show-all-notes": Command("show-all-notes", lambda x: "In development"), 
}


def start():
    print(Fore.LIGHTGREEN_EX + "Welcome to the Contacts24!\n" + Fore.WHITE + "Type 'help' to see available commands.\n")
    command_completer = WordCompleter(list(commands.keys()))
    while True:
        try:
            style = Style.from_dict(PROMPT_STYLE)
            user_input = prompt(PROMPT_MESSAGE, style=style, completer=command_completer)
            command, args = parse_input(user_input)

            if command == "exit":
                print(Fore.LIGHTGREEN_EX + "Good bye!")
                contacts.save_to_file()
                break

            if command in commands:
                print(Fore.WHITE + str(commands[command]()(args)))
            else:
                help_text = get_help(commands)
                print(Fore.RED + f"Unknown command '{command}', please try again.\n{help_text}")
        except Exception as e:
            print(Fore.RED + f"Unexpected error occured {e}")
