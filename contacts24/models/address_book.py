import json
from collections import UserDict, defaultdict
from datetime import date, datetime
from typing import Optional

from contacts24.models.record import Record
from contacts24.config import (
    CONTACTS_FILE, WEEKDAYS, MONDAY_INDEX, NEXT_MONDAY_INDEX, DATE_FORMAT
)


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
            print(f"{name} record is deleted")
        else:
            print(f"No records found by the name {name}")

    def save_to_file(self, filename: str = CONTACTS_FILE) -> None:
        with open(filename, "w") as f:
            records_list = [record.to_dict() for record in self.data.values()]
            json.dump(records_list, f)

    @staticmethod
    def load_from_file(filename: str = CONTACTS_FILE) -> "AddressBook":
        with open(filename, "r") as f:
            records_list = json.load(f)
        address_book = AddressBook()
        for record_dict in records_list:
            record = Record.from_dict(record_dict)
            address_book.add_record(record)
        return address_book

    def get_birthdays_per_week(self, relative_date: date = datetime.today().date()) -> str:
        """
        Determine which colleagues have birthdays in the upcoming week.

        Args:
            relative_date (date, optional): The date from which to calculate one week forward. Default is today's date.

        Returns:
            str: A formatted string containing the names of colleagues that have birthdays
                in the upcoming week, sorted by the day of the week.
        """
        next_week_birthday_colleagues = defaultdict(list)

        for colleague in self.data.values():
            name = colleague.name
            if not colleague.birthday:
                continue
            birthday = colleague.birthday.get_birthday_datetime()
            birthday_this_year = self._get_birthday_this_year(birthday, relative_date)

            delta_days = (birthday_this_year - relative_date).days
            if delta_days < 7:
                weekday_to_greet = self._get_greeting_day(birthday_this_year, relative_date)
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
        """
        Returns this year's birthday based on a given reference date.

        Args:
            birthday (date): The birthday date.
            relative_date (date): The reference date.

        Returns:
            date: This year's birthday based on the reference date.
        """

        birthday_this_year = birthday.replace(year=relative_date.year)
        if birthday_this_year < relative_date:
            birthday_this_year = birthday_this_year.replace(year=relative_date.year + 1)

        return birthday_this_year

    @staticmethod
    def _get_greeting_day(birthday_this_year: date, relative_date: date) -> str:
        """
        Returns the weekday to greet the colleague.

        Args:
            birthday_this_year (date): The colleague's birthday this year.
            relative_date (date): The reference date.

        Returns:
            str: The weekday to greet the colleague.
        """

        # if birthday is a weekend and relative_date is Monday, so greeting goes to next Monday
        if (birthday_this_year.weekday() >= 5) & (relative_date.weekday() == 0):
            return WEEKDAYS[NEXT_MONDAY_INDEX]
        elif birthday_this_year.weekday() >= 5:
            return WEEKDAYS[MONDAY_INDEX]
        else:
            return WEEKDAYS[birthday_this_year.weekday()]
