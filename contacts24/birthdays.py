rom collections import defaultdict
from datetime import date, datetime, timedelta
from typing import DefaultDict, List

from contacts24.config import DATE_FORMAT
from contacts24.models.address_book import AddressBook


def get_birthdays_within_days(address_book: AddressBook, within_days: int) -> str:
    relative_date = _get_relative_date(within_days)
    birthday_map = _construct_birthday_map(address_book, relative_date, within_days)

    return _construct_greeting_string(relative_date, birthday_map, within_days)


def _construct_birthday_map(address_book: AddressBook, relative_date: date, within_days: int) -> DefaultDict[str, List[str]]:
    birthday_map = defaultdict()

    # Initialize an ordered dictionary with date keys for within_days
    ordered_keys = []
    for i in range(within_days):
        current_date_key = f"In {i} days ({(relative_date + timedelta(days=i)).strftime(DATE_FORMAT)})"
        ordered_keys.append(current_date_key)
        birthday_map[current_date_key] = []

    for colleague in address_book.data.values():
        name = colleague.name.value

        if not colleague.birthday:
            continue

        birthday = colleague.birthday.get_birthday_datetime()
        birthday_this_year = _get_birthday_this_year(birthday, relative_date)
        
        delta_days = (birthday_this_year - relative_date).days

        if 0 <= delta_days < within_days:
            current_date_key = f"In {delta_days} days ({(relative_date + timedelta(delta_days)).strftime(DATE_FORMAT)})"
            birthday_map[current_date_key].append(
                f"{name}"
            )

    birthday_map = {k: v for k, v in birthday_map.items() if v}

    return birthday_map

def _get_birthday_this_year(birthday: date, relative_date: date) -> date:
    birthday_this_year = birthday.replace(year=relative_date.year)
    
    if birthday_this_year < relative_date:
        birthday_this_year = birthday_this_year.replace(year=relative_date.year + 1)

    return birthday_this_year


def _get_relative_date(within_days: int) -> date:
    return (datetime.now()).date()


def _construct_greeting_string(relative_date: date, birthday_map: DefaultDict[str, List[str]], within_days: int) -> str:
    greeting_string = f"---\nColleagues to greet for the next {within_days} days, as of {relative_date.strftime(DATE_FORMAT)}:\n---"
    
    if birthday_map:
        for week_day in birthday_map:
            week_day_birthdays = birthday_map[week_day]
            if week_day_birthdays:
                greeting_string += f"\n{week_day}: {', '.join(week_day_birthdays)}"
    else:
        greeting_string += "\nNo birthdays this week :("

    return greeting_string

