from collections import UserDict
from typing import Optional

from contacts24.models.record import Record
from contacts24.config import ADDRESSBOOK_FILE


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

    def save_to_file(self, filename: str = ADDRESSBOOK_FILE) -> None:
        from contacts24.db import save_address_book
        if filename:
            save_address_book(self, filename)
        else:
            save_address_book(self)

    @staticmethod
    def load_from_file(filename: str = ADDRESSBOOK_FILE) -> "AddressBook":
        from contacts24.db import get_contacts
        if filename:
            return get_contacts(filename)
        else:
            return get_contacts()

    def __str__(self) -> str:
        # Initialize the header and its length
        columns = ['Name', 'Birthday', 'Address', 'Phones', 'Emails']
        col_width = [len(h)+ 3 for h in columns]

        # Gather all data
        data = []
        for name, record in self.data.items():
            phones = ', '.join(str(p.value) for p in record.phones) if record.phones else 'N/A'
            emails = ', '.join(str(e.value) for e in record.emails) if record.emails else 'N/A'
            birthday = str(record.birthday) if record.birthday else 'N/A'
            address = str(record.address) if record.address else 'N/A'
            row = [name, birthday, address, phones, emails]
            
            # Update maximum column width
            col_width = [max(col_width[i], len(cell)) for i, cell in enumerate(row)]

            data.append(row)

        # Define format string for each row
        format_string = ''.join(f'{{:<{w}}} ' for w in col_width)

        # Build table string
        output = format_string.format(*columns) + '\n'
        output += '\n'.join(format_string.format(*row) for row in data)

        return output
