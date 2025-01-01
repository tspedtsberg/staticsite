from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        #check if other is a TextNode
        if not isinstance(other, TextNode):
            return False
        #check if other is equal to self.
        return other.text == self.text and other.text_type == self.text_type and other.url == self.url
        

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
