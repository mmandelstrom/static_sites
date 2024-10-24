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
    

