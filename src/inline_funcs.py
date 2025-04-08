import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

"""
Functions to extraxt alt text & urls for images and links
"""
def extract_markdown_images(text):
    res = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return res

def extract_markdown_links(text):
    res = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return res


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid_delimiters = {"**", "`", "_"}
    if delimiter not in valid_delimiters: #Make sure valid delimiter is provided
        raise Exception(f"{delimiter} is not a valid markdown delimiter")
    
    new_nodes = []
    for node in old_nodes: #For each node check if it's a text_type text, if not just add it as it
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else: #Call helper function with each node
            new_nodes.extend(process_text_node(node, delimiter, text_type))
            
    return new_nodes

"""
Helper function, checks for delimiter in textnodes' text and breaks it in to separate textnodes for each type of delimiter
we keep slicing the remaining text using delimiter to portion out each textnode's text
"""
def process_text_node(text_node, delimiter, text_type):
    result = []
    remaining_text = text_node.text

    if not remaining_text or delimiter not in remaining_text:
        result.append(text_node)
        return result

    while delimiter in remaining_text:
        start_index = remaining_text.find(delimiter)

        if start_index == -1:
            break

        if start_index > 0:
            result.append(TextNode(remaining_text[:start_index], TextType.TEXT))
        
        remaining_text = remaining_text[start_index + len(delimiter):]
        end_index = remaining_text.find(delimiter)

        if end_index == -1:
            raise Exception(f"No closing delimiter found for {delimiter}")
        
        result.append(TextNode(remaining_text[:end_index], text_type))
        remaining_text = remaining_text[end_index + len(delimiter):]

    if remaining_text:
        result.append(TextNode(remaining_text, TextType.TEXT))

    return result



def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: #If a node is not text we add it without changing it
            res.append(node)
            continue
            
        text = node.text
        while len(text) > 0:
            extracted_images = extract_markdown_images(text)
            if extracted_images: #Check to make sure functioncall returned something
                image_alt, image_link = extracted_images[0]

                remaining_text = text.split(f"![{image_alt}]({image_link})", maxsplit=1)#Split text on image
                if len(remaining_text[0]) > 0: #If there was text before the image create a textnode
                    res.append(TextNode(remaining_text[0], TextType.TEXT))
                res.append(TextNode(image_alt, TextType.IMAGE, image_link)) #Create textnode for image
                text = remaining_text[1] #update text to parse rest of the string
            else: #If no images are found and there is text create a textnode, else exit loop
                if len(text) > 0:
                    res.append(TextNode(text, TextType.TEXT))
                    break
    return res


def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT: #if old node is not type text, just append to list and move on
            res.append(node)
            continue

        text = node.text
        while len(text) > 0:
            extracted_link = extract_markdown_links(text)
            if extracted_link: #If the input node contains links
                alt_text, url = extracted_link[0]

            remaining_text = text.split(f"[{alt_text}]({url})", maxsplit=1)
            if len(remaining_text[0]) > 0:#If there was text before image add it as node with texttype text
                res.append(TextNode(remaining_text[0], TextType.TEXT))
            res.append(TextNode(alt_text, TextType.LINK, url)) #Add textnode with link
            text = remaining_text[1] #Update text to remaing and continue loop
        else: #If no link is found, add text if there is some then break loop
            if len(text) > 0:
                res.append(TextNode(text, TextType.TEXT))
                break
    return res



node = TextNode(
        "Here is just one image at the end ![final image](https://example.com)",
        TextType.TEXT,
    )



node1 = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)

print(split_nodes_link([node1]))