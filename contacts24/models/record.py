import re
from datetime import date, datetime
from typing import List, Optional

from contacts24.errors import InaccurateBirthdayFormat, InaccuratePhoneFormat, InaccurateEmailFormat
from contacts24.config import DATE_FORMAT


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass

class Address(Field):
    pass


class Email(Field):
    def __init__(self, value: str):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
            raise InaccurateEmailFormat()
        super().__init__(value)

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
        self.emails: List[Email] = []
        self.birthday: Optional[Birthday] = None
        self.address: Optional[Address] = None

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        if new_phone:
            self.phones.append(new_phone)

    def add_email(self, email: str) -> None:
        new_email = Email(email)
        if new_email:
            self.emails.append(new_email)

    def delete_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def delete_email(self, email: str) -> None:
        self.emails = [p for p in self.emails if p.value != email]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for index, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[index] = Phone(new_phone)
                break

    def edit_email(self, old_email: str, new_email: str) -> None:
        for index, p in enumerate(self.emails):
            if p.value == old_email:
                self.emails[index] = Email(new_email)
                break

    def find_phone(self, phone: str) -> Optional[str]:
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def find_email(self, email: str) -> Optional[str]:
        for p in self.emails:
            if p.value == email:
                return p.value
        return None

    def to_dict(self):
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "emails": [email.value for email in self.emails],
            "birthday": self.birthday.value if self.birthday else None,
            "address": self.address.value if self.address else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        record = cls(data["name"])
        for phone in data["phones"]:
            record.add_phone(phone)
        for email in data["emails"]:
            record.add_email(email)
        if data["birthday"]:
            record.add_birthday(data["birthday"])
        if data["address"]:
            record.add_address(data["address"])
        return record

    def __str__(self) -> str:
        return (
            f"Contact name: {self.name}, birthday: {self.birthday}, address: {self.address}, phones: {'; '.join(p.value for p in self.phones)}, emails: {'; '.join(p.value for p in self.emails)}"
        )
