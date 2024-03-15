"""Prototype of CLI assistant"""

from functools import partial

from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from .cli_commands import Command, get_help
from .os_resources import get_file_path

from .config import PROMPT_MESSAGE, PROMPT_STYLE, ADDRESSBOOK_FILE
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
from .notes_functions import (
    show_all_notes,
    add_note,
    change_note,
    search_text
)
from contacts24.models.notes import Notes

init(autoreset=True)


contacts = load_contacts_book(get_file_path(ADDRESSBOOK_FILE))

def mock_notes():
    mock_notes = Notes()
    mock_notes.add_note("Some text")
    mock_notes.add_note("Second text about second text not to forget second text")
    mock_notes.add_note("Third note")
    return mock_notes


notes = mock_notes()

commands = {
    "hello": Command("hello", lambda x: "How can I help you?\n", is_hidden = True),
    "help": Command("help",  lambda x: "\n\nAvailable commands: \n{0}\n".format(get_help(commands)), is_hidden=True),
    "add-contact": Command("add-contact",  partial(add_contact, contacts=contacts), "Adds a new contact", "add-contact <username> <phone>"),
    "change-phone": Command("change-phone", partial(change_contact, contacts=contacts), "Changes a contact's phone number", "change-phone <username> <phone>"), 
    "change-email": Command("change-email", partial(change_email, contacts=contacts), "Changes a contact's email", "change-email <username> <email>"),
    "change-address": Command("change-address", partial(add_address, contacts=contacts), "Changes a contact's address", "change-email <username> <address>"),
    "show-phone": Command("show-phone", partial(get_contact_phone, contacts=contacts), "Prints a contact's number", "show-phone <username>"), 
    "add-birthday": Command("add-birthday", partial(add_birthday, contacts=contacts),  "Adds a contact's birthday", "add-birthday <username> <date>"), 
    "show-birthday": Command("show-birthday", partial(get_contact_birthday, contacts=contacts),  "Prints a contact's birthday", "show-birthday <username>"), 
    "birthdays": Command("birthdays", partial(get_upcoming_birthdays, contacts=contacts), "Prints upcoming birthdays in N days", "birthdays <n_days>"), 
    "show-all-contacts": Command("show-all-contacts", partial(get_all_contacts, contacts=contacts), "Prints all contacts", "show-all-contacts"), 
    "find-contacts": Command("find-contact", partial(find_contacts, contacts=contacts), "Prints contacts by name", "find-contacts"),
    "add-note": Command("add-note", partial(add_note, notes=notes), "Adds a new note", "add-note <text>"), 
    "change-note": Command("change-note", partial(change_note, notes=notes), "Changes a note's text", "change_note <id> <new_text>"), 
    "find-note": Command("find-note", partial(search_text, notes=notes), "Prints notes by search query", "find-note <search_query>"), 
    "show-all-notes": Command("show-all-notes", partial(show_all_notes, notes=notes), "Prints all notes", "show-all-notes"), 
}


def start():
    print(Fore.LIGHTGREEN_EX + "\n\nWelcome to the Contacts24!\n\n" + Fore.WHITE + "\nType 'help' to see available commands.\n\n")
    command_completer = WordCompleter(list(commands.keys()))
    while True:
        try:
            style = Style.from_dict(PROMPT_STYLE)
            user_input = prompt(PROMPT_MESSAGE, style=style, completer=command_completer)
            command, args = parse_input(user_input)

            if command == "exit":
                print(Fore.LIGHTGREEN_EX + "Good bye!")
                contacts.save_to_file(get_file_path(ADDRESSBOOK_FILE))
                break

            if command in commands:
                print(Fore.WHITE + str(commands[command]()(args)))
            else:
                help_text = get_help(commands)
                print(Fore.RED + f"Unknown command '{command}', please try again.\n{help_text}")
        except Exception as e:
            print(Fore.RED + f"Unexpected error occured {e}\n")
