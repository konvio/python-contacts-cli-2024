"""Prototype of CLI assistant"""

from functools import partial

from colorama import Fore, init
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from .cli_commands import Command

from .config import PROMPT_MESSAGE, PROMPT_STYLE
from .contacts import (
    add_birthday,
    add_contact,
    change_contact,
    change_email,
    add_address,
    get_all_contacts,
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
    "help": Command("help",  lambda x: "\n\nAvailable commands: \n{0}\n".format(get_help()), is_hidden=True),
    "add": Command("add",  partial(add_contact, contacts=contacts), "Adds a new contact", "add <username> <phone>"),
    "change-phone": Command("change-phone", partial(change_contact, contacts=contacts), "Changes a contact's phone number", "change-phone <username> <phone>"), 
    "change-email": Command("change-email", partial(change_email, contacts=contacts), "Changes a contact's email", "change-email <username> <email>"),
    "change-address": Command("change-address", partial(add_address, contacts=contacts), "Changes a contact's address", "change-email <username> <address>"),
    "phone": Command("phone", partial(get_contact_phone, contacts=contacts), "Prints a contact's number", "phone <username>"), 
    "add-birthday": Command("add-birthday", partial(add_birthday, contacts=contacts),  "Adds a contact's birthday", "add-birthday <username> <date>"), 
    "show-birthday": Command("show-birthday", partial(get_contact_birthday, contacts=contacts),  "Prints a contact's birthday", "show-birthday <username>"), 
    "birthdays": Command("birthdays", partial(get_upcoming_birthdays, contacts=contacts), "Prints upcoming birthdays", "birthdays"), 
    "all-contacts": Command("all-contacts", partial(get_all_contacts, contacts=contacts), "Prints all contacts", "all-contacts"), 
    "add-note": Command("add-note", lambda x: "In development"), 
    "change-note": Command("change-note", lambda x: "In development"), 
    "find-note": Command("find-note", lambda x: "In development"), 
    "get-all-notes":Command("get-all-notes", lambda x: "In development"), 
}

def get_help() -> str:
    """Generate help based on the available list of commands

    Returns:
        str: Help table
    """
    message = "\n"
    
    padding_command = len("Command")
    padding_description = len("Description")
    padding_format = len("Format")
    
    for name, command in commands.items():
        if command.is_hidden:
            continue
        padding_command = max([padding_command, len(name)])
        padding_description = max([padding_description, len(command.description)])
        padding_format = max([padding_format, len(command.format)])
    
    message += (("| {0:-^%s} " % padding_command ) + ("| {0:-^%s} |" % padding_description) + (" {0:-^%s} |\n" % padding_format)).format("-")
    message += (("| {0:^%s} " % padding_command ) + ("| {1:^%s} |" % padding_description) + (" {2:^%s} |\n" % padding_format)).format("Command", "Description", "Format")
    message += (("| {0:-^%s} " % padding_command ) + ("| {0:-^%s} |" % padding_description) + (" {0:-^%s} |\n" % padding_format)).format("-")
    
    for name, command in commands.items():
        if command.is_hidden:
            continue
        message += (("| {0:<%s} " % padding_command ) + ("| {1:<%s} |" % padding_description) + (" {2:<%s} |\n" % padding_format)).format(command.name, command.description, command.format)
    message += (("| {0:-^%s} " % padding_command ) + ("| {0:-^%s} |" % padding_description) + (" {0:-^%s} |\n" % padding_format)).format("-")
    
    return message

def start():
    print(Fore.LIGHTGREEN_EX + "Welcome to the Contants24!\n" + Fore.WHITE + "Type 'help' to see available commands.\n")
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
                help_text = get_help()
                print(Fore.RED + f"Unknown command '{command}', please try again.\n{help_text}")
        except Exception as e:
            print(Fore.RED + f"Unexpected error occured {e}")
