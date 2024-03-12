from dataclasses import dataclass
import datetime


@dataclass
class Contact:
    name: str
    email: str
    phones: list[str]
    address: str
    birthday: datetime.date


@dataclass
class Note:
    title: str
    content: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tags: list[str]
