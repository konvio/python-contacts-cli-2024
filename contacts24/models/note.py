from contacts24.models.record import Field
from typing import List
from contacts24.errors import TagAlreadyExistsError

class Id(Field):
    pass 

class Text(Field):
    pass 

class Tag(Field):
    pass

class Note():
    def __init__(self, id: int, text: str):
        self.id = Id(id)
        self.text = Text(text)
        self.tags: List[Tag] = []

    def get_text(self, id: int) -> str:
        """Get the text of the note with the given id."""
        
        return self.text.get(id, "")

    def add_tag(self, input_tag: str):
        """Add a tag to note."""
        
        if input_tag in [tag for tag in self.tags]:
            raise TagAlreadyExistsError()
        
        self.tags.append(Tag(input_tag))
        

    def contains_tag(self, search_tag: str) -> bool:
        """Check if the note contains the specified tag."""

        return any(tag.value == search_tag for tag in self.tags)
    
    def __str__(self):
        return f"""Note:
Id: {self.id}
Tags: {' '.join(f"#{str(t.value)}" for t in self.tags) if self.tags else 'N/A'}
Text: {self.text.value}"""
