
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
    

class ChangeNameInputError(InputError):
    def __str__(self):
        return "ChangeNameInputError: 'change-name' command expects two arguments 'name' and  'new_name'."
    

class FindContactsInputError(InputError):
    def __str__(self):
        return "FindContactsInputError: 'find-contacts' command expects one arguments 'name'."


class DeleteContactError(InputError):
    def __str__(self):
        return "DeleteContactError: 'delete-contact' command expects one arguments 'name'."


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


class InaccurateBirthdaysCommand(InputError):
    def __str__(self):
        return "InaccurateBirthdaysCommand: birthdays command expects one numeric argument 'n_days' >= 0"

#endregion

#region Notes errors

class AddNoteInputError(InputError):
    def __str__(self):
        return "AddNoteInputError: 'add-note' command expects one argument 'text'"

class ChangeNoteError(InputError):
    def __str__(self):
        return "ChangeNoteError: 'change-note' command expects two arguments 'id' and 'new_text'"

class AddTagError(InputError):
    def __str__(self):
        return "AddTagError: 'add-tag' command expects two arguments 'id' and 'tag'"

class DeleteTagError(InputError):
    def __str__(self):
        return "DeleteTagError: 'delete-tag' command expects two arguments 'id' and 'tag'"

class DeleteMissingError(InputError):
    def __str__(self):
        return "DeleteMissingError: This tag does not exist or has been deleted"

class NonExistingNote(InputError):
    def __str__(self):
        return "NonExistingNote: This note does not exist or has been deleted"
    
class TagAlreadyExistsError(InputError):
    def __str__(self):
        return "TagAlreadyExists: This tag already exists"

class FindNoteInputError(InputError):
    def __str__(self):
        return "FindNoteInputError: 'find-notes' command expects one arguments 'search_query'."

class DeleteNoteError(InputError):
    def __str__(self):
        return "DeleteNoteError: 'delete-note' command expects one arguments 'id'."

class InvalidNoteIdError(InputError):
    def __str__(self):
        return "InvalidNoteIdError: Invalid note id."

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

