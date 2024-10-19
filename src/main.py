from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from enum import Enum

def main():

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            ParentNode("div", [LeafNode("i", "this is a nested child"), LeafNode("b", "This is the second nested child", {"href": "https://www.google.com"})])
        ],
    )

    print(node.to_html())
    
main()