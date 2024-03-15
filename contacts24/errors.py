
class AppError(Exception):
    pass


class InputError(Exception):
    """Base class for other input exceptions"""
    pass


#region Contacts Errors

class AddContactInputError(InputError):
    def __str__(self):
        return "AddContactInputError: 'add-contact' command expects two arguments 'name' and 'phone'"


class AddBirthdayInputError(InputError):
    def __str__(self):
        return "AddBirthdayInputError: 'add-birthday' command expects two arguments 'name' and 'birthday'."


class ChangeInputError(InputError):
    def __str__(self):
        return "ChangeInputError: 'change-phone' command expects two arguments 'name' and 'phone'"

class ChangeEmailInputError(InputError):
    def __str__(self):
        return "ChangeEmailInputError: 'change-email' command expects two arguments 'name' and  'email'."

class FindContactsInputError(InputError):
    def __str__(self):
        return "FindContactsInputError: 'find-contacts' command expects one arguments 'name'."


class AddAddressInputError(InputError):
    def __str__(self):
        return "AddAddressInputError: 'add-address' command expects two arguments 'name' and 'address'."

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


class InAccurateBirthdaysCommand(InputError):
    def __str__(self):
        return "InAccurateBirthdaysCommand: birthdays command expects one numeric argument 'n_days' >= 0"

#endregion

#region Notes errors

class NonExistingNote(InputError):
    def __str__(self):
        return "NonExistingNote: This note does not exist or has been deleted"


class EmptyNoteError(InputError)
    def __str__(self):
        return "EmptyNoteError: No text for note was provided"


class NotEnoughArgumentsInputError(InputError):
    def __str__(self):
        return "NotEnoughArgumentsInputError: add-note' command expects two arguments 'name' and 'phone'"



#endregion

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InputError as e:
            return str(e)

    return inner


def app_error_wrapper(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise AppError(e)

    return inner

