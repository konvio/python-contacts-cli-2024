
from collections import UserDict

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
            raise KeyError(f"Note with key {key} not found.")

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

def input_error(func):
    """Обробник помилок вводу."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return str(e)
        except IndexError:
            return "Invalid number of arguments."

    return inner

def parse_input(user_input):
    """Розбирає введену команду на команду та аргументи."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_note(args, note_book):
    """Додає нотатку до записника."""
    client_id, title, text = args
    note_book.add_note(client_id, title, text)
    return "Note added."

@input_error
def change_note(args, note_book):
    """Змінює текст існуючої нотатки."""
    key, new_text = args
    note_book.change_note(int(key), new_text)
    return "Note changed."

@input_error
def get_notes(note_book):
    """Показує всі нотатки з записника."""
    notes = note_book.get_notes()
    return "\n".join([str(note) for note in notes])

@input_error
def delete_note(args, note_book):
    """Видаляє нотатку з записника."""
    key, = args
    note_book.delete_note(int(key))
    return "Note deleted."

@input_error
def search_text(args, note_book):
    """Пошук нотаток за текстовим запитом."""
    search_query, = args
    found_notes = note_book.search_text(search_query)
    if found_notes:
        return "\n".join([f"Note ID: {note_id}, Note Data: {note_data}" for note_id, note_data in found_notes])
    else:
        return "No notes found."

