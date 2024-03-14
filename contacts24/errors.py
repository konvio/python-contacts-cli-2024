
class AppError(Exception):
    pass


class InputError(Exception):
    """Base class for other input exceptions"""
    pass


class AddContactInputError(InputError):
    def __str__(self):
        return "AddContactInputError: 'add-contact' command expects two arguments 'name' and 'phone'"


class AddBirthdatInputError(InputError):
    def __str__(self):
        return "AddBirthdatInputError: 'add-birthday' command expects two arguments 'name' and 'birthday'."


class ChangeInputError(InputError):
    def __str__(self):
        return "ChangeInputError: 'change-phone' command expects two arguments 'name' and 'phone'"

class ChangeEmailInputError(InputError):
    def __str__(self):
        return "ChangeInputError: 'change-email' command expects two arguments 'name' and  'email'."

class FindContactsInputError(InputError):
    def __str__(self):
        return "FindContactsInputError: 'find-contacts' command expects one arguments 'name'."


class AddAddressInputError(InputError):
    def __str__(self):
        return "AddBirthdatInputError: 'add-address' command expects two arguments 'name' and 'address'."

class PhoneInputError(InputError):
    def __str__(self):
        return "PhoneInputError: 'show-phone' command expects one argument 'name'."


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
