from contacts24.models.record import Field


class Id(Field):
    pass 

class Text(Field):
    pass 

class Note():
    def __init__(self, id: int, title: str, text=""):
        self.id = Id(id)
        self.text = Text(text)
        self.tags = []

    def get_text(self, id: int) -> str:
        """Get the text of the note with the given id."""
        
        return self.text.get(id, "")

    def add_tag(self, tag: str):
        """Add a tag to note."""
        
        self.tags.append(tag)

    def contains_tag(self, tag: str) -> bool:        
        """Check if the note contains the specified tag."""
        
        return tag in self.tags
    
    def __str__(self):
        return (f"Note:\n"
                f"  Id: {self.id}\n"
                f"  Tags: {', '.join(self.tags)}\n\n"
                f"  Text: {self.text}")

