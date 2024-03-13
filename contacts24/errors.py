HELP_ERROR_MESSAGE = """\
+--------------+----------------------------------+----------------------------------+
| Command      | Description                      | Format                           |
+--------------+----------------------------------+----------------------------------+
| add          | Adds a new contact               | 'add <username> <phone>'         |
| change-phone | Changes a contact's phone number | 'change-phone <username> <phone>'|
| phone        | Prints a contact's number        | 'phone <username>'               |
| add-birthday | Adds a contact's birthday        | 'add-birthday <username> <date>' |
| show-birthday| Prints a contact's birthday      | 'show-birthday <username>'       |
| birthdays    | Prints upcoming birthdays        | 'birthdays'                      |
| all-contacts | Prints all contacts              | 'all-contacts'                   |
| exit/close   | Closes the app                   | 'exit' or 'close'                |
+--------------+----------------------------------+----------------------------------+
"""


class AppError(Exception):
    pass


class InputError(Exception):
    """Base class for other input exceptions"""
    pass


class AddContactInputError(InputError):
    def __str__(self):
        return "AddContactInputError: 'add' command expects two arguments 'name' and 'phone'."


class AddBirthdatInputError(InputError):
    def __str__(self):
        return "AddBirthdatInputError: 'add-birthday' command expects two arguments 'name' and 'birthday'."


class ChangeInputError(InputError):
    def __str__(self):
        return "ChangeInputError: 'change' command expects two arguments 'name' and 'phone'."


class PhoneInputError(InputError):
    def __str__(self):
        return "PhoneInputError: 'phone' command expects one argument 'name'."


class GetBirthdayInputError(InputError):
    def __str__(self):
        return "GetBirthdayInputError: 'show-birthday' command expects one argument username"


class InaccurateBirthdayFormat(InputError):
    def __str__(self):
        return "InaccurateBirthdayFormat: Birthday must be in format DD.MM.YYYY."


class InaccuratePhoneFormat(InputError):
    def __str__(self):
        return "InaccuratePhoneFormat: Phone number must contain exactly 10 digits."


class NonExistingContact(InputError):
    def __str__(self):
        return "NonExistingContact: Check contact name, no such contact in address book"


class NonExistingNote(InputError):
    def __str__(self):
        return "NonExistingNote: This note does not exist or has been deleted"

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InputError as e:
            return str(e)

    return inner



