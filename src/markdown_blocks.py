from htmlnode import *
from textnode import *
from inline_markdown import *

def markdown_to_blocks(markdown):
    split_lines = markdown.split("\n\n")
    result = []
    for i, line in enumerate(split_lines):
        result.append(line.strip())
    return result

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    
    elif all(item.startswith(">") for i, item in enumerate(lines)):
        return "quote"
    
    elif all(item.startswith("* ") or item.startswith("- ") for i, item in enumerate(lines)):
        return "unordered_list"
    
    elif all(item.startswith(f"{i}. ") for i, item in enumerate(lines ,start=1)):
        return "ordered_list"
    
    else:
        return "paragraph"
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        print(node)


def block_to_html_node(block, block_type):
    match(block_type):

        case "paragraph":
            return HTMLNode("p", block)
        
        case "ordered_list":
            return HTMLNode("ol", block)

        case "heading":
            return HTMLNode("h1", block)

        case "unordered_list":
            return HTMLNode("ul", block)

        case "code":
            return HTMLNode("code", block)


def text_to_children(text):
    result = []
    node = TextNode(text, TextType.TEXT)
    delimit_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    delimit_italic = split_nodes_delimiter(delimit_bold, "*", TextType.ITALIC)
    delimit_code = split_nodes_delimiter(delimit_italic, "`", TextType.CODE)
    split_link = split_nodes_link(delimit_code)
    final = split_nodes_image(split_link)
    
    for node in final:
        html_node = text_node_to_html_node(node)
        result.append(html_node)
        
    return result


text = "This is some text with **bold** and some *italic* inside it and some `code`"
nodes = text_to_children(text)
for node in nodes:
    print(isinstance(node, LeafNode))  # Should print True for all

print(nodes)