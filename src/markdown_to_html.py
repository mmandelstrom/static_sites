from block_funcs import *
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from node_conversion import text_node_to_html_node
from inline_funcs import text_to_textnodes

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        nodes.append(block_to_html_node(block, block_type))
    return ParentNode("div", nodes)




def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.HEADING:
            if block.startswith("# "):
                return ParentNode("h1", text_to_children(block.strip("# ")))
            elif block.startswith("## "):
                return ParentNode("h2", text_to_children(block.strip("## ")))
            elif block.startswith("### "):
                return ParentNode("h3", text_to_children(block.strip("### ")))
            elif block.startswith("#### "):
                return ParentNode("h4", text_to_children(block.strip("#### ")))
            elif block.startswith("##### "):
                return ParentNode("h5", text_to_children(block.strip("##### ")))
            elif block.startswith("###### "):
                return ParentNode("h6", text_to_children(block.strip("###### ")))
            
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block.replace("\n", " "))) #In raw html we replace newlines with spaces
        
        case BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.strip(">"))
            text = "\n".join(new_lines)
            return ParentNode("blockquote", text_to_children(text.replace("\n", " ")))
        
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            res = ""
            list_items = []
            for line in lines:
                list_items.append(ParentNode("li", text_to_children(line.strip("-"))))
            return ParentNode("ul", list_items)
        
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            res = ""
            list_items = []
            i = 1
            for line in lines:
                list_items.append(ParentNode("li", text_to_children(line.strip(f"{i}."))))
                i += 1
            return ParentNode("ol", list_items)
        
        case BlockType.CODE:
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, block.strip("```").lstrip("\n"))])])
            


def text_to_children(text):
    res = []
    child_nodes = text_to_textnodes(text)
    for node in child_nodes:
        res.append(text_node_to_html_node(node))
    return res


    