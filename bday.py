
# Нова креативна варіація оригінальної програми.
# Головна ідея цих змін полягає в тому, щоб додати функціональність нагадування для того,
# щоб користувачі пригадували про наближаються дні народження протягом певної кількості днів.
# Також додано обробку помилок для неправильного введення дати та неіснуючих контактів.

from datetime import datetime, timedelta

class AddBirthdayInputError(Exception):
    pass

class NonExistingContactError(Exception):
    pass

# Припускаючи, що декоратор @input_error визначений десь в коді.
@input_error
def add_birthday_reminder(args, contacts, days_remaining):
    if args is None or len(args) < 2:
        raise AddBirthdayInputError()

    name, date = args[:2]

    try:
        birthdate = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise AddBirthdayInputError("Invalid date format. Date should be in YYYY-MM-DD format.")

    contact = contacts.find(name)
    if not contact:
        raise NonExistingContactError("Contact does not exist.")

    contact.add_birthday(date)

    today = datetime.now().date()
    upcoming_birthday = datetime(today.year, birthdate.month, birthdate.day).date()

    if days_remaining > 0 and (upcoming_birthday - today).days <= days_remaining:
        return f"Birthday added for {name}. Reminder: {days_remaining} days remaining until their birthday!"
    else:
        return f"Birthday added for {name}."

# Приклад використання:
args = ["Alice", "2024-08-15"]
days_remaining = 30
# Припускаючи, що contacts є визначеним об'єктом AddressBook.
result = add_birthday_reminder(args, contacts, days_remaining)
print(result)
