import re
from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
#loop through all nodes and check if TexType is TEXT
#If it's just appends the node as is to result
    for node in old_nodes:
        if node.text_type == TextType.TEXT:

#Check wether delimiter is present, if it is attempt to split in to 3 parts
            if delimiter in node.text:
                parts = node.text.split(delimiter, 2)

#If string is only split in to 2 parts, there is an unclosed delimiter, we raise Exception
                if len(parts) %  2 == 0:
                    raise Exception("Invalid markdown")

#If the string is successfully split in to 3 parts we define first, middle and end                
                if len(parts) == 3:
                    first, middle, last = parts 

#check wether first/last are none and create textnodes accordingly
                    if first and last:
                        result.extend([
                                TextNode(first, TextType.TEXT),
                                TextNode(middle, text_type),
                                TextNode(last, TextType.TEXT)
                                ])
                                                
                    elif first and not last:
                        result.extend([
                                TextNode(first, TextType.TEXT),
                                TextNode(middle, text_type),
                                ])
                    elif not first and last:
                        result.extend([
                            TextNode(middle, text_type),
                            TextNode(last, TextType.TEXT)
                        ])
#If no delimiter is found we append node as is                        
            else:
                result.append(node)

#If text is not TextType TEXT we append node as is                            
        else:
            result.append(node)
    return result



def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        remaining_text = node.text
        links = extract_markdown_links(node.text)

        if not links:
            return [node]

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
        remaining_text = node.text
        links = extract_markdown_images(node.text)

        if not links:
            return [node]
        
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




def extract_markdown_images(text):
    return (re.findall(r'!\[(.*?)\]\((.*?)\)', text))



def extract_markdown_links(text):
    return (re.findall(r'\[(.*?)\]\((.*?)\)', text))
    




