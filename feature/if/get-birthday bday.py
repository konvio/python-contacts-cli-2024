
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







#13/03/24 18:35 


feature/if/get-birthday 



1 варіант 


import json
from datetime import date, datetime
from typing import Optional
from collections import defaultdict

from my_contacts.models.contact import Contact
from my_contacts.config import WEEKDAYS, MONDAY_INDEX, NEXT_MONDAY_INDEX, DATE_FORMAT

class MyAssistant:
    
    @staticmethod
    def print_upcoming_birthdays(contacts: list[Contact], days: int = 7):
        print(f"Upcoming birthdays in the next {days} days: for {len(contacts)} contacts")

    @staticmethod
    def get_birthdays_per_week(contacts, number_of_days):
        relative_date = datetime.today().date()

        next_week_birthday_colleagues = defaultdict(list)

        for colleague in contacts.values():
            name = colleague.name
            if not colleague.birthday:
                continue
            birthday = colleague.birthday.get_birthday_datetime()
            birthday_this_year = MyAssistant._get_birthday_this_year(birthday, relative_date)

            delta_days = (birthday_this_year - relative_date).days
            if delta_days < number_of_days:
                weekday_to_greet = MyAssistant._get_greeting_day(birthday_this_year, relative_date)
                next_week_birthday_colleagues[weekday_to_greet].append(
                    f"{name} ({birthday_this_year.strftime(DATE_FORMAT)})"
                )

        relative_date_str = f"{relative_date.strftime(DATE_FORMAT)}, {WEEKDAYS[relative_date.weekday()]}"

        greeting_string = f"---\nColleagues to greet for the next week, as of {relative_date_str}:\n---"
        if next_week_birthday_colleagues:
            for week_day in WEEKDAYS:
                week_day_birthdays = next_week_birthday_colleagues.get(week_day)
                if week_day_birthdays:
                    greeting_string += f"\n{week_day}: {', '.join(week_day_birthdays)}"
        else:
            greeting_string += "\nNo birthdays this week :("

        return greeting_string

    @staticmethod
    def _get_birthday_this_year(birthday: date, relative_date: date) -> date:
        birthday_this_year = birthday.replace(year=relative_date.year)
        if birthday_this_year < relative_date:
            birthday_this_year = birthday_this_year.replace(year=relative_date.year + 1)

        return birthday_this_year

    @staticmethod
    def _get_greeting_day(birthday_this_year: date, relative_date: date) -> str:
        if birthday_this_year.weekday() >= 5:
            if relative_date.weekday() == 0:
                return WEEKDAYS[NEXT_MONDAY_INDEX]
            else:
                return WEEKDAYS[MONDAY_INDEX]
        else:
            return WEEKDAYS[birthday_this_year.weekday()]

# Виклик функції для демонстрації роботи
contacts = {...}  # Ваші контакти
greeting_message = MyAssistant.get_birthdays_per_week(contacts, 7)
print(greeting_message) 



Інтегрований варіант 


import json
from collections import UserDict, defaultdict
from datetime import date, datetime
from typing import Optional

from my_contacts.models.contact import Contact
from my_contacts.config import WEEKDAYS, MONDAY_INDEX, NEXT_MONDAY_INDEX, DATE_FORMAT

class MyAssistant(UserDict):
    
    def add_contact(self, contact: Contact) -> None:
        self.data[contact.name] = contact

    def find_contact(self, name: str) -> Optional[Contact]:
        return self.data.get(name)

    def delete_contact(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
            print(f"{name} contact is deleted")
        else:
            print(f"No contacts found by the name {name}")

    def save_to_file(self, filename: str) -> None:
        with open(filename, "w") as f:
            contacts_list = [contact.to_dict() for contact in self.data.values()]
            json.dump(contacts_list, f)

    @staticmethod
    def load_from_file(filename: str) -> "MyAssistant":
        with open(filename, "r") as f:
            contacts_list = json.load(f)
        my_assistant = MyAssistant()
        for contact_dict in contacts_list:
            contact = Contact.from_dict(contact_dict)
            my_assistant.add_contact(contact)
        return my_assistant

    def get_birthdays_per_week(self, relative_date: date = datetime.today().date()) -> str:
        next_week_birthday_contacts = defaultdict(list)

        for contact in self.data.values():
            name = contact.name
            if not contact.birthday:
                continue
            birthday = contact.birthday.get_birthday_datetime()
            birthday_this_year = MyAssistant._get_birthday_this_year(birthday, relative_date)

            delta_days = (birthday_this_year - relative_date).days
            if delta_days < 7:
                weekday_to_greet = MyAssistant._get_greeting_day(birthday_this_year, relative_date)
                next_week_birthday_contacts[weekday_to_greet].append(
                    f"{name} ({birthday_this_year.strftime(DATE_FORMAT)})"
                )

        relative_date_str = f"{relative_date.strftime(DATE_FORMAT)}, {WEEKDAYS[relative_date.weekday()]}"

        greeting_string = f"---\nContacts to greet for the next week, as of {relative_date_str}:\n---"
        if next_week_birthday_contacts:
            for week_day in WEEKDAYS:
                week_day_birthdays = next_week_birthday_contacts.get(week_day)
                if week_day_birthdays:
                    greeting_string += f"\n{week_day}: {', '.join(week_day_birthdays)}"
        else:
            greeting_string += "\nNo birthdays this week :("

        return greeting_string

    @staticmethod
    def _get_birthday_this_year(birthday: date, relative_date: date) -> date:
        birthday_this_year = birthday.replace(year=relative_date.year)
        if birthday_this_year < relative_date:
            birthday_this_year = birthday_this_year.replace(year=relative_date.year + 1)

        return birthday_this_year

    @staticmethod
    def _get_greeting_day(birthday_this_year: date, relative_date: date) -> str:
        if birthday_this_year.weekday() >= 5:
            if relative_date.weekday() == 0:
                return WEEKDAYS[NEXT_MONDAY_INDEX]
            else:
                return WEEKDAYS[MONDAY_INDEX]
        else:
            return WEEKDAYS[birthday_this_year.weekday()]

# Usage example:
my_assistant = MyAssistant()
# Add your contacts to my_assistant
# my_assistant.add_contact(...)
# Assume contacts have been add 



2й варіант 




from datetime import date, datetime
from collections import defaultdict
from typing import List

from my_contacts.models.contact import Contact
from my_contacts.config import WEEKDAYS, MONDAY_INDEX, NEXT_MONDAY_INDEX, DATE_FORMAT


class MyAssistant:

    @staticmethod
    def print_upcoming_birthdays(contacts: List[Contact], days: int = 7):
        print(f"Upcoming birthdays in the next {days} days for {len(contacts)} contacts")

    @staticmethod
    def get_birthdays_per_week(contacts: dict, number_of_days: int) -> str:
        relative_date = datetime.today().date()
        next_week_birthday_colleagues = defaultdict(list)

        for colleague in contacts.values():
            name = colleague.name
            if not colleague.birthday:
                continue
            birthday = colleague.birthday.get_birthday_datetime()
            birthday_this_year = MyAssistant._get_birthday_this_year(birthday, relative_date)

            delta_days = (birthday_this_year - relative_date).days
            if delta_days < number_of_days:
                weekday_to_greet = MyAssistant._get_greeting_day(birthday_this_year, relative_date)
                next_week_birthday_colleagues[weekday_to_greet].append(
                    f"{name} ({birthday_this_year.strftime(DATE_FORMAT)})"
                )

        relative_date_str = f"{relative_date.strftime(DATE_FORMAT)}, {WEEKDAYS[relative_date.weekday()]}"
        greeting_string = f"---\nColleagues to greet for the next week, as of {relative_date_str}:\n---"
        if next_week_birthday_colleagues:
            for week_day in WEEKDAYS:
                week_day_birthdays = next_week_birthday_colleagues.get(week_day)
                if week_day_birthdays:
                    greeting_string += f"\n{week_day}: {', '.join(week_day_birthdays)}"
        else:
            greeting_string += "\nNo birthdays this week :("

        return greeting_string

    @staticmethod
    def _get_birthday_this_year(birthday: date, relative_date: date) -> date:
        birthday_this_year = birthday.replace(year=relative_date.year)
        if birthday_this_year < relative_date:
            birthday_this_year = birthday_this_year.replace(year=relative_date.year + 1)
        return birthday_this_year

    @staticmethod
    def _get_greeting_day(birthday_this_year: date, relative_date: date) -> str:
        if birthday_this_year.weekday() >= 5:
            if relative_date.weekday() == 0:
                return WEEKDAYS[NEXT_MONDAY_INDEX]
            else:
                return WEEKDAYS[MONDAY_INDEX]
        else:
            return WEEKDAYS[birthday_this_year.weekday()]


# Assume contacts have been defined with your data here

# Creating an instance of MyAssistant and processing the upcoming birthdays
my_assistant = MyAssistant()
greeting_message = my_assistant.get_birthdays_per_week(contacts, 7)
print(greeting_message)


2й варіант 

Інтегрований 


import json
from collections import UserDict, defaultdict
from datetime import date, datetime
from typing import Optional

from my_contacts.models.contact import Contact
from my_contacts.config import WEEKDAYS, MONDAY_INDEX, NEXT_MONDAY_INDEX, DATE_FORMAT


class MyAssistant(UserDict):

    def add_contact(self, contact: Contact) -> None:
        self.data[contact.name] = contact

    def find_contact(self, name: str) -> Optional[Contact]:
        return self.data.get(name)

    def delete_contact(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
            print(f"{name} contact is deleted")
        else:
            print(f"No contacts found by the name {name}")

    def save_to_file(self, filename: str) -> None:
        with open(filename, "w") as f:
            contacts_list = [contact.to_dict() for contact in self.data.values()]
            json.dump(contacts_list, f)

    @staticmethod
    def load_from_file(filename: str) -> "MyAssistant":
        with open(filename, "r") as f:
            contacts_list = json.load(f)
        my_assistant = MyAssistant()
        for contact_dict in contacts_list:
            contact = Contact.from_dict(contact_dict)
            my_assistant.add_contact(contact)
        return my_assistant

    def get_birthdays_per_week(self, relative_date: date = datetime.today().date()) -> str:
        next_week_birthday_contacts = defaultdict(list)

        for contact in self.data.values():
            name = contact.name
            if not contact.birthday:
                continue
            birthday = contact.birthday.get_birthday_datetime()
            birthday_this_year = self._get_birthday_this_year(birthday, relative_date)

            delta_days = (birthday_this_year - relative_date).days
            if delta_days < 7:
                weekday_to_greet = self._get_greeting_day(birthday_this_year, relative_date)
                next_week_birthday_contacts[weekday_to_greet].append(
                    f"{name} ({birthday_this_year.strftime(DATE_FORMAT)})"
                )

        relative_date_str = f"{relative_date.strftime(DATE_FORMAT)}, {WEEKDAYS[relative_date.weekday()]}"

        greeting_string = f"---\nContacts to greet for the next week, as of {relative_date_str}:\n---"
        if next_week_birthday_contacts:
            for week_day in WEEKDAYS:
                week_day_birthdays = next_week_birthday_contacts.get(week_day)
                if week_day_birthdays:
                    greeting_string += f"\n{week_day}: {', '.join(week_day_birthdays)}"
        else:
            greeting_string += "\nNo birthdays this week :("

        return greeting_string

    @staticmethod
    def _get_birthday_this_year(birthday: date, relative_date: date) -> date:
        birthday_this_year = birthday.replace(year=relative_date.year)
        if birthday_this_year < relative_date:
            birthday_this_year = birthday_this_year.replace(year=relative_date.year + 1)

        return birthday_this_year

    @staticmethod
    def _get_greeting_day(birthday_this_year: date, relative_date: date) -> str:
        if birthday_this_year.weekday() >= 5:
            if relative_date.weekday() == 0:
                return WEEKDAYS[NEXT_MONDAY_INDEX]
            else:
                return WEEKDAYS[MONDAY_INDEX]
        else:
            return WEEKDAYS[birthday_this_year.weekday()]


# Usage example:
my_assistant = MyAssistant()
# Add your contacts to my_assistant
# my_assistant.add_contact(...)
# Assume contacts have been added




