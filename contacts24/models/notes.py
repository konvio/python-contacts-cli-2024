from collections import UserDict

from contacts24.models.note import Note

# Temporary contract
class Notes(UserDict):
    def add_note(self, note: Note) -> None:
        # To complete by Sergii Shulga
        pass
def get_notes():
    pass

from collections import UserDict
from contacts24.errors import NonExistingNote


class Note(UserDict):
    """Цей клас має функціонал для роботи з нотатками"""
    def add_note(self, client_id, title, text):
        """Додає нову нотатку до записника."""
        note_id = len(self.data) + 1  # Генерує унікальний ідентифікатор для нотатки
        self.data[note_id] = {'client_id': client_id, 'title': title, 'text': text}

    def change_note(self, key, new_text):
        """Змінює текст існуючої нотатки за її ключем."""
        if key in self.data:
            self.data[key]['text'] = new_text
        else:
            raise NonExistingNote()

    def get_notes(self):
        """Повертає всі нотатки з записника."""
        return self.data.values()

    def delete_note(self, key):
        """Видаляє нотатку за її ключем."""
        if key in self.data:
            del self.data[key]
        else:
            raise KeyError(f"Note with key {key} not found.")

    def search_text(self, search_query):
        """Пошук нотаток за текстовим запитом."""
        found_notes = []
        for note_id, note_data in self.data.items():
            if search_query in note_data['text']:
                found_notes.append((note_id, note_data))
        return found_notes


