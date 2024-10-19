from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode
from enum import Enum

def main():

    node = TextNode('text', 'text')
    node2 = TextNode('this is the text', TextType.BOLD)

    html_node = text_node_to_html_node(node2)
  
    print(html_node)
main()