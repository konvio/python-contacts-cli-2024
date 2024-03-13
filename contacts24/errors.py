HELP_ERROR_MESSAGE = """Supported functions:
- 'add': Add new contact, the correct format is 'add username phone email address'
- 'change': Change existing contact, the correct format is 'change username phone email address'
- 'phone': Print existing contact number, the correct format is 'phone username'
- 'add-birthday': command expects two arguments 'name' and 'birthday'
- 'show-birthday': Print existing contact birthday, the correct format is 'show-birthday username'
- 'birthdays': Print birthdays upcoming next week if any, the correct format is 'birthdays'
- 'all': Print all existing contact numbers if any, the correct format is 'all'
- 'exit' | 'close': Close the app, the correct format 'exit' and 'close'
"""


class AppError(Exception):
    pass


class InputError(Exception):
    """Base class for other input exceptions"""
    pass


class AddContactInputError(InputError):
    def __str__(self):
        return "AddContactInputError: 'add' command expects 4 arguments 'name', 'phone', 'email' and 'address'."


class AddBirthdatInputError(InputError):
    def __str__(self):
        return "AddBirthdatInputError: 'add-birthday' command expects two arguments 'name' and 'birthday'."


class ChangeInputError(InputError):
    def __str__(self):
        return "ChangeInputError: 'change' command expects 4 arguments 'name', 'phone', 'email' and 'address'."


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

class InaccurateEmailFormat(InputError):
    def __str__(self):
        return "InaccurateEmailFormat: The email address provided does not adhere to the standard email format."


class NonExistingContact(InputError):
    def __str__(self):
        return "NonExistingContact: Check contact name, no such contact in address book"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InputError as e:
            return str(e)

    return inner
