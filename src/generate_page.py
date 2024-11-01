#markdown = "./static/content/index.md"
from htmlnode import *
from markdown_blocks import *
import os


def extract_title(markdown):

    #for Using md file:
    #lines = open(markdown, "r")

    # For using raw markdown
    lines = markdown.splitlines()
    

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found in the markdown.")



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as original_file, open(template_path, "r") as template_file:
        original_content = original_file.read()
        template_content = template_file.read()

    original_to_html_node = markdown_to_html_node(original_content)
    original_to_html = original_to_html_node.to_html()
    title = extract_title(original_content)
    page_content = template_content.replace("{{ Title }}", title)
    page_content = page_content.replace("{{ Content }}", original_to_html)

    with open(dest_path, "w") as result:
        result.write(page_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        ext = item.split(".")[-1]
        source_path = os.path.join(dir_path_content, item)
        

        if os.path.isfile(source_path) and ext == "md":
            dest_path = os.path.join(dest_dir_path, "index.html")
            os.makedirs(dest_dir_path, exist_ok=True)

            with open(source_path, "r") as original_file, open(template_path, "r") as template_file:
                original_content = original_file.read()
                template_content = template_file.read()

                original_to_html_node = markdown_to_html_node(original_content)
                original_to_html = original_to_html_node.to_html()
                title = extract_title(original_content)
                page_content = template_content.replace("{{ Title }}", title)
                page_content = page_content.replace("{{ Content }}", original_to_html)

                
                with open(dest_path, "w") as result:
                    result.write(page_content)

        if os.path.isdir(source_path):
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_dir_path, exist_ok=True)
            print(f"new path: {new_dest_dir_path}")

            generate_pages_recursive(source_path, template_path, new_dest_dir_path)




