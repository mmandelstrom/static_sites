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