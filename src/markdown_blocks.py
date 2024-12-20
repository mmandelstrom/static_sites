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

    if block.startswith("# "):
        return "heading_1"
    
    elif block.startswith("## "):
        return "heading_2"
    
    elif block.startswith("### "):
        return "heading_3"
    
    elif block.startswith("#### "):
        return "heading_4"
    
    elif block.startswith("##### "):
        return "heading_5"
    
    elif block.startswith("###### "):
        return "heading_6"
    
    elif block.startswith("```") and block.endswith("```"):
        return "code_block"
    
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
    result = []

    for block in blocks:
        block_type = block_to_block_type(block)
        result.append(block_to_html_node(block, block_type))

    return ParentNode("div", result)



def block_to_html_node(block, block_type):
    result = []
    lines = block.split("\n")

    match(block_type):
        
        case "paragraph":
            return ParentNode("p",text_to_children(block))
        
        case "ordered_list":
            for i, item in enumerate(lines ,start=1):
                prefix = f"{i}. "
                line = item.lstrip(prefix)
                result.append(ParentNode("li", text_to_children(line)))
            return ParentNode('ol', result)

        case "heading_1":
            block = block.strip("# ")
            return ParentNode("h1", text_to_children(block))
        
        case "heading_2":
            block = block.strip("## ")
            return ParentNode("h2", text_to_children(block))
        
        case "heading_3":
            block = block.strip("### ")
            return ParentNode("h3", text_to_children(block))
        
        case "heading_4":
            block = block.strip("#### ")
            return ParentNode("h4", text_to_children(block))
        
        case "heading_5":
            block = block.strip("##### ")
            return ParentNode("h5", text_to_children(block))
        
        case "heading_6":
            block = block.strip("###### ")
            return ParentNode("h6", text_to_children(block))

        case "unordered_list":
            for line in lines:
                line = line.strip("*- ")
                result.append(ParentNode("li", text_to_children(line)))
            return ParentNode('ul',result)

        case "code_block":
            block = block.strip("```")
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, block)])])
        
        case "quote":
            for line in lines:
                line = line.lstrip(">").lstrip()
                result.extend(text_to_children(line))
            return ParentNode("blockquote", result)



def text_to_children(text):
    result = []
    final = text_to_textnodes(text)

    for node in final:
        html_node = text_node_to_html_node(node)
        result.append(html_node)

    return result


