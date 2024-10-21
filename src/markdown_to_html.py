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


