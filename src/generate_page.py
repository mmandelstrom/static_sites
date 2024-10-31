markdown = "./static/content/index.md"

def extract_title(markdown):
    lines = open(markdown)
    for line in lines:
        print(line)

extract_title(markdown)
