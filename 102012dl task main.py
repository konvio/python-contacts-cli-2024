import json
import os
from datetime import datetime, timedelta


class PersonalAssistant:
    def __init__(self):
        self.contacts = []
        self.notes = []
        self.data_file = "personal_data.json"

        if os.path.exists(self.data_file):
            self.load_data()
        else:
            self.save_data()

    def load_data(self):
        with open(self.data_file, "r") as file:
            data = json.load(file)
            self.contacts = data.get("contacts", [])
            self.notes = data.get("notes", [])

    def save_data(self):
        with open(self.data_file, "w") as file:
            data = {
                "contacts": self.contacts,
                "notes": self.notes
            }
            json.dump(data, file)

    def add_contact(self, name, address, phone, email, birthday):
        new_contact = {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "birthday": birthday
        }
        self.contacts.append(new_contact)
        self.save_data()

    def search_contact(self, search_term):
        results = [contact for contact in self.contacts if search_term.lower() in contact["name"].lower()]
        return results

    def delete_contact(self, name):
        self.contacts = [contact for contact in self.contacts if contact["name"] != name]
        self.save_data()

    def add_note(self, text):
        new_note = {
            "text": text
        }
        self.notes.append(new_note)
        self.save_data()

    def search_note_by_keyword(self, keyword):
        results = [note for note in self.notes if keyword.lower() in note["text"].lower()]
        return results

    def delete_note_by_text(self, text):
        self.notes = [note for note in self.notes if note["text"] != text]
        self.save_data()

    def upcoming_birthdays(self, days):
        current_date = datetime.now()
        upcoming_date = current_date + timedelta(days=days)
        upcoming_birthdays = [
            contact["name"] for contact in self.contacts
            if contact["birthday"] and datetime.strptime(contact["birthday"], "%Y-%m-%d").date() <= upcoming_date.date()
        ]
        return upcoming_birthdays


# Below you can test the functionality of the personal assistant
# assistant = PersonalAssistant()
# assistant.add_contact("John Doe", "123 Main St", "555-1234", "john.doe@example.com", "1990-05-20")
# assistant.add_note("Remember to call Jane.")
# print(assistant.upcoming_birthdays(30))
# print(assistant.search_contact("John"))
# assistant.delete_contact("John Doe")
# print(assistant.search_note_by_keyword("call"))
# assistant.delete_note_by_text("Remember to call Jane.")
