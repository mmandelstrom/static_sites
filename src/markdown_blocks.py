def markdown_to_blocks(markdown):
    split_lines = markdown.split("\n\n")
    result = []
    for i, line in enumerate(split_lines):
        result.append(line.strip())
    return result
