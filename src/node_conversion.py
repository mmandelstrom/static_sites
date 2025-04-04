from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node): #Function to convert text_nodes to leafnodes
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError(f"Link nodes require a non-empty 'url'. Got: {text_node.url}")
            return LeafNode("a", text_node.text, {'href': text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError(f"Image nodes require a non-empty 'url'. Got: {text_node.url}")
            return LeafNode("img", "", {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception("Invalid Text type")
        

