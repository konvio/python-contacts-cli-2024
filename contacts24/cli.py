"""Prototype of CLI assistant"""

from functools import partial

from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter, WordCompleter
from prompt_toolkit.styles import Style

from .config import PROMPT_MESSAGE, PROMPT_STYLE
from .contacts import (
    add_birthday,
    add_contact,
    change_contact,
    get_all_contacts,
    get_contact_birthday,
    get_contact_phone,
    get_upcoming_birthdays,
    load_contacts_book,
    parse_input,
)
from .errors import HELP_ERROR_MESSAGE

init(autoreset=True)


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
    print(Fore.LIGHTGREEN_EX + "Welcome to the Contants24!\n" + Fore.WHITE + "Type 'help' to see available commands.\n")
    command_completer = FuzzyWordCompleter(list(commands.keys()))
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
                print(Fore.WHITE + str(commands[command](args)))
            else:
                print(Fore.RED + f"Unknown command '{command}', please try again.\n{HELP_ERROR_MESSAGE}")
        except Exception as e:
            print(Fore.RED + f"Unexpected error occured {e}")
