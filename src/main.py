from textnode import TextNode, TextType
import os, shutil
from markdown_to_html import markdown_to_html_node, extract_title

def main():
    static_root = "./static/"
    public_root = "./public/"

    def clear_public(folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(f"Creating directory: {folder}")

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            
            try:

                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleting file: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleting folder: {file_path}")

            except Exception as e:
                print(f'Could not remove {file_path}. Error: {e}')
   


    def copy_static(source, destination):
        if not os.path.exists(destination):
            os.mkdir(destination)
            print(f"Creating directory: {destination}")

        for filename in os.listdir(source):
            source_path = os.path.join(source, filename)
            destination_path = os.path.join(destination, filename)

            if os.path.isfile(source_path):
                shutil.copy(source_path, destination_path)
                print(f"Copying {source_path} to {destination_path}")

            elif os.path.isdir(source_path):
                if not os.path.exists(destination_path):
                    os.mkdir(destination_path)
                    print(f"Creating directory: {destination_path}")
                copy_static(source_path, destination_path)
                    


    clear_public(public_root)
    copy_static(static_root, public_root)


    def generate_page(from_path, template_path, dest_path):
        print(f"Generating a page from {from_path} to {dest_path} using {template_path}")

        with open(from_path) as f:
            md = f.read()

        with open(template_path) as t:
            template = t.read()

        node = markdown_to_html_node(md)
        html = node.to_html()
        title = extract_title(md)
        template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

        with open(dest_path, 'w') as f:
            f.write(template)



    generate_page("./content/index.md", "./template.html", "./public/index.html")
main()