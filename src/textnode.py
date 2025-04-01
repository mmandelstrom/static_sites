from enum import Enum 


class TextType(Enum): #Enum to provide valid text-types
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class Textnode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other): #Method to compare textnodes objects for tests
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self): #Method to print textnodes
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
