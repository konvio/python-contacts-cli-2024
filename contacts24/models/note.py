
from contacts24.models.record import Field


class Id(Field):
    pass 


class Title(Field):
    pass 


class Text(Field):
    pass 


class Note():
    def __init__(self, id: int, title: str, text=""):
        self.id = Id(id)
        self.title = Title(title)
        self.text = Text(text)
        self.tags = []

    def add_text(self, id: int, text: str):
        """Add text to the note with the given id."""
        if id in self.text:
            self.text += "\n" + text  # Append text to existing text
        else:
            self.text = text

    def get_text(self, id: int) -> str:
        """Get the text of the note with the given id."""
        return self.text.get(id, "")

    def add_tag(self, tag: str):
        """Add a tag to note."""
        self.tags.append(tag)

    def search_by_tag(self, tag: str) -> bool:
        """Check if the note contains the specified tag."""
        return tag in self.tags