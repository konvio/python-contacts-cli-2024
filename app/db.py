import datetime
from app.model import Contact, Note


def get_contacts() -> list[Contact]:
    return [
        Contact(
            name="John Doe",
            email="john@doe.com",
            phones=["123456789", "987654321"],
            address="Somewhere",
            birthday=datetime.date(1990, 1, 1),
        ),
    ]


def save_contacts(contacts: list[Contact]):
    print(f"Saving {len(contacts)} contacts...")


def get_notes() -> list[Note]:
    return [
        Note(
            title="My first note",
            content="This is the content of my first note",
            created_at=datetime.datetime(2021, 1, 1, 12, 0, 0),
            updated_at=datetime.datetime(2021, 1, 1, 12, 0, 0),
            tags=["first", "note"],
        ),
    ]
