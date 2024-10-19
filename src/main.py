from textnode import TextType, TextNode
from htmlnode import HTMLNode
from enum import Enum

def main():

    node = TextNode("This is my first node", "bold", "https://boot.dev")
    print(node)
    node2 = HTMLNode("div", "This is my value")
    print(node2)

main()