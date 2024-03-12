import re
from datetime import date, datetime
from typing import List, Optional

from contacts24.errors import InaccurateBirthdayFormat, InaccuratePhoneFormat

DATE_FORMAT = "%d.%m.%Y"


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not re.match(r"^\d{10}$", value):
            raise InaccuratePhoneFormat()
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", value):
            raise InaccurateBirthdayFormat()
        super().__init__(value)

    def get_birthday_datetime(self) -> date:
        return datetime.strptime(self.value, DATE_FORMAT).date()


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        if new_phone:
            self.phones.append(new_phone)

    def delete_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for index, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[index] = Phone(new_phone)
                break

    def find_phone(self, phone: str) -> Optional[str]:
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def to_dict(self):
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "birthday": self.birthday.value if self.birthday else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        record = cls(data["name"])
        for phone in data["phones"]:
            record.add_phone(phone)
        if data["birthday"]:
            record.add_birthday(data["birthday"])
        return record

    def __str__(self) -> str:
        return (
            f"Contact name: {self.name}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"
        )
