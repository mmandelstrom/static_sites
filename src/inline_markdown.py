import re
from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:

            # Split by all occurrences of the delimiter
            parts = node.text.split(delimiter)

            # If the number of parts is even, raise an exception (this indicates unbalanced delimiters)
            if len(parts) % 2 == 0:
                print(f"Warning: Unbalanced delimiter '{delimiter}' in text: {node.text}")
                

            # Process the parts alternately as text_type and TEXT
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:  # Only add non-empty parts as TEXT
                        result.append(TextNode(part, TextType.TEXT))
                else:
                    if part:  # Only add non-empty parts as the given text_type
                        result.append(TextNode(part, text_type))

        else:
            result.append(node)
    
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        remaining_text = node.text
        links = extract_markdown_links(node.text)

        if not links:
            result.append(node)  
            continue  

        for t in links:
            alt_text = t[0]
            url = t[1]

            if not url:
                raise Exception("Invalid input: Missing URL.")
            
            if alt_text is None:
                alt_text = ""

            divided_text = remaining_text.split(f"[{alt_text}]({url})", 1)
            first_part = divided_text[0]
            next_part = divided_text[1]
            
            if first_part:
                result.append(TextNode(first_part, TextType.TEXT))
            result.append(TextNode(alt_text, TextType.LINK, url))

            remaining_text = next_part

        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))


    return result
    

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        
        remaining_text = node.text
        links = extract_markdown_images(node.text)

        if not links:
            result.append(node)  
            continue  
        
        for t in links:
            
            alt_text = t[0]
            url = t[1]

            if not url:
                raise Exception("Invalid input: Missing URL.")
            
            if alt_text is None:
                alt_text = ""
            
            divided_text = remaining_text.split(f"![{alt_text}]({url})", 1)
            first_part = divided_text[0]
            next_part = divided_text[1]
            
            if first_part:
                result.append(TextNode(first_part, TextType.TEXT))
            result.append(TextNode(alt_text, TextType.IMAGE, url))

            remaining_text = next_part

        if remaining_text:
            result.append(TextNode(remaining_text, TextType.TEXT))


    return result


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    split_image = split_nodes_image([node])
    split_link = split_nodes_link(split_image)
    split_bold = split_nodes_delimiter(split_link, "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "*", TextType.ITALIC)
    final_split = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    return final_split


def extract_markdown_images(text):
    return (re.findall(r'!\[(.*?)\]\((.*?)\)', text))



def extract_markdown_links(text):
    return (re.findall(r'\[(.*?)\]\((.*?)\)', text))


