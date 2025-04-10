from block_types import BlockType

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    res = []
    final = []

    for line in lines:
        line = line.strip()
        res.append(line)

    joined_res = "\n".join(res)
    inner_lines = joined_res.split("\n\n")
    for inner_line in inner_lines:
        inner_line = inner_line.strip()
        if len(inner_line) > 0:
            final.append(inner_line)
    return final


def block_to_block_type(block):
    lines = block.split("\n")
    flag = True

    if (block.startswith("# ") or #Handle all heading types
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")):
        return BlockType.HEADING
    
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    elif block.startswith(">"): #For it to be a quote all lines must start with >
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
        return BlockType.PARAGRAPH
       
    elif block.startswith("-"): #All lines must start with - else it's a paragraph
        if all(line.startswith("-") for line in lines):
            return BlockType.UNORDERED_LIST
        return BlockType.PARAGRAPH
        
    elif block.startswith("1."): #All lines must start with 1. 2. etc else its a paragraph
        if all(line.startswith(f"{i}.") for i, line in enumerate(lines, start=1)):
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH
    
    else:
        return BlockType.PARAGRAPH
        
