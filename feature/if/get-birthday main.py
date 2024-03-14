from datetime import date
from typing import List


class Contact:
    def __init__(self, name: str, birthday: date):
        self.name = name
        self.birthday = birthday


def get_birthdays(contacts: List[Contact], number_of_days: int) -> List[Contact]:
    """Get a list of contacts with upcoming birthdays within a specified number of days."""
    upcoming_birthdays = []
    current_date = date.today()

    for contact in contacts:
        birthday_this_year = contact.birthday.replace(year=current_date.year)
        if birthday_this_year < current_date:
            birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)

        if (birthday_this_year - current_date).days <= number_of_days:
            upcoming_birthdays.append(contact)

    return upcoming_birthdays


def print_upcoming_bdays(contacts: List[Contact], days: int = 7):
    """Print the contacts with upcoming birthdays within the next specified number of days."""
    upcoming_birthdays = get_birthdays(contacts, days)
    print(f"Upcoming birthdays in the next {days} days:")
    for contact in upcoming_birthdays:
        print(f"{contact.name} - {contact.birthday.strftime('%Y-%m-%d')}")


# Sample usage:
# contacts = [... list of Contact instances ...]
# print_upcoming_bdays(contacts, 7)
